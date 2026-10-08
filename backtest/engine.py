"""Moteur du modèle A (unfilled FVG), conforme à strategy/pseudocode.md.

Deux passes :
  1. find_events : pour chaque triplet HTF (C1, C2, C3) et chaque sens, toutes les bougies LTF où un
     modèle d'entrée valide se déclenche en W1 (fin de C3) ou W2 (pendant C4). Indépendant des positions.
  2. simulate : parcours chronologique des événements, une seule exposition à la fois, plafond journalier,
     remplissage (marché / limite), sortie (SL, TP, BE, sortie forcée), coûts.
"""
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from . import bars, signals

ROOT = Path(__file__).resolve().parent.parent
TICK = 0.25
POINT_VALUE = 20.0          # NQ : 20 $ par point
ANCHOR = {15: 0, 60: 0, 240: 6 * 60}     # 4 h ancrées à 18:00 ET (Q16)


# ----------------------------------------------------------------------------------------------- paramètres
def default_params():
    data = json.loads((ROOT / "strategy" / "parametres.json").read_text(encoding="utf-8"))
    return {p["nom"]: p["default"] for g in data["groupes"].values() for p in g}


def resolve(p, htf):
    """Les paramètres définis par timeframe ({"15": .., "60": ..}) sont réduits à la valeur du HTF."""
    out = dict(p)
    for k, v in p.items():
        if isinstance(v, dict) and str(htf) in v:
            out[k] = v[str(htf)]
    out["htf_minutes"] = htf
    out["ltf_minutes"] = p["ltf_map"][str(htf)] if isinstance(p["ltf_map"], dict) else p["ltf_map"]
    return out


def hhmm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


# ----------------------------------------------------------------------------------------------- préparation
def prepare(df1m, htf, ltf_minutes):
    ltf = bars.from_frame(df1m, period=ltf_minutes)
    H = bars.htf_over_ltf(ltf, htf, ANCHOR.get(htf, 0))
    H["atr"] = bars.atr(H["h"], H["l"], H["c"])
    return ltf, H


