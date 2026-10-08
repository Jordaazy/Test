"""Tests du moteur sur des scénarios construits à la main (règles de strategy/regles.md) et sur des
propriétés générales (symétrie long/short, absence de lookahead)."""
import numpy as np
import pandas as pd
import pytest

from backtest import engine

# ---------------------------------------------------------------------------------------------- scénario
# FVG baissier 15 min (C1 low 100, C3 high 95 -> gap [95, 100]) ; C2 = displacement baissier ;
# C3 balaie le low de C2 (80 -> 78) puis réintègre ; IFVG 1 min inversé à 10:41 (W1, 3 min avant la clôture).
C1 = [(105, 110, 104, 106)] + [(106, 107, 100, 104)] + [(104, 106, 103, 105)] * 13
C2 = [(99, 99.5, 97, 97.5), (97.5, 98, 93, 93.5), (93.5, 94, 89, 89.5), (89.5, 90, 86, 86.5),
      (86.5, 87, 83, 83.5)] + [(83.5, 84, 81, 81.5)] * 9 + [(81.5, 82, 80, 82)]
C3 = [
    (82, 95, 81.5, 83),        # 10:30  pic : high de C3 = 95 (bord proche du gap)
    (83, 80.5, 78, 78.5),      # 10:31  sweep sous le low de C2 (80)
    (78.5, 79, 78.25, 78.75),  # 10:32
    (79, 83, 79, 82.5),        # 10:33
    (82.5, 84, 82, 83.5),      # 10:34
    (83.5, 84.5, 83, 84),      # 10:35
    (84, 85, 83.5, 84.5),      # 10:36  b1 du FVG 1 min baissier (low 83.5)
    (84.5, 84.5, 81, 81.25),   # 10:37  b2
    (81.25, 82.5, 80.5, 81),   # 10:38  b3 (high 82.5 < 83.5) -> FVG [82.5, 83.5]
    (81, 82, 80.75, 81.5),     # 10:39
    (81.5, 83, 81.25, 82.75),  # 10:40
    (82.75, 86, 82.5, 85.5),   # 10:41  clôture 85.5 > 83.5 : IFVG -> signal (clôture 10:42, reste 3 min)
    (85.5, 86.5, 85.25, 86),   # 10:42  entrée à l'ouverture 85.5 + 1 tick
    (86, 87, 85.5, 86.5),      # 10:43
    (86.5, 87.5, 86, 87),      # 10:44  clôture de C3 = 87 > 80 : étape 2 validée
]
C4_WIN = [(87, 89, 86.5, 88.5), (88.5, 92, 88, 91.5), (91.5, 95.5, 91, 95.25)] + [(95.25, 96, 95, 95.5)] * 12
C4_LOSS = [(87, 87.5, 82, 82.5), (82.5, 83, 76, 76.25)] + [(76.25, 77, 75, 76)] * 13


def frame(rows, start="2026-05-06 10:00"):
    """Un 1 min par ligne (o, h, l, c), à partir de `start` (heure de New York)."""
    ts = pd.date_range(start, periods=len(rows), freq="1min", tz="America/New_York")
    a = np.array(rows, dtype=float)
    # garantit h >= max(o, c) et l <= min(o, c), y compris pour les lignes écrites à la main
    h = np.maximum(a[:, 1], np.maximum(a[:, 0], a[:, 3]))
    l = np.minimum(a[:, 2], np.minimum(a[:, 0], a[:, 3]))
    return pd.DataFrame({"ts": ts, "o": a[:, 0], "h": h, "l": l, "c": a[:, 3], "v": 100.0})


def params(**kw):
    p = engine.default_params()
    p.update({"modeles": ["IFVG"], "session_et": ["00:00", "23:59"]})
    p.update(kw)
    return p


def mirror(df):
    return df.assign(o=-df.o, h=-df.l, l=-df.h, c=-df.c)


# ---------------------------------------------------------------------------------------------- scénarios
def test_long_gagnant_w1():
    trades, events = engine.run(frame(C1 + C2 + C3 + C4_WIN), params())
    assert len(trades) == 1
    t = trades.iloc[0]
    assert t["dir"] == 1 and t["fenetre"] == "W1" and t["modele"] == "IFVG"
    assert t["t_entree"] == pd.Timestamp("2026-05-06 10:42")
    assert t["entree"] == pytest.approx(85.75)            # ouverture 85.5 + 1 tick de slippage
    assert t["tp"] == pytest.approx(95.0)                  # bord proche du gap = high de C3
    assert t["sl"] == pytest.approx(76.5)                  # 1:1 depuis l'objectif (TP_FIRST)
    assert t["raison"] == "TP"
    assert t["R"] == pytest.approx((95 - 85.75 - 0.225) / 9.25)


