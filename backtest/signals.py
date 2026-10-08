"""Modèles d'entrée LTF (pseudocode §5).

Toute la logique est écrite pour un **long**. Pour un short, on appelle la même fonction sur les prix
négatifs (high et low échangés), puis on renie les niveaux : c'est l'exact miroir.

scan_long(...) parcourt une fenêtre de bougies et renvoie, pour chaque bougie k, le meilleur signal :
  model[k] (0 = aucun), zone[k] (prix de l'ordre limite), inv[k] (invalidation = niveau de structure).
"""
import numpy as np

IFVG, CISD, CISD_OPEN, OB = 1, 2, 3, 4
MODEL_NAMES = {IFVG: "IFVG", CISD: "CISD", CISD_OPEN: "CISD_OPEN", OB: "OB"}
NAME_TO_CODE = {v: k for k, v in MODEL_NAMES.items()}


def _swings(h, l, n, first):
    """Indices des swing highs / lows (fractal strict de n bougies de chaque côté), index >= first."""
    sh, sl = [], []
    for i in range(max(first, n), len(h) - n):
        left_h, right_h = h[i - n:i], h[i + 1:i + n + 1]
        if h[i] > left_h.max() and h[i] > right_h.max():
            sh.append(i)
        left_l, right_l = l[i - n:i], l[i + 1:i + n + 1]
        if l[i] < left_l.min() and l[i] < right_l.min():
            sl.append(i)
    return sh, sl


def scan_long(o, h, l, c, s0, n=2, ifvg_min=0.25, models=(IFVG, CISD), k_from=None):
    """Signaux long sur les bougies k >= k_from (défaut s0+1).

    Les tableaux couvrent [s0 - contexte, fin) : les bougies avant s0 ne servent que de voisines pour les
    fractals ; swings, FVG et sweeps ne sont pris qu'à partir de s0 (« within that third candle »).
    """
    N = len(c)
    model = np.zeros(N, dtype=np.int8)
    zone = np.full(N, np.nan)
    inv = np.full(N, np.nan)
    sh, sl = _swings(h, l, n, s0)
    sh_arr, sl_arr = np.array(sh, dtype=int), np.array(sl, dtype=int)

    # FVG baissiers LTF (pour l'IFVG long) : (index de formation, haut de zone)
    fvgs = []
    if IFVG in models:
        for i in range(s0 + 2, N):
            if h[i] < l[i - 2] and l[i - 2] - h[i] >= ifvg_min:
                fvgs.append([i, l[i - 2], False])        # [formé en i, top, inversé ?]

    start = s0 + 1 if k_from is None else max(k_from, s0 + 1)
    # état IFVG avant `start`
    for f in fvgs:
        if f[0] < start - 1 and np.any(c[f[0] + 1:start] > f[1]):
            f[2] = True

    for k in range(start, N):
        cands = []

        if IFVG in models:
            live = [f for f in fvgs if f[0] <= k - 1 and not f[2]]
            if live:
                F = live[-1]
                if c[k] > F[1]:
                    cands.append((IFVG, F[1], l[s0:k + 1].min()))
            for f in fvgs:
                if f[0] <= k - 1 and not f[2] and c[k] > f[1]:
                    f[2] = True

        if CISD in models or OB in models:
            known_h = sh_arr[(sh_arr + n) <= k - 1] if len(sh_arr) else sh_arr
            known_l = sl_arr[(sl_arr + n) <= k - 1] if len(sl_arr) else sl_arr
            for iH in known_h[::-1][:3]:
                lvl = h[iH]
                if c[k] <= lvl or (k - 1 > iH and c[iH + 1:k].max() > lvl):
                    continue                                    # pas une 1re clôture au-dessus de H1
                before = known_l[known_l < iH]
                if len(before) == 0:
                    continue
                iL1 = before[-1]
                if CISD in models and k - 1 > iH:
                    L2 = l[iH + 1:k].min()
                    if L2 < l[iL1]:
                        seg = np.arange(iL1, iH + 1)
                        bull = seg[c[seg] > o[seg]]
                        j = bull[-1] if len(bull) else iH
                        cands.append((CISD, h[j], L2))
                        break
                if OB in models:
                    after = known_l[(known_l > iH)]
                    if len(after) and l[after[-1]] > l[iL1]:
                        iL2 = after[-1]
                        seg = np.arange(iH, iL2 + 1)
                        bear = seg[c[seg] < o[seg]]
                        j = bear[-1] if len(bear) else iL2
                        cands.append((OB, h[j], l[iL2]))
                        break

        if CISD_OPEN in models and k - 1 >= s0:
            seg_l = l[s0:k]
            m = s0 + int(np.flatnonzero(seg_l == seg_l.min())[-1])
            e = m
            while e >= s0 and not c[e] < o[e]:
                e -= 1
            if e >= s0:
                s = e
                while s - 1 >= s0 and c[s - 1] < o[s - 1]:
                    s -= 1
                lvl = o[s]
                if c[k] > lvl and (k - 1 < m or c[m:k].max() <= lvl):
                    cands.append((CISD_OPEN, lvl, l[m]))

        if cands:
            best = max(cands, key=lambda x: x[2])               # invalidation la plus proche = risque le plus faible
            model[k], zone[k], inv[k] = best
    return model, zone, inv


def scan(direction, o, h, l, c, s0, **kw):
    """direction = +1 (long) ou -1 (short, par miroir des prix)."""
    if direction > 0:
        return scan_long(o, h, l, c, s0, **kw)
    m, z, i = scan_long(-o, -l, -h, -c, s0, **kw)
    return m, -z, -i
