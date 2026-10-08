#!/usr/bin/env python3
"""Phase 0.2a — Téléchargement des sous-titres (aucune vidéo).

Choix de la piste, par vidéo, dans cet ordre :
  1. sous-titres manuels dans la langue de la vidéo ;
  2. sous-titres manuels FR, puis EN ;
  3. sous-titres auto ORIGINAUX (reconnaissance vocale : clé "xx-orig" ou clé == langue de la vidéo), FR/EN ;
  4. à défaut, piste auto traduite FR/EN — signalée "translated" dans le manifeste (qualité faible).
Le choix est tracé dans data/subs_manifest.csv.

Usage :
  python3 scripts/p0_subs.py [--cookies cookies.txt] [--sleep 1.5] [--only ID1,ID2]
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import yt_dlp

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "meta"
RAW_DIR = ROOT / "data" / "subs_raw"
MANIFEST = ROOT / "data" / "subs_manifest.csv"
WANTED = ("fr", "en")


def base(lang):
    return lang.split("-")[0].lower()


def choose_track(meta):
    """Retourne (lang_key, kind, note) ou (None, None, raison)."""
    vlang = base(meta.get("language") or "")
    manual = meta.get("subtitles") or {}
    auto = meta.get("automatic_captions") or {}
    manual = {k: v for k, v in manual.items() if k != "live_chat"}

    # 1-2. manuels
    order = ([vlang] if vlang in WANTED else []) + [l for l in WANTED if l != vlang]
    for lang in order:
        for key in sorted(manual, key=len):
            if base(key) == lang:
                return key, "manual", ""
    # 3. auto originaux
    for key in auto:
        if key.endswith("-orig") and base(key) in WANTED:
            return key, "auto", "asr-orig"
    if vlang in WANTED and vlang in auto:
        return vlang, "auto", "asr"
    # 4. auto traduits (dernier recours)
    for lang in WANTED:
        if lang in auto:
            return lang, "auto", f"translated-from-{vlang or 'unknown'}"
    return None, None, "no-subtitles"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookies", default=None)
    ap.add_argument("--sleep", type=float, default=1.0)
    ap.add_argument("--only", default="", help="IDs séparés par des virgules")
    args = ap.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    only = set(filter(None, args.only.split(",")))
    metas = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(META_DIR.glob("*.json"))]
    if only:
        metas = [m for m in metas if m["id"] in only]

    rows = []
    for m in metas:
        vid = m["id"]
        key, kind, note = choose_track(m)
        row = {"video_id": vid, "lang": key or "", "kind": kind or "", "note": note, "file": ""}
        if key:
            existing = sorted(RAW_DIR.glob(f"{vid}.{key}.*"))
            if not existing:
                opts = {
                    "quiet": True,
                    "noprogress": True,
                    "skip_download": True,
                    "ignoreerrors": True,
                    "writesubtitles": kind == "manual",
                    "writeautomaticsub": kind == "auto",
                    "subtitleslangs": [key],
                    "subtitlesformat": "json3/vtt/best",
                    "outtmpl": {"default": str(RAW_DIR / "%(id)s.%(ext)s")},
                    "sleep_interval_requests": args.sleep,
                    "sleep_interval_subtitles": args.sleep,
                    "extractor_args": {"youtube": {"skip": ["hls", "dash"]}},  # pas besoin des flux vidéo
                    "js_runtimes": {"node": {}, "deno": {}, "bun": {}},  # défis JS YouTube (yt-dlp-ejs)
                }
                if args.cookies:
                    opts["cookiefile"] = args.cookies
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={vid}"])
                existing = sorted(RAW_DIR.glob(f"{vid}.{key}.*"))
            row["file"] = existing[0].name if existing else ""
            if not existing:
                row["note"] = (row["note"] + " download-failed").strip()
        rows.append(row)
        print(f"[subs] {vid} {row['kind']:6} {row['lang']:8} {row['note']}", file=sys.stderr)

    # Fusion avec le manifeste existant (une exécution partielle n'efface pas les autres lignes).
    merged = {}
    if MANIFEST.exists():
        merged = {r["video_id"]: r for r in csv.DictReader(MANIFEST.open(encoding="utf-8"))}
    merged.update({r["video_id"]: r for r in rows})
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["video_id", "lang", "kind", "note", "file"])
        w.writeheader()
        w.writerows(sorted(merged.values(), key=lambda r: r["video_id"]))
    ok = sum(1 for r in merged.values() if r["file"])
    print(f"[subs] {ok}/{len(merged)} pistes téléchargées -> {RAW_DIR.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
