"""Agrégation des bougies sur la grille d'horloge ET (pseudocode §1).

Les temps sont manipulés en **minutes d'horloge locale naïve** (int64) : une bougie de 15 min « de 10:30 »
couvre [10:30, 10:45). Les changements d'heure tombent le dimanche à 2 h, marché fermé.
"""
import numpy as np
import pandas as pd


def to_local_minutes(ts):
    """Série de Timestamps tz-aware (ET) -> minutes locales naïves depuis l'epoch (int64)."""
    naive = ts.dt.tz_localize(None)
    return (naive.astype("datetime64[ns]").astype("int64") // 60_000_000_000).to_numpy()


def minutes_to_ts(m):
    return pd.to_datetime(np.asarray(m, dtype="int64") * 60_000_000_000)


def resample(t_open, o, h, l, c, v, period, anchor_offset=0):
    """Agrège des bougies (t_open en minutes locales) sur une grille de `period` minutes.

    anchor_offset : décalage de la grille en minutes (ex. 4 h ancrées à 18:00 -> offset 6*60, car
    18:00 + 6 h = minuit). Renvoie un dict d'arrays numpy + `src_start`/`src_end` (indices des bougies
    sources de chaque bougie agrégée, end exclusif).
    """
    key = ((t_open + anchor_offset) // period) * period - anchor_offset
    # les clés sont croissantes : on repère les débuts de groupes
    starts = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    ends = np.r_[starts[1:], len(key)]
    return {
        "t_open": key[starts],
        "t_close": key[starts] + period,
        "o": o[starts],
        "h": np.maximum.reduceat(h, starts),
        "l": np.minimum.reduceat(l, starts),
        "c": c[ends - 1],
        "v": np.add.reduceat(v, starts),
        "src_start": starts,
        "src_end": ends,
    }


def from_frame(df, period=1):
    """DataFrame 1 min (backtest.data) -> dict de bougies `period` minutes."""
    t = to_local_minutes(df["ts"])
    arr = {k: df[k].to_numpy(dtype="float64") for k in "ohlcv"}
    if period == 1:
        n = len(t)
        return {"t_open": t, "t_close": t + 1, **arr, "src_start": np.arange(n), "src_end": np.arange(n) + 1}
    return resample(t, arr["o"], arr["h"], arr["l"], arr["c"], arr["v"], period)


def htf_over_ltf(ltf, htf_period, anchor_offset=0):
    """Bougies HTF construites à partir des bougies LTF (indices LTF dans src_start/src_end)."""
    return resample(ltf["t_open"], ltf["o"], ltf["h"], ltf["l"], ltf["c"], ltf["v"], htf_period, anchor_offset)


def atr(h, l, c, n=14):
    """ATR de Wilder (valeur connue à la clôture de chaque bougie)."""
    prev_c = np.r_[c[0], c[:-1]]
    tr = np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))
    out = np.empty_like(tr)
    out[0] = tr[0]
    alpha = 1.0 / n
    for i in range(1, len(tr)):
        out[i] = out[i - 1] + alpha * (tr[i] - out[i - 1])
    return out
