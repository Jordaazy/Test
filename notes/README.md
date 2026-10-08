# Phase 1 — Fiches par vidéo

Une fiche par vidéo transcrite (9 sur les 16 du périmètre), dans l'ordre de lecture de
`data/ordre_lecture.md`.

| # | Fiche | Modèle(s) |
|---|---|---|
| 1 | [2026-05-06 — Stupid Simple Strategy](2026-05-06_stupid-simple-strategy_Tea-SeT3-OU.md) | Unfilled FVG : 3 étapes, 3 modèles d'entrée |
| 2 | [2026-07-29 — UPDATED Strategy (2026)](2026-07-29_updated-day-trading-strategy-2026_4BLGd9GMo8U.md) | Unfilled FVG : IFVG + CISD, timing 1-4 min |
| 3 | [2026-06-09 — $30,000/Month](2026-06-09_simple-scalping-strategy-30k-month_6jM0S5_Um9M.md) | Unfilled FVG + gestion (1 trade/jour, gros ranges 1 h) |
| 4 | [2026-09-30 — $1,000 a Day](2026-09-30_strategy-1000-a-day_3LrXQDS187Y.md) | Continuation (CPT) + reversal (FVG jusqu'au 4 h) |
| 5 | [2026-10-06 — Two Concepts (live)](2026-10-06_two-concepts-live-trade_nxYi6bd9enA.md) | Trade live FVG 1 h / M5, break-even |
| 6 | [2026-10-08 — $500 by Tomorrow (live)](2026-10-08_make-500-by-tomorrow_oSqLOXBP7NY.md) | Trade live breaker HTF ; short FVG refusé |
| 7 | [2025-10-22 — Funded Challenge](2025-10-22_only-setup-funded-challenge_3z6qgc66RA8.md) | Version 2025 : checklist, filtre FVG 3 min, SMT |
| 8 | [2025-10-17 — Increased Win Rate](2025-10-17_increased-win-rate_CsV2m7miTyk.md) | Version 2025 : daily/4 h, PO3, CISD (opening price) |
| 9 | [2025-12-24 — Hourly candle framework](2025-12-24_hourly-candle-framework_v1rIJOeAv2c.md) | Bougie 9-10 h → biais 10-11 h (ES) |

**Sans transcription** (bloquées par YouTube, non analysées) : ICMqaYh6l9g, uAITVN8kEUk, JGQ3-DJIWbo,
EKdBRVsAItU, Z-FKuV1LiMI, NfMG6bHHmgg, 88O_nyGNIEs.

## Conventions

- **Statuts** : EXPLICITE (dit tel quel), DÉDUITE (tirée de plusieurs passages), DISCRÉTIONNAIRE
  (laissé à l'appréciation), CONTRADICTOIRE (en conflit avec un autre passage), [VISUEL] (dépend de l'écran).
- **Citations** « … » : **mot pour mot** les sous-titres automatiques, fautes comprises ; mes corrections
  sont entre crochets, ex. « unfilled for gap [FVG] ». « … » marque une coupe.
- **Timestamps** : liens vers la vidéo à la seconde (début du segment de sous-titre).
- **Vérification** : `python3 scripts/check_citations.py notes/*.md` contrôle que chaque citation figure dans
  la transcription à ±1 min du timestamp (0 écart à ce jour).