# ----------------------------------------------------------------------------------------------- passe 1
def find_events(ltf, H, p):
    per = p["htf_minutes"]
    n = p["fractal_n"]
    models = tuple(signals.NAME_TO_CODE[m] for m in p["modeles"])
    t_ant = p["w1_minutes_avant_cloture"]
    sess0, sess1 = hhmm(p["session_et"][0]), hhmm(p["session_et"][1])
    rule = p["c3_regle"]
    big = p["grand_range_points_1h"] if per == 60 else None
    o, h, l, c = ltf["o"], ltf["h"], ltf["l"], ltf["c"]
    lt_close = ltf["t_close"]
    events = []
    nH = len(H["t_open"])

    for j in range(2, nH):
        T = H["t_open"]
        if not (T[j - 1] == T[j - 2] + per and T[j] == T[j - 1] + per):
            continue                                                   # C1-C2-C3 contigus (pas de pont de session)
        c4_ok = j + 1 < nH and T[j + 1] == T[j] + per
        h1, l1 = H["h"][j - 2], H["l"][j - 2]
        o2, h2, l2, c2 = H["o"][j - 1], H["h"][j - 1], H["l"][j - 1], H["c"][j - 1]
        rng2 = h2 - l2
        body2 = abs(c2 - o2)
        disp_ok = (p["c2_displacement_atr_k"] == 0 or body2 >= p["c2_displacement_atr_k"] * H["atr"][j - 1]) \
            and (rng2 > 0 and body2 / rng2 >= p["c2_body_ratio_min"])
        if not disp_ok:
            continue
        a3, b3 = H["src_start"][j], H["src_end"][j]
        a4, b4 = (H["src_start"][j + 1], H["src_end"][j + 1]) if c4_ok else (b3, b3)
        struct_start = a3 if p["fenetre_structure_debut"] == "ouverture_C3" else H["src_start"][j - 1]
        o3, h3, l3, c3 = H["o"][j], H["h"][j], H["l"][j], H["c"][j]
        forced_t = {"cloture_C4": T[j] + 2 * per, "cloture_C5": T[j] + 3 * per}.get(p["sortie_forcee"], np.inf)

        for s_f in (+1, -1):
            d = -s_f
            if s_f > 0:
                run_near = np.minimum.accumulate(l[a3:b3])           # bord proche provisoire = plus bas de C3
                run_ext3 = np.maximum.accumulate(h[a3:b3])
                far, ext2 = h1, h2
            else:
                run_near = np.maximum.accumulate(h[a3:b3])
                run_ext3 = np.minimum.accumulate(l[a3:b3])
                far, ext2 = l1, l2
            gap_run = s_f * (run_near - far)                         # taille provisoire du gap
            # validation finale à la clôture de C3
            G = gap_run[-1]
            wick3 = (h3 - max(o3, c3)) if s_f > 0 else (min(o3, c3) - l3)
            final_ok = (c4_ok and G >= p["gap_min_points"] and s_f * (c3 - ext2) < 0
                        and ("sweep" not in rule or s_f * (run_ext3[-1] - ext2) > 0)
                        and ("wick" not in rule or (h3 - l3 > 0 and wick3 >= p["c3_wick_min"] * (h3 - l3))))

            # bougies W1
            w1 = []
            if p["w1_actif"]:
                for k in range(a3, b3 - 1):                          # la dernière bougie de C3 relève de W2
                    t_rem = T[j] + per - lt_close[k]
                    r = k - a3
                    if (0 < t_rem <= t_ant and gap_run[r] >= p["gap_min_points"]
                            and ("sweep" not in rule or s_f * (run_ext3[r] - ext2) > 0)
                            and s_f * (c[k] - ext2) < 0
                            and s_f * (ext2 - c[k]) >= p["w1_distance_c2_frac"] * rng2):
                        w1.append(k)
            w2_on = final_ok and p["w2_actif"]
            if not w1 and not w2_on:
                continue

            end = b4 if w2_on else b3
            ctx0 = max(0, struct_start - n)
            sl_ = slice(ctx0, end)
            k_from = min(w1[0] if w1 else b3 - 1, b3 - 1) - ctx0
            mdl, zone, inv = signals.scan(d, o[sl_], h[sl_], l[sl_], c[sl_], struct_start - ctx0, n=n,
                                          ifvg_min=p["ifvg_min_points"], models=models, k_from=k_from)

            def add(k, window, near, ext3, rng3, mid3):
                r = k - ctx0
                if mdl[r] == 0:
                    return
                tod = int(lt_close[k] % 1440)
                if not (sess0 <= tod < sess1):
                    return
                tp_level = near - p["tp_profondeur"] * (near - far)    # du bord proche vers le bord lointain
                events.append({
                    "k": k, "j": j, "s_f": s_f, "dir": d, "window": window,
                    "model": signals.MODEL_NAMES[int(mdl[r])], "zone": float(zone[r]), "inv": float(inv[r]),
                    "tp_level": float(tp_level), "near": float(near), "ext3": float(ext3),
                    "big_range": big is not None and rng3 > big, "mid3": mid3,
                    "expire": (b4 - 1) if c4_ok else (b3 - 1), "forced_t": forced_t,
                    "gap": float(s_f * (near - far)), "rng2": float(rng2), "body2_atr": float(body2 / H["atr"][j - 1]),
                    "sweep_c2": bool(s_f * (run_ext3[min(k, b3 - 1) - a3] - ext2) > 0),
                })

            for k in w1:
                r = k - a3
                hi3, lo3 = h[a3:k + 1].max(), l[a3:k + 1].min()
                add(k, "W1", run_near[r], run_ext3[r], hi3 - lo3, (hi3 + lo3) / 2)
            if w2_on:
                near_f = run_near[-1]
                tp_f = near_f - p["tp_profondeur"] * (near_f - far)
                for k in [b3 - 1] + list(range(a4, b4 - 1)):           # dernière bougie de C4 exclue : expiration (A.7.1)
                    if p["consommer_si_gap_touche"] and k >= a4:
                        touched = (l[a4:k + 1].min() <= tp_f) if s_f > 0 else (h[a4:k + 1].max() >= tp_f)
                        if touched:
                            break
                    if p["w2_flip_requis"] and k >= a4:
                        o4 = o[a4]
                        manip = (h[a4:k + 1].max() > o4) if d < 0 else (l[a4:k + 1].min() < o4)
                        if not (manip and d * (c[k] - o4) > 0):
                            continue
                    add(k, "W2", near_f, run_ext3[-1], h3 - l3, (h3 + l3) / 2)
    events.sort(key=lambda e: (e["k"], e["j"]))
    return events