def test_long_perdant_sl():
    trades, _ = engine.run(frame(C1 + C2 + C3 + C4_LOSS), params())
    t = trades.iloc[0]
    assert t["raison"] == "SL"
    assert t["sortie"] == pytest.approx(76.5 - 0.25)       # stop + 1 tick de slippage
    assert t["R"] == pytest.approx((76.25 - 85.75 - 0.225) / 9.25)


def test_filtre_session():
    trades, _ = engine.run(frame(C1 + C2 + C3 + C4_WIN), params(session_et=["11:00", "16:00"]))
    assert len(trades) == 0


def test_w1_desactive_donne_entree_w2_ou_rien():
    trades, _ = engine.run(frame(C1 + C2 + C3 + C4_WIN), params(w1_actif=False))
    assert all(trades["fenetre"] == "W2") if len(trades) else True


def test_c3_cloture_hors_de_c2_annule_w2():
    # C3 clôture sous le low de C2 (80) : pas de setup armé, donc aucune entrée W2
    c3 = C3[:-1] + [(86.5, 87, 79, 79.5)]
    trades, events = engine.run(frame(C1 + C2 + c3 + C4_WIN), params(w1_actif=False))
    assert len(trades) == 0 and not [e for e in events if e["window"] == "W2"]


def test_stop_plus_serre_que_la_structure_rejete():
    # Sweep plus profond (76) : le stop à 1:1 depuis l'objectif (76,5) serait AU-DESSUS du plus bas de la
    # structure -> rejeté en TP_FIRST ; en mode STRUCTURE le stop passe sous 76 et le trade est pris.
    c3 = list(C3)
    c3[1] = (83, 80.5, 76, 76.5)
    df = frame(C1 + C2 + c3 + C4_WIN)
    assert len(engine.run(df, params())[0]) == 0
    t = engine.run(df, params(stop_mode="STRUCTURE"))[0].iloc[0]
    assert t["sl"] == pytest.approx(76 - 0.5)              # invalidation - 2 ticks
    assert t["tp"] == pytest.approx(85.75 + (85.75 - 75.5))


def test_miroir_short_identique():
    df = frame(C1 + C2 + C3 + C4_WIN)
    long_t, _ = engine.run(df, params())
    short_t, _ = engine.run(mirror(df), params())
    assert len(short_t) == 1 and short_t.iloc[0]["dir"] == -1
    assert short_t.iloc[0]["R"] == pytest.approx(long_t.iloc[0]["R"])


def test_un_trade_par_jour():
    day = C1 + C2 + C3 + C4_WIN
    df = pd.concat([frame(day, "2026-05-06 10:00"), frame(day, "2026-05-06 13:00")], ignore_index=True)
    assert len(engine.run(df, params())[0]) == 1
    assert len(engine.run(df, params(max_trades_par_jour=2))[0]) == 2


# ---------------------------------------------------------------------------------------------- propriétés
def random_walk(n=6000, seed=0):
    rng = np.random.default_rng(seed)
    steps = rng.standard_t(4, size=n) * 2.0
    c = 20000 + np.round(np.cumsum(steps) / 0.25) * 0.25
    o = np.r_[c[0], c[:-1]]
    wick = np.round(np.abs(rng.normal(0, 1.5, size=(2, n))) / 0.25) * 0.25
    h = np.maximum(o, c) + wick[0]
    l = np.minimum(o, c) - wick[1]
    ts = pd.date_range("2026-03-02 09:30", periods=n, freq="1min", tz="America/New_York")
    return pd.DataFrame({"ts": ts, "o": o, "h": h, "l": l, "c": c, "v": 1.0})


@pytest.mark.parametrize("mode", ["TP_FIRST", "STRUCTURE", "C3_EXTREME"])
def test_symetrie_sur_marche_aleatoire(mode):
    df = random_walk()
    p = params(modeles=["IFVG", "CISD"], stop_mode=mode, max_trades_par_jour=99)
    a, _ = engine.run(df, p)
    b, _ = engine.run(mirror(df), p)
    assert len(a) == len(b) > 0
    assert np.allclose(np.sort(a["R"].to_numpy()), np.sort(b["R"].to_numpy()))


def test_pas_de_lookahead():
    df = random_walk(seed=1)
    p = params(modeles=["IFVG", "CISD", "OB", "CISD_OPEN"])
    _, full = engine.run(df, p)
    cut = len(df) // 2
    _, part = engine.run(df.iloc[:cut], p)
    # un événement dont la bougie de signal est bien avant la coupure doit exister à l'identique
    limit = cut - 2 * 15 - 1
    keep = lambda evs: {(e["k"], e["s_f"], e["window"], e["model"], round(e["inv"], 2)) for e in evs if e["k"] < limit}
    assert keep(full) == keep(part)
