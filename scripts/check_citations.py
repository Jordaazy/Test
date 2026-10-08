#!/usr/bin/env python3
"""Vérifie les citations des fiches : chaque « citation » suivie d'un timestamp [[H:MM:SS]] doit
se retrouver dans la transcription autour de ce timestamp (fenêtre -40 s / +90 s).

  python3 scripts/check_citations.py notes/*.md strategy/*.md

Fonctionne avant et après scripts/linkify.py.
Sortie : une ligne par citation introuvable ; code de retour 1 s'il y en a.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TJSON = ROOT / "data" / "transcripts" / "json"
# Deux syntaxes acceptées : [[ID H:MM:SS]] (source) et [ID @ H:MM:SS](https://www.youtube.com/watch?v=ID&t=Ns) (après linkify).
TOKEN = re.compile(r"\[\[(?:([A-Za-z0-9_-]{11}) )?(\d+):(\d{2}):(\d{2})\]\]"
                   r"|\[(?:[A-Za-z0-9_-]{11} @ )?(\d+):(\d{2}):(\d{2})\]\(https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})&t=\d+s\)")
QUOTE = re.compile(r"«\s*([^»]+?)\s*»")
VID = re.compile(r"^video_id:\s*([A-Za-z0-9_-]{11})\s*$", re.M)


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def load(vid, cache={}):
    if vid not in cache:
        p = TJSON / f"{vid}.json"
        cache[vid] = json.loads(p.read_text(encoding="utf-8"))["segments"] if p.exists() else None
    return cache[vid]


def window_text(segs, t, before=40, after=90):
    return norm(" ".join(s["text"] for s in segs if t - before <= s["start"] <= t + after))


def found(quote, text):
    """Chaque fragment (séparé par « … ») doit apparaître ; le texte entre [crochets] est une
    insertion éditoriale et n'est pas vérifié. Fragments de moins de 3 mots ignorés."""
    for frag in re.split(r"…|\.\.\.|\[[^\]]*\]", quote):
        words = norm(frag).split()
        if len(words) < 3:
            continue
        chunks = [" ".join(words[i:i + 4]) for i in range(0, max(1, len(words) - 3), 4)]
        if not all(c in text for c in chunks):
            return False
    return True


def main():
    bad = 0
    for path in map(Path, sys.argv[1:]):
        content = path.read_text(encoding="utf-8")
        m = VID.search(content)
        default = m.group(1) if m else None
        for n, line in enumerate(content.splitlines(), 1):
            tokens = list(TOKEN.finditer(line))
            if not tokens:
                continue
            for q in QUOTE.finditer(line):
                # Timestamps rattachés : ceux qui suivent la citation sur la même ligne.
                after = [t for t in tokens if t.start() > q.end()] or tokens
                ok = False
                for t in after[:3]:
                    if t.group(2) is not None:
                        vid, h, mi, se = t.group(1) or default, t.group(2), t.group(3), t.group(4)
                    else:
                        vid, h, mi, se = t.group(8), t.group(5), t.group(6), t.group(7)
                    segs = load(vid) if vid else None
                    if segs is None:
                        continue
                    sec = int(h) * 3600 + int(mi) * 60 + int(se)
                    if found(q.group(1), window_text(segs, sec)):
                        ok = True
                        break
                if not ok:
                    bad += 1
                    print(f"{path.name}:{n}: introuvable près de {[t.group(0) for t in after[:3]]} : « {q.group(1)} »")
    print(f"[check] {bad} citation(s) à vérifier", file=sys.stderr)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
