"""Expériences de la Phase 4 : cas de base, IS/OOS, sensibilité, grille, walk-forward, coûts.

  python3 -m backtest.run --data <nq_1m_continuous.parquet> --out results

Toutes les sorties (markdown, CSV, JSON) vont dans --out ; aucune donnée de marché brute n'y est écrite.
"""
import argparse
import copy
import itertools
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from . import engine, stats

IS_END = pd.Timestamp("2026-01-01")          # in-sample = 2025 ; out-of-sample = 2026-01 -> 2026-10


def md(df, floatfmt=3):
    """DataFrame -> tableau markdown (sans dépendance externe)."""
    if df is None or len(df) == 0:
        return "_(aucun trade)_\n"
    df = df.reset_index() if df.index.name is not None or not isinstance(df.index, pd.RangeIndex) else df
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        cells = []
        for v in row:
            if isinstance(v, float):
                cells.append("" if np.isnan(v) else f"{v:.{floatfmt}f}".rstrip("0").rstrip("."))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def months_between(a, b):
    return (b - a).days / 30.44


def split(tr):
    if len(tr) == 0:
        return tr, tr
    return tr[tr["t_entree"] < IS_END], tr[tr["t_entree"] >= IS_END]


class Lab:
    def __init__(self, df):
        self.df = df
        self.cache = {}
        self.t0, self.t1 = df["ts"].iloc[0].tz_localize(None), df["ts"].iloc[-1].tz_localize(None)
        self.m_is = months_between(self.t0, IS_END)
        self.m_oos = months_between(IS_END, self.t1)

    def run(self, p, htf=15):
        tr, ev = engine.run(self.df, p, htf=htf, cache=self.cache)
        return tr, ev

    def row(self, tr):
        a, b = split(tr)
        sa, sb = stats.summary(a, self.m_is), stats.summary(b, self.m_oos)
        return {"IS_trades": sa.get("trades", 0), "IS_winrate": sa.get("winrate"), "IS_R_moyen": sa.get("R_moyen (expectancy)"),
                "IS_PF": sa.get("profit_factor"), "IS_DD_R": sa.get("drawdown_max_R"),
                "OOS_trades": sb.get("trades", 0), "OOS_winrate": sb.get("winrate"), "OOS_R_moyen": sb.get("R_moyen (expectancy)"),
                "OOS_PF": sb.get("profit_factor"), "OOS_DD_R": sb.get("drawdown_max_R")}


# --------------------------------------------------------------------------------------------- expériences
def baseline(lab, out, report):
    base = engine.default_params()
    report.append("## 1. Version de référence (valeurs par défaut)\n")
    report.append("Paramètres : `strategy/parametres.json` (défauts). In-sample = 2025, out-of-sample = 2026-01 → 2026-10.\n")
    rows, details = [], {}
    for htf in (15, 60, 240):
        tr, ev = lab.run(base, htf)
        tr.to_csv(out / f"trades_reference_{htf}m.csv", index=False)
        a, b = split(tr)
        for name, t, m in (("complet", tr, lab.m_is + lab.m_oos), ("IS 2025", a, lab.m_is), ("OOS 2026", b, lab.m_oos)):
            s = stats.summary(t, m)
            rows.append({"HTF": f"{htf} min", "période": name, **s})
        details[htf] = (tr, ev)
    report.append(md(pd.DataFrame(rows)))

    tr, ev = details[15]
    report.append("\n### Entonnoir (15 min)\n")
    evs = pd.DataFrame(ev)
    funnel = {"signaux (événements)": len(evs),
              "dont W1": int((evs["window"] == "W1").sum()) if len(evs) else 0,
              "dont W2": int((evs["window"] == "W2").sum()) if len(evs) else 0,
              **{f"rejet : {k}": v for k, v in tr.attrs.get("rejets", {}).items()},
              "trades": len(tr)}
    report.append(md(pd.DataFrame([funnel]).T.rename(columns={0: "nombre"})))

    report.append("\n### Robustesse statistique (15 min, rééchantillonnage de l'ordre des trades)\n")
    for name, t in zip(("complet", "IS 2025", "OOS 2026"), (tr, *split(tr))):
        report.append(f"- **{name}** : `{json.dumps(stats.bootstrap(t), ensure_ascii=False)}`")
    report.append("")
    report.append("\n### 15 min — par session **et par année** (une régularité doit tenir dans les deux)\n")
    t2 = tr.assign(annee=tr["t_entree"].dt.year, session=stats.session_of(tr["t_entree"]))
    g = t2.groupby(["session", "annee"])["R"]
    report.append(md(pd.DataFrame({"trades": g.size(), "winrate": g.apply(lambda x: (x > 0).mean()).round(3),
                                   "R_moyen": g.mean().round(3)}).reset_index()))
    for col in ("modele", "dir", "fenetre"):
        g = t2.groupby([col, "annee"])["R"]
        report.append(f"\n**{col} × année**\n")
        report.append(md(pd.DataFrame({"trades": g.size(), "R_moyen": g.mean().round(3)}).reset_index()))
    for by, title in (("session", "par session"), ("heure", "par heure d'entrée (ET)"), ("jour", "par jour"),
                      ("fenetre", "par fenêtre d'entrée"), ("modele", "par modèle d'entrée"), ("dir", "par sens (1 = long)"),
                      ("raison", "par motif de sortie"), ("sweep_c2", "C3 a balayé l'extrême de C2 ?"), ("mois", "par mois")):
        report.append(f"\n### 15 min — {title}\n")
        report.append(md(stats.breakdown(tr, by)))
    return details


