#!/usr/bin/env python3
"""Transforme les citations en liens horodatés cliquables (en place, idempotent).

Syntaxe dans les fichiers markdown :
  [[0:01:58]]               -> lien vers la vidéo de la fiche (champ `video_id:` en tête de fichier)
  [[Tea-SeT3-OU 0:01:58]]   -> lien vers une vidéo précise (fichiers de synthèse)

  python3 scripts/linkify.py notes/*.md strategy/*.md
"""
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"\[\[(?:([A-Za-z0-9_-]{11}) )?(\d+):(\d{2}):(\d{2})\]\]")
VID = re.compile(r"^video_id:\s*([A-Za-z0-9_-]{11})\s*$", re.M)


def convert(text):
    m = VID.search(text)
    default = m.group(1) if m else None

    def repl(t):
        vid = t.group(1) or default
        h, mi, s = int(t.group(2)), int(t.group(3)), int(t.group(4))
        label = f"{h}:{mi:02d}:{s:02d}"
        if not vid:
            raise ValueError(f"citation sans vidéo et pas de video_id: {t.group(0)}")
        if t.group(1):
            label = f"{vid} @ {label}"
        return f"[{label}](https://www.youtube.com/watch?v={vid}&t={h * 3600 + mi * 60 + s}s)"

    return TOKEN.sub(repl, text)


def main():
    for p in map(Path, sys.argv[1:]):
        old = p.read_text(encoding="utf-8")
        new = convert(old)
        if new != old:
            p.write_text(new, encoding="utf-8")
            print(f"[linkify] {p}")


if __name__ == "__main__":
    main()