# ----------------------------------------------------------------------------------------------- stops
def stops(p, ev, e, why=None):
    """Renvoie (sl, tp, R) ou None si le trade est rejeté (pseudocode §6.2). `why` (Counter) reçoit la raison."""
    def rej(reason):
        if why is not None:
            why[reason] += 1
        return None

    d, b = ev["dir"], p["stop_buffer_ticks"] * TICK
    mode = p["stop_mode"]
    if mode == "TP_FIRST":
        tp = ev["tp_level"]
        R = d * (tp - e)
        sl = e - d * R
        if R <= 0:
            return rej("objectif_deja_depasse")
        if d * (ev["inv"] - sl) < b:
            return rej("stop_plus_serre_que_structure")
    elif mode == "STRUCTURE":
        sl = ev["inv"] - d * b
        R = d * (e - sl)
        tp = e + d * R
        if R <= 0:
            return rej("risque_nul")
        if d * (tp - ev["near"]) < 0:
            return rej("1R_n_atteint_pas_le_gap")
    elif mode == "C3_EXTREME":
        sl = ev["ext3"] - ev["dir"] * b          # ext3 est du côté opposé au trade : stop au-delà
        R = d * (e - sl)
        tp = e + d * R
        if R <= 0:
            return rej("risque_nul")
    else:
        raise ValueError(mode)
    sl, tp = round_tick(sl), round_tick(tp)
    R = d * (e - sl)
    if R <= 0:
        return rej("risque_nul")
    if d * (tp - e) < p["distance_tp_min_points"]:
        return rej("objectif_trop_proche")
    return sl, tp, R


def round_tick(x):
    return round(x / TICK) * TICK