def sensitivity(lab, out, report, htf=15):
    """Un paramètre à la fois autour de la référence (plages `test` de parametres.json)."""
    spec = json.loads((engine.ROOT / "strategy" / "parametres.json").read_text(encoding="utf-8"))
    base = engine.default_params()
    skip = {"instrument", "htf_minutes", "rr", "commission_aller_retour_usd", "meme_bougie_sl_tp", "ancrage_4h_et"}
    rows = [{"paramètre": "(référence)", "valeur": "", **lab.row(lab.run(base, htf)[0])}]
    for g in spec["groupes"].values():
        for prm in g:
            if prm["nom"] in skip:
                continue
            for val in prm["test"]:
                p = copy.deepcopy(base)
                if isinstance(prm["default"], dict) and isinstance(val, dict):
                    p[prm["nom"]] = {**prm["default"], **val}
                else:
                    p[prm["nom"]] = val
                if p[prm["nom"]] == base[prm["nom"]]:
                    continue
                tr, _ = lab.run(p, htf)
                rows.append({"paramètre": prm["nom"], "valeur": json.dumps(val, ensure_ascii=False), **lab.row(tr)})
    df = pd.DataFrame(rows)
    df.to_csv(out / f"sensibilite_{htf}m.csv", index=False)
    report.append(f"\n## 2. Sensibilité, un paramètre à la fois ({htf} min)\n")
    report.append("Chaque ligne change **un seul** paramètre par rapport à la référence. On cherche des zones stables, pas le maximum.\n")
    report.append(md(df))
    return df


GRID = {
    "tp_profondeur": [0, 0.5, 1.0],
    "stop_mode": ["TP_FIRST", "STRUCTURE"],
    "fenetres": ["W1+W2", "W1", "W2"],
    "gap_min_points": [0.25, 2, 5],
    "distance_tp_min_points": [5, 8, 12],
}


def apply_combo(base, combo):
    p = copy.deepcopy(base)
    for k, v in combo.items():
        if k == "fenetres":
            p["w1_actif"], p["w2_actif"] = "W1" in v, "W2" in v
        elif k == "distance_tp_min_points":
            p[k] = {**base[k], "15": v}
        else:
            p[k] = v
    return p


def grid(lab, out, report, htf=15):
    base = engine.default_params()
    keys = list(GRID)
    rows, trades = [], {}
    for vals in itertools.product(*GRID.values()):
        combo = dict(zip(keys, vals))
        tr, _ = lab.run(apply_combo(base, combo), htf)
        trades[vals] = tr
        rows.append({**combo, **lab.row(tr)})
    df = pd.DataFrame(rows)
    df.to_csv(out / f"grille_{htf}m.csv", index=False)
    report.append(f"\n## 3. Grille de robustesse ({len(df)} combinaisons, {htf} min)\n")
    pos_is = (df["IS_R_moyen"] > 0).mean()
    pos_oos = (df["OOS_R_moyen"] > 0).mean()
    both = ((df["IS_R_moyen"] > 0) & (df["OOS_R_moyen"] > 0)).mean()
    corr = df[["IS_R_moyen", "OOS_R_moyen"]].corr().iloc[0, 1]
    report.append(f"- combinaisons à expectancy > 0 : **{pos_is:.0%} en IS**, **{pos_oos:.0%} en OOS**, {both:.0%} dans les deux ;")
    report.append(f"- corrélation IS → OOS de l'expectancy entre combinaisons : **{corr:.2f}** "
                  "(proche de 0 ou négative = le classement IS ne prédit rien).\n")
    for k in keys:
        g = df.groupby(k)[["IS_R_moyen", "OOS_R_moyen", "IS_trades", "OOS_trades"]].mean().round(3)
        report.append(f"\n**Moyenne sur la grille par `{k}`**\n")
        report.append(md(g))
    top = df.sort_values("IS_R_moyen", ascending=False).head(10)
    report.append("\n**Les 10 meilleures combinaisons en IS et leur résultat OOS** (pour mesurer la dégradation)\n")
    report.append(md(top))
    return df, trades


