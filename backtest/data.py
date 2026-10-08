"""Préparation des données Databento (GLBX.MDP3, OHLCV-1m) en une série NQ continue.

- garde les contrats NQ « outright » (NQH5, NQM5, …) : ni MNQ, ni spreads calendaires ;
- front = contrat le plus échangé la **veille** (pas de lookahead), sans retour vers une échéance antérieure ;
- roll au début d'une journée de trading CME (18:00 ET) ;
- ajustement par différence (« Panama ») : les écarts de prix intra-journée sont exacts, seul le niveau
  absolu des périodes anciennes est décalé. Colonne `contract` = contrat réellement utilisé.

Usage :
  python3 -m backtest.data <csv_databento> <sortie.parquet>
"""
import re
import sys

import pandas as pd

TZ = "America/New_York"
OUTRIGHT = re.compile(r"^NQ[HMUZ]\d$")
MONTHS = {"H": 3, "M": 6, "U": 9, "Z": 12}


def expiry_key(sym, ref_year):
    """Ordre chronologique d'une échéance NQ (chiffre de l'année sur une décennie)."""
    m, y = sym[2], int(sym[3])
    year = (ref_year // 10) * 10 + y
    if year < ref_year - 2:
        year += 10
    return year * 100 + MONTHS[m]


def trading_day(ts_et):
    """Journée CME : une barre de 18:00 ET appartient au jour suivant."""
    return (ts_et + pd.Timedelta(hours=6)).dt.date


def load_raw(csv_path):
    df = pd.read_csv(csv_path, usecols=["ts_event", "open", "high", "low", "close", "volume", "symbol"])
    df = df[df["symbol"].str.match(OUTRIGHT)].copy()
    df["ts"] = pd.to_datetime(df["ts_event"], utc=True).dt.tz_convert(TZ)
    df = df.drop(columns="ts_event").rename(columns={"open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
    df["day"] = trading_day(df["ts"])
    return df


def choose_fronts(df):
    vol = df.groupby(["day", "symbol"])["v"].sum().unstack(fill_value=0)
    days = list(vol.index)
    ref_year = days[0].year
    fronts, current = {}, None
    for i, d in enumerate(days):
        basis = vol.iloc[i - 1] if i > 0 else vol.iloc[i]
        best = basis.idxmax()
        if current is None or expiry_key(best, ref_year) > expiry_key(current, ref_year):
            current = best                      # jamais de retour vers une échéance plus ancienne
        fronts[d] = current
    return fronts


def build_continuous(df):
    fronts = choose_fronts(df)
    df["front"] = df["day"].map(fronts)
    cont = df[df["symbol"] == df["front"]].sort_values("ts").reset_index(drop=True)
    cont = cont.rename(columns={"symbol": "contract"}).drop(columns="front")

    # Ajustement par différence, en remontant le temps.
    cont["adj"] = 0.0
    rolls = []
    days = sorted(fronts)
    for prev_d, d in zip(days, days[1:]):
        a, b = fronts[prev_d], fronts[d]
        if a == b:
            continue
        # dernière minute commune aux deux contrats pendant la journée qui précède le roll
        pa = df[(df["symbol"] == a) & (df["day"] == prev_d)].set_index("ts")["c"]
        pb = df[(df["symbol"] == b) & (df["day"] == prev_d)].set_index("ts")["c"]
        common = pa.index.intersection(pb.index)
        if len(common) == 0:
            raise ValueError(f"pas de minute commune {a}/{b} le {prev_d}")
        t = common.max()
        offset = float(pb[t] - pa[t])
        rolls.append({"jour_roll": d, "de": a, "vers": b, "minute_ref": t, "offset_points": offset})
        cont.loc[cont["day"] < d, "adj"] += offset
    for col in "ohlc":
        cont[col] = cont[col] + cont["adj"]
    return cont[["ts", "day", "o", "h", "l", "c", "v", "contract", "adj"]], pd.DataFrame(rolls)


def sanity(cont):
    per_day = cont.groupby("day").size()
    ret = cont["c"].diff().abs()
    same = cont["contract"].eq(cont["contract"].shift())
    return {
        "barres": len(cont),
        "jours": len(per_day),
        "barres_par_jour_median": int(per_day.median()),
        "debut": str(cont["ts"].iloc[0]),
        "fin": str(cont["ts"].iloc[-1]),
        "plus_grand_saut_1m_meme_contrat_pts": float(ret[same].max()),
        "prix_ohlc_incoherents": int(((cont["h"] < cont[["o", "c"]].max(axis=1)) |
                                      (cont["l"] > cont[["o", "c"]].min(axis=1))).sum()),
    }


def main():
    src, out = sys.argv[1], sys.argv[2]
    cont, rolls = build_continuous(load_raw(src))
    cont.to_parquet(out, index=False)
    print(rolls.to_string(index=False))
    for k, v in sanity(cont).items():
        print(f"{k:40s} {v}")


if __name__ == "__main__":
    main()
