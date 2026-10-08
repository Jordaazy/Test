#!/usr/bin/env python3
"""Phase 0.3a — Pré-classement AUTOMATIQUE des vidéos (premier tri, à valider à la lecture).

Catégories : strategie (stratégie/règles), trades (trades en live/revue), mindset, hors_sujet.
Score = 3 x occurrences dans le titre + 1 x dans la description + densité dans la transcription
(occurrences pour 1000 mots). Rien de ce fichier n'est une conclusion : c'est un tri pour
prioriser la lecture. La classification finale (data/classification.csv) est faite à la main.

Sortie : data/classification_auto.csv
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_CSV = ROOT / "data" / "index.csv"
META_DIR = ROOT / "data" / "meta"
TJSON = ROOT / "data" / "transcripts" / "json"
OUT = ROOT / "data" / "classification_auto.csv"

KEYWORDS = {
    "strategie": [
        r"strat[ée]gie", r"strategy", r"r[èe]gles?", r"rules?", r"setup", r"mod[èe]le", r"model",
        r"entr[ée]e", r"entry", r"fvg", r"fair value gap", r"imbalance", r"order ?block", r"\bob\b",
        r"breaker", r"liquidit[ée]", r"liquidity", r"sweep", r"\bbos\b", r"choch", r"\bmss\b",
        r"market structure", r"structure", r"ifvg", r"inversion", r"\bsmt\b", r"pd array", r"premium",
        r"discount", r"\bote\b", r"fibonacci", r"killzone", r"kill zone", r"session", r"asia",
        r"london", r"new york", r"opening range", r"silver bullet", r"\bpo3\b", r"amd", r"biais",
        r"\bbias\b", r"timeframe", r"\bhtf\b", r"\bltf\b", r"stop ?loss", r"take ?profit", r"\brr\b",
        r"risk ?reward", r"tuto", r"tutorial", r"explication", r"expliqu", r"backtest", r"checklist",
        r"comment je", r"how i", r"step by step", r"[ée]tape",
    ],
    "trades": [
        r"\blive\b", r"en direct", r"trade[sr]?\b", r"recap", r"r[ée]cap", r"review", r"revue",
        r"journal", r"payout", r"funded", r"challenge", r"prop ?firm", r"apex", r"topstep", r"ftmo",
        r"\bp ?& ?l\b", r"\bpnl\b", r"profit", r"\+\$?\d", r"\$\d", r"aujourd'hui", r"today",
        r"semaine", r"week", r"session de trading", r"j'ai pris", r"i took",
    ],
    "mindset": [
        r"mindset", r"mental", r"psycholog", r"discipline", r"patience", r"motivation", r"[ée]motion",
        r"peur", r"fear", r"greed", r"avidit", r"confiance", r"confidence", r"conseil", r"advice",
        r"erreurs?", r"mistakes?", r"overtrad", r"revenge", r"routine", r"habitude", r"habit",
        r"process", r"processus", r"consistan", r"r[ée]gularit",
    ],
    "hors_sujet": [
        r"vlog", r"lifestyle", r"voyage", r"travel", r"unboxing", r"setup bureau", r"desk setup",
        r"q ?& ?a", r"faq", r"annonce", r"announcement", r"giveaway", r"concours", r"formation",
        r"discord", r"podcast", r"interview",
    ],
}
COMPILED = {c: [re.compile(k, re.I) for k in ks] for c, ks in KEYWORDS.items()}


def count(cat, text):
    hits = {}
    for rx in COMPILED[cat]:
        n = len(rx.findall(text))
        if n:
            hits[rx.pattern] = n
    return hits


def main():
    rows = list(csv.DictReader(INDEX_CSV.open(encoding="utf-8")))
    out = []
    for r in rows:
        vid = r["video_id"]
        meta = json.loads((META_DIR / f"{vid}.json").read_text())
        title, desc = r["title"], meta.get("description") or ""
        tpath = TJSON / f"{vid}.json"
        transcript = ""
        if tpath.exists():
            transcript = " ".join(s["text"] for s in json.loads(tpath.read_text())["segments"])
        words = max(len(transcript.split()), 1)

        scores, top_kw = {}, {}
        for cat in KEYWORDS:
            ht, hd, hx = count(cat, title), count(cat, desc), count(cat, transcript)
            scores[cat] = round(3 * sum(ht.values()) + sum(hd.values()) + 1000 * sum(hx.values()) / words, 2)
            merged = {}
            for h in (ht, hd, hx):
                for k, v in h.items():
                    merged[k] = merged.get(k, 0) + v
            top_kw[cat] = ", ".join(f"{k}:{v}" for k, v in sorted(merged.items(), key=lambda x: -x[1])[:6])
        best = max(scores, key=scores.get)
        if r["type"] == "short" or float(r["duration_s"] or 0) < 90:
            note = "short/très court"
        elif not transcript:
            note = "pas de transcription"
        else:
            note = ""
        out.append({
            "video_id": vid, "upload_date": r["upload_date"], "title": title, "duration": r["duration"],
            "type": r["type"], "auto_category": best if scores[best] > 0 else "indetermine",
            **{f"score_{c}": scores[c] for c in KEYWORDS},
            **{f"kw_{c}": top_kw[c] for c in KEYWORDS},
            "note": note,
        })
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter(o["auto_category"] for o in out))


if __name__ == "__main__":
    main()
