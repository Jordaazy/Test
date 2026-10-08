#!/usr/bin/env python3
"""Phase 0.2b — Conversion des sous-titres bruts en texte propre horodaté.

Entrée  : data/subs_raw/<id>.<lang>.(json3|vtt)  + data/meta/<id>.json + data/subs_manifest.csv
Sorties : data/transcripts/<date>_<slug>_<id>.md    (lecture humaine, paragraphes horodatés [H:MM:SS])
          data/transcripts/json/<id>.json           (segments fins {start, end, text} pour la recherche)

Gère les deux formats :
  - json3 (préféré) : un événement = un segment, pas de doublons ;
  - vtt : les sous-titres auto YouTube "roulent" (chaque ligne est répétée dans la cue suivante),
    on supprime les balises <c>/<00:00:01.000> et on déduplique.

Usage :
  python3 scripts/p0_clean.py [--para-seconds 20] [--gap 2.5]
"""
import argparse
import csv
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "meta"
RAW_DIR = ROOT / "data" / "subs_raw"
MANIFEST = ROOT / "data" / "subs_manifest.csv"
OUT_DIR = ROOT / "data" / "transcripts"

NOISE = re.compile(r"\[(musique|music|applaudissements|applause|rires|laughter|__)\]", re.I)
TAGS = re.compile(r"<[^>]+>")
TS = re.compile(r"(\d+):(\d{2}):(\d{2})[.,](\d{3})|(\d{2}):(\d{2})[.,](\d{3})")


def hms(sec):
    s = int(sec)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def slugify(text, maxlen=60):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:maxlen].rstrip("-") or "video"


def clean_text(t):
    t = html.unescape(TAGS.sub("", t))
    t = NOISE.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()


def parse_json3(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    segs = []
    for ev in data.get("events", []):
        if "segs" not in ev:
            continue
        text = clean_text("".join(s.get("utf8", "") for s in ev["segs"]))
        if not text:
            continue
        start = ev.get("tStartMs", 0) / 1000
        end = start + ev.get("dDurationMs", 0) / 1000
        segs.append({"start": round(start, 2), "end": round(end, 2), "text": text})
    return segs


def to_sec(m):
    if m.group(1) is not None:
        h, mi, s, ms = m.group(1), m.group(2), m.group(3), m.group(4)
    else:
        h, mi, s, ms = 0, m.group(5), m.group(6), m.group(7)
    return int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000


def parse_vtt(path):
    # Lecture ligne à ligne : les cues auto YouTube contiennent des lignes " " (un espace)
    # qu'un découpage sur lignes vides confondrait avec une fin de cue.
    segs, last_line, cue = [], None, None
    for raw in path.read_text(encoding="utf-8").replace("\r", "").split("\n"):
        if "-->" in raw:
            ms = list(TS.finditer(raw))
            cue = (to_sec(ms[0]), to_sec(ms[1])) if len(ms) >= 2 else None
            continue
        if cue is None:
            continue
        line = clean_text(raw)
        if not line or line == last_line:
            continue
        segs.append({"start": round(cue[0], 2), "end": round(cue[1], 2), "text": line})
        last_line = line
    return segs


def paragraphs(segs, para_seconds, gap):
    paras, cur = [], None
    for s in segs:
        if cur is None or s["start"] - cur["end"] >= gap or s["start"] - cur["start"] >= para_seconds:
            if cur:
                paras.append(cur)
            cur = {"start": s["start"], "end": s["end"], "text": [s["text"]]}
        else:
            cur["text"].append(s["text"])
            cur["end"] = max(cur["end"], s["end"])
    if cur:
        paras.append(cur)
    return paras


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--para-seconds", type=float, default=20.0)
    ap.add_argument("--gap", type=float, default=2.5)
    args = ap.parse_args()

    (OUT_DIR / "json").mkdir(parents=True, exist_ok=True)
    manifest = {r["video_id"]: r for r in csv.DictReader(MANIFEST.open(encoding="utf-8"))}
    done = 0
    for vid, row in manifest.items():
        if not row["file"]:
            continue
        path = RAW_DIR / row["file"]
        meta = json.loads((META_DIR / f"{vid}.json").read_text(encoding="utf-8"))
        segs = parse_json3(path) if path.suffix == ".json3" else parse_vtt(path)
        if not segs:
            print(f"[clean] {vid}: piste vide", file=sys.stderr)
            continue

        d = meta.get("upload_date") or "00000000"
        date = f"{d[:4]}-{d[4:6]}-{d[6:]}"
        url = f"https://www.youtube.com/watch?v={vid}"
        name = f"{date}_{slugify(meta.get('title') or vid)}_{vid}"

        (OUT_DIR / "json" / f"{vid}.json").write_text(json.dumps(
            {"video_id": vid, "title": meta.get("title"), "date": date, "url": url,
             "sub_lang": row["lang"], "sub_kind": row["kind"], "sub_note": row["note"], "segments": segs},
            ensure_ascii=False, indent=0), encoding="utf-8")

        out = [f"# {meta.get('title')}", "",
               f"- **URL** : {url}",
               f"- **Date** : {date}",
               f"- **Durée** : {hms(meta.get('duration') or 0)}",
               f"- **Sous-titres** : {row['kind']} / {row['lang']} {('(' + row['note'] + ')') if row['note'] else ''}",
               f"- **Lien horodaté** : `{url}&t=<secondes>s`", ""]
        if row["kind"] == "auto":
            out += ["> ⚠️ Sous-titres automatiques : les termes techniques (FVG, BOS, iFVG, SMT, OTE…) "
                    "peuvent être mal transcrits. Vérifier sur la vidéo avant de citer une règle.", ""]
        if meta.get("chapters"):
            out += ["## Chapitres", ""]
            out += [f"- [{hms(c['start_time'])}] {c.get('title', '')}" for c in meta["chapters"]]
            out += [""]
        out += ["## Transcription", ""]
        out += [f"[{hms(p['start'])}] {' '.join(p['text'])}" + "\n" for p in paragraphs(segs, args.para_seconds, args.gap)]
        if meta.get("description"):
            out += ["## Description de la vidéo", "", "```", meta["description"].strip(), "```", ""]
        (OUT_DIR / f"{name}.md").write_text("\n".join(out), encoding="utf-8")
        done += 1
    print(f"[clean] {done} transcriptions -> {OUT_DIR.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
