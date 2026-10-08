# Analyse de la stratégie AMAS PFT

Objectif : extraire la stratégie de trading de la chaîne YouTube
[AMAS PFT](https://www.youtube.com/@amaspft), la formaliser en règles objectives sourcées
(vidéo + timestamp), puis la coder (indicateur Pine v6 → `strategy()` Pine → backtest Python sur NQ Databento).

## Règles de travail

- Aucune règle inventée : chaque règle cite sa source `vidéo @ H:MM:SS`.
- Statut de chaque règle : **explicite** / **déduite** / **discrétionnaire** / **contradictoire**.
- `[VISUEL @ H:MM:SS]` = passage qui dépend de ce qui est montré à l'écran (non vérifiable par la transcription seule).
- Une phase à la fois, validation avant la suivante.

## Arborescence

```
data/
  index.csv               # toutes les vidéos : id, date, titre, durée, URL, type, langue, sous-titres dispo
  meta/<id>.json          # métadonnées complètes par vidéo (description, chapitres, pistes de sous-titres)
  subs_raw/               # sous-titres bruts (json3 ou vtt) — non versionnés, régénérables
  subs_manifest.csv       # piste choisie par vidéo (manuel / auto original / auto traduit)
  transcripts/*.md        # transcriptions propres, paragraphes horodatés [H:MM:SS]
  transcripts/json/*.json # segments fins {start, end, text} pour la recherche
  classification_auto.csv # pré-tri automatique par mots-clés (non conclusif)
  classification.csv      # classement final, validé à la lecture  (Phase 0.3)
  ordre_lecture.md        # ordre de lecture proposé                (Phase 0.3)
notes/                    # Phase 1 : une fiche par vidéo
strategy/                 # Phase 2-3 : glossaire, règles, questions, pseudo-code
scripts/                  # pipeline
```

## Phase 0 — exécution

```bash
pip install -r requirements.txt          # yt-dlp + Node.js 22+ (ou Deno) requis
python3 scripts/run_phase0.py --test     # essai sur 3 vidéos
python3 scripts/run_phase0.py            # toute la chaîne
python3 scripts/run_phase0.py --sleep 4  # plus lent si YouTube renvoie 429 / « not a bot »
python3 scripts/run_phase0.py --cookies cookies.txt   # dernier recours
```

Si YouTube bloque l'IP du serveur cloud : guide pas à pas pour lancer la collecte sur un ordinateur
personnel dans [`docs/phase0_en_local.md`](docs/phase0_en_local.md).

Chaque étape est reprenable (ce qui est déjà téléchargé est sauté).

Choix des sous-titres, par vidéo : manuel (langue de la vidéo, puis FR, puis EN)
→ auto **original** (reconnaissance vocale, `xx-orig`) → en dernier recours auto **traduit**
(signalé `translated-from-…` dans `subs_manifest.csv`, à considérer comme peu fiable).
