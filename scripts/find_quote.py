#!/usr/bin/env python3
"""Retrouve le timestamp exact d'une citation dans les transcriptions (segments fins).

  python3 scripts/find_quote.py "fails to close above the second candle"        # toutes les vidéos
  python3 scripts/find_quote.py "one trade a day" --video 6jM0S5_Um9M
  python3 scripts/find_quote.py "9:00 a.m. candle" --context 2

La recherche ignore la casse et la ponctuation, et tolère qu'une phrase soit coupée entre deux segments.
"""
import argparse
import json
import re
from pathlib import Path

TJSON = Path(__file__).resolve().parent.parent / "data" / "transcripts" / "json"


def norm(t):
    return re.sub(r"[^a-z0-9$%:]+", " ", t.lower()).strip()


def hms(sec):
    s = int(sec)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--video", default=None)
    ap.add_argument("--context", type=int, default=1, help="segments affichés avant/après")
    args = ap.parse_args()
    q = norm(args.query)
    for path in sorted(TJSON.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if args.video and data["video_id"] != args.video:
            continue
        segs = data["segments"]
        # Texte concaténé + position de début de chaque segment, pour les phrases à cheval.
        text, starts = "", []
        for s in segs:
            starts.append(len(text))
            text += norm(s["text"]) + " "
        for m in re.finditer(re.escape(q), text):
            i = max(k for k, st in enumerate(starts) if st <= m.start())
            lo, hi = max(0, i - args.context), min(len(segs), i + args.context + 1)
            excerpt = " ".join(s["text"] for s in segs[lo:hi])
            t = int(segs[i]["start"])
            print(f"{data['date']} {data['video_id']} @ {hms(t)}  https://www.youtube.com/watch?v={data['video_id']}&t={t}s")
            print(f"    … {excerpt} …")


if __name__ == "__main__":
    main()