def walk_forward(lab, out, report, grid_df, grid_trades, htf=15):
    """Fenêtres glissantes : 6 mois d'entraînement, 3 mois de test. Sélection robuste : la combinaison dont
    la moyenne avec ses voisines (un pas sur un paramètre) est la meilleure en entraînement (>= 20 trades)."""
    keys = list(GRID)
    starts = pd.date_range("2025-01-01", "2026-07-01", freq="3MS")
    folds = [(s, s + pd.DateOffset(months=6), s + pd.DateOffset(months=9)) for s in starts
             if s + pd.DateOffset(months=6) < lab.t1]
    combos = list(grid_trades)

    def exp_in(tr, a, b):
        t = tr[(tr["t_entree"] >= a) & (tr["t_entree"] < b)] if len(tr) else tr
        return (t["R"].mean() if len(t) else np.nan), len(t), t

    def neighbours(v):
        res = [v]
        for i, k in enumerate(keys):
            opts = GRID[k]
            idx = opts.index(v[i])
            for dj in (-1, 1):
                if 0 <= idx + dj < len(opts):
                    w = list(v)
                    w[i] = opts[idx + dj]
                    res.append(tuple(w))
        return res

    rows, oos_parts, ref_parts = [], [], []
    ref_key = (0, "TP_FIRST", "W1+W2", 0.25, 8)
    for a, b, c in folds:
        train = {v: exp_in(grid_trades[v], a, b) for v in combos}
        score = {}
        for v in combos:
            if train[v][1] < 20:
                continue
            vals = [train[w][0] for w in neighbours(v) if w in train and not np.isnan(train[w][0])]
            score[v] = np.mean(vals)
        if not score:
            continue
        best = max(score, key=score.get)
        m_test, n_test, t_test = exp_in(grid_trades[best], b, c)
        m_ref, n_ref, t_ref = exp_in(grid_trades[ref_key], b, c)
        oos_parts.append(t_test)
        ref_parts.append(t_ref)
        rows.append({"entraînement": f"{a:%Y-%m} → {b:%Y-%m}", "test": f"{b:%Y-%m} → {c:%Y-%m}",
                     "choix": " / ".join(map(str, best)), "score_entr.": round(score[best], 3),
                     "R_moyen_entr.": round(train[best][0], 3), "test_trades": n_test,
                     "test_R_moyen": round(m_test, 3) if n_test else None,
                     "référence_test_trades": n_ref, "référence_test_R_moyen": round(m_ref, 3) if n_ref else None})
    df = pd.DataFrame(rows)
    df.to_csv(out / f"walkforward_{htf}m.csv", index=False)
    report.append(f"\n## 4. Walk-forward ({htf} min) — 6 mois d'entraînement, 3 mois de test\n")
    report.append("Choix = " + " / ".join(keys) + " ; sélection lissée par les voisins pour éviter de choisir un pic isolé.\n")
    report.append(md(df))
    wf = pd.concat(oos_parts) if oos_parts else pd.DataFrame()
    rf = pd.concat(ref_parts) if ref_parts else pd.DataFrame()
    m = sum(3 for _ in rows)
    report.append("\n**Tous les trimestres de test mis bout à bout**\n")
    report.append(md(pd.DataFrame([{"version": "walk-forward (paramètres choisis)", **stats.summary(wf, m)},
                                   {"version": "référence fixe", **stats.summary(rf, m)}])))
    return df


def costs(lab, out, report, htf=15):
    base = engine.default_params()
    rows = []
    for slip in (0, 1, 2):
        for comm in (0.0, 4.5, 6.0):
            p = copy.deepcopy(base)
            p["slippage_ticks_marche_et_stop"] = slip
            p["commission_aller_retour_usd"] = comm
            rows.append({"slippage_ticks": slip, "commission_usd": comm, **lab.row(lab.run(p, htf)[0])})
    report.append(f"\n## 5. Sensibilité aux coûts ({htf} min)\n")
    report.append(md(pd.DataFrame(rows)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    t = time.time()
    lab = Lab(pd.read_parquet(args.data))
    report = ["# Résultats du backtest — modèle A (unfilled FVG)", "",
              f"Données : NQ continu 1 min (Databento GLBX.MDP3), {lab.t0:%Y-%m-%d} → {lab.t1:%Y-%m-%d}, "
              "front month au volume de la veille, ajustement par différence. "
              "Coûts par défaut : 4,50 $ aller-retour + 1 tick de slippage (entrée marché, stop, sortie forcée). "
              "R = résultat net ÷ risque initial.", "",
              "> **Lecture de la séparation IS / OOS.** Les valeurs par défaut ont été fixées à partir des vidéos, "
              "*avant* de voir les données : pour la version de référence, 2025 comme 2026 sont hors échantillon. "
              "En revanche, l'auteur a formalisé ses règles en 2026 en montrant des trades de 2026 : cette période "
              "peut être favorable à ses règles par construction (biais de sélection des exemples). "
              "La séparation IS 2025 / OOS 2026 sert surtout à juger l'optimisation (grille, walk-forward).", ""]
    baseline(lab, out, report)
    sensitivity(lab, out, report, 15)
    gdf, gtr = grid(lab, out, report, 15)
    walk_forward(lab, out, report, gdf, gtr, 15)
    costs(lab, out, report, 15)
    report.append(f"\n_Calcul : {time.time() - t:.0f} s._\n")
    (out / "rapport_backtest.md").write_text("\n".join(report), encoding="utf-8")
    print(f"[run] rapport -> {out / 'rapport_backtest.md'} ({time.time() - t:.0f} s)")


if __name__ == "__main__":
    main()
