"""Statistiques d'un ensemble de trades (colonne R = résultat net en multiples du risque initial)."""
import numpy as np
import pandas as pd

SESSIONS = [("Asie", 18 * 60, 26 * 60), ("Londres", 2 * 60, 8 * 60 + 30), ("NY matin", 8 * 60 + 30, 12 * 60),
            ("NY après-midi", 12 * 60, 16 * 60), ("Hors séance", 16 * 60, 18 * 60)]
JOURS = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"]


def session_of(ts):
    m = ts.dt.hour * 60 + ts.dt.minute
    out = pd.Series("?", index=ts.index)
    for name, a, b in SESSIONS:
        mm = np.where(m < 18 * 60, m + 24 * 60, m) if name == "Asie" else m
        out[(mm >= a) & (mm < b)] = name
    return out


def max_drawdown(r):
    eq = np.cumsum(np.r_[0.0, r])
    return float((np.maximum.accumulate(eq) - eq).max())


def max_streak(r, losing=True):
    best = cur = 0
    for x in r:
        cur = cur + 1 if ((x < 0) if losing else (x > 0)) else 0
        best = max(best, cur)
    return best


def summary(tr, months=None):
    """Indicateurs principaux. `months` = durée de la période (pour la fréquence)."""
    if len(tr) == 0:
        return {"trades": 0}
    r = tr["R"].to_numpy()
    wins, losses = r[r > 0], r[r < 0]
    n = len(r)
    sd = r.std(ddof=1) if n > 1 else np.nan
    out = {
        "trades": n,
        "trades_par_mois": round(n / months, 1) if months else None,
        "winrate": round(float((r > 0).mean()), 3),
        "R_moyen (expectancy)": round(float(r.mean()), 3),
        "R_median": round(float(np.median(r)), 3),
        "t_stat": round(float(r.mean() / (sd / np.sqrt(n))), 2) if n > 2 and sd > 0 else None,
        "R_total": round(float(r.sum()), 1),
        "profit_factor": round(float(wins.sum() / -losses.sum()), 2) if len(losses) and losses.sum() < 0 else None,
        "gain_moyen_R": round(float(wins.mean()), 3) if len(wins) else None,
        "perte_moyenne_R": round(float(losses.mean()), 3) if len(losses) else None,
        "drawdown_max_R": round(max_drawdown(r), 1),
        "pertes_consecutives_max": max_streak(r),
        "sorties_TP_SL_temps": "/".join(str(int((tr["raison"] == x).sum())) for x in ("TP", "SL", "temps")),
        "risque_moyen_pts": round(float(tr["risque_pts"].mean()), 1),
        "duree_mediane_min": int(tr["duree_min"].median()),
        "usd_par_contrat": int(tr["usd"].sum()),
    }
    return out


def bootstrap(tr, n_iter=2000, seed=0):
    """Intervalle à 95 % de l'expectancy et distribution du drawdown / de la série de pertes
    si l'ordre des trades avait été différent (rééchantillonnage avec remise)."""
    r = tr["R"].to_numpy()
    if len(r) < 10:
        return {}
    rng = np.random.default_rng(seed)
    means, dds, streaks = [], [], []
    for _ in range(n_iter):
        s = rng.choice(r, size=len(r), replace=True)
        means.append(s.mean())
        dds.append(max_drawdown(s))
        streaks.append(max_streak(s))
    return {
        "expectancy_IC95": [round(float(np.percentile(means, 2.5)), 3), round(float(np.percentile(means, 97.5)), 3)],
        "P(expectancy<=0)": round(float(np.mean(np.array(means) <= 0)), 3),
        "drawdown_R_p50_p95": [round(float(np.percentile(dds, 50)), 1), round(float(np.percentile(dds, 95)), 1)],
        "pertes_consecutives_p95": int(np.percentile(streaks, 95)),
    }


def breakdown(tr, by):
    """Tableau par catégorie : trades, winrate, R moyen, R total."""
    if len(tr) == 0:
        return pd.DataFrame()
    t = tr.copy()
    if by == "heure":
        key = t["t_entree"].dt.hour
    elif by == "jour":
        key = t["t_entree"].dt.dayofweek.map(dict(enumerate(JOURS)))
    elif by == "session":
        key = session_of(t["t_entree"])
    elif by == "mois":
        key = t["t_entree"].dt.strftime("%Y-%m")
    else:
        key = t[by]
    g = t.groupby(key)["R"]
    return pd.DataFrame({"trades": g.size(), "winrate": g.apply(lambda x: (x > 0).mean()).round(3),
                         "R_moyen": g.mean().round(3), "R_total": g.sum().round(1)})