# ----------------------------------------------------------------------------------------------- passe 2
def simulate(ltf, events, p):
    o, h, l, c = ltf["o"], ltf["h"], ltf["l"], ltf["c"]
    t_open, t_close = ltf["t_open"], ltf["t_close"]
    N = len(c)
    slip = p["slippage_ticks_marche_et_stop"] * TICK
    through = p["limite_trade_through_ticks"] * TICK
    comm_pts = p["commission_aller_retour_usd"] / POINT_VALUE
    be = p["be_a_R"]
    free_from = 0
    per_day = Counter()
    why = Counter()
    trades = []

    for ev in events:
        k = ev["k"]
        if k < free_from or k + 1 >= N:
            why["position_ou_ordre_en_cours"] += 1
            continue
        day = (t_close[k] + 360) // 1440                               # journée CME (18:00 ET)
        if per_day[day] >= p["max_trades_par_jour"]:
            why["plafond_journalier"] += 1
            continue
        d = ev["dir"]
        limit = p["type_ordre"] == "limite_zone" or ev["big_range"]
        if not limit:
            f = k + 1
            e = o[f] + d * slip
            st = stops(p, ev, e, why)
            if st is None:
                continue
            limit_fill_bar = False
        else:
            price = round_tick(ev["mid3"] if ev["big_range"] else ev["zone"])
            st = stops(p, ev, price, why)
            if st is None:
                continue
            f = None
            for b in range(k + 1, min(ev["expire"], N - 1) + 1):
                if (d > 0 and l[b] <= price - through) or (d < 0 and h[b] >= price + through):
                    f = b
                    break
            if f is None:
                free_from = ev["expire"] + 1                          # l'ordre en attente bloquait le compte
                why["limite_non_remplie"] += 1
                continue
            e = price
            limit_fill_bar = True
        sl, tp, R = st
        if t_open[f] >= ev["forced_t"]:
            why["entree_apres_sortie_forcee"] += 1
            continue                                                    # l'entrée tomberait après la sortie forcée
        sl0 = sl
        exit_b, exit_px, reason = None, None, None
        for b in range(f, N):
            if t_open[b] >= ev["forced_t"]:
                exit_b, exit_px, reason = b - 1, c[b - 1] - d * slip, "temps"
                break
            if d > 0:
                if o[b] <= sl and not (b == f and limit_fill_bar):
                    exit_b, exit_px, reason = b, o[b] - slip, "SL"
                    break
                hit_sl, hit_tp = l[b] <= sl, h[b] >= tp + through
            else:
                if o[b] >= sl and not (b == f and limit_fill_bar):
                    exit_b, exit_px, reason = b, o[b] + slip, "SL"
                    break
                hit_sl, hit_tp = h[b] >= sl, l[b] <= tp - through
            if b == f and limit_fill_bar:
                hit_tp = False
            if hit_sl:
                exit_b, exit_px, reason = b, sl - d * slip, ("BE" if sl != sl0 else "SL")
                break
            if hit_tp:
                exit_b, exit_px, reason = b, tp, "TP"
                break
            if be is not None and sl == sl0:
                mfe = (h[b] - e) if d > 0 else (e - l[b])
                if mfe >= be * R:
                    sl = e
            if t_close[b] >= ev["forced_t"]:
                exit_b, exit_px, reason = b, c[b] - d * slip, "temps"
                break
        if exit_b is None:
            exit_b, exit_px, reason = N - 1, c[N - 1], "fin_donnees"
        pnl = d * (exit_px - e) - comm_pts
        per_day[(t_close[f] + 360) // 1440] += 1
        trades.append({
            "t_signal": t_close[k], "t_entree": t_open[f], "t_sortie": t_close[exit_b], "dir": d,
            "entree": e, "sl": sl0, "tp": tp, "risque_pts": R, "sortie": exit_px, "raison": reason,
            "pnl_pts": pnl, "R": pnl / R, "usd": pnl * POINT_VALUE, "fenetre": ev["window"], "modele": ev["model"],
            "type": "limite" if limit else "marche", "gap_pts": ev["gap"], "rng2": ev["rng2"],
            "body2_atr": ev["body2_atr"], "sweep_c2": ev["sweep_c2"], "duree_min": int(t_close[exit_b] - t_open[f]),
        })
        free_from = exit_b
    df = pd.DataFrame(trades)
    df.attrs["rejets"] = dict(why)
    if len(df):
        for col in ("t_signal", "t_entree", "t_sortie"):
            df[col] = bars.minutes_to_ts(df[col].to_numpy())
    return df


def run(df1m, params=None, htf=15, cache=None):
    """Backtest complet sur un DataFrame 1 min. `cache` (dict) évite de ré-agréger les bougies."""
    p = resolve(params or default_params(), htf)
    key = (htf, p["ltf_minutes"])
    if cache is not None and key in cache:
        ltf, H = cache[key]
    else:
        ltf, H = prepare(df1m, htf, p["ltf_minutes"])
        if cache is not None:
            cache[key] = (ltf, H)
    events = find_events(ltf, H, p)
    return simulate(ltf, events, p), events
