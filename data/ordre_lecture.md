# Phase 0 — Classement et ordre de lecture

Périmètre retenu (validé par l'utilisateur) : les **16 vidéos longues les plus récentes**
(2025-10-09 → 2026-10-08), dont **9 avec transcription**. Les 436 autres vidéos (anciennes vidéos,
lives, shorts) sont listées dans `index.csv` mais hors périmètre.

Toutes les transcriptions sont des **sous-titres automatiques anglais** (piste originale) :
fiables sur le fond, mais les termes techniques sont souvent déformés (voir le lexique en bas).

## Classement (lecture intégrale des 9 transcriptions)

| Catégorie | Vidéos |
|---|---|
| **Stratégie / règles** | Tea-SeT3-OU, 4BLGd9GMo8U, 6jM0S5_Um9M, 3LrXQDS187Y, v1rIJOeAv2c |
| **Trades en live / revue** (avec rappel du cadre) | nxYi6bd9enA, oSqLOXBP7NY, 3z6qgc66RA8, CsV2m7miTyk |
| **Mindset** | aucune vidéo dédiée ; éléments épars (1:1, « base hits », discipline prop firm) dans toutes |
| **Hors-sujet** | segments seulement : payouts / codes promo Tradeify / Discord (ex. 3LrXQDS187Y 0:00:00-0:01:22) |
| **Non classables** (pas de transcription) | ICMqaYh6l9g, uAITVN8kEUk, JGQ3-DJIWbo, EKdBRVsAItU, Z-FKuV1LiMI, NfMG6bHHmgg, 88O_nyGNIEs |

Détail et justification par vidéo : `data/classification.csv`.

## Ce que contient le corpus : 3 modèles distincts

1. **Unfilled FVG model** (« reversal model ») — le cœur de la chaîne en 2026.
   FVG en 15 min ou 1 h (4 h ajouté en septembre 2026), la 3e bougie échoue à clôturer au-delà de la 2e,
   on vise un retour dans le FVG à 1:1 avec une entrée en 1 min (ou 5 min pour un FVG 1 h).
2. **Continuation model** (« Candle Projection Theory », draw on liquidity) — n'apparaît que dans
   3LrXQDS187Y (2026-09-30) et dans le trade long de oSqLOXBP7NY.
3. **Modèle « bougie horaire 9h-10h »** — seulement dans v1rIJOeAv2c (2025-12-24) : la couleur de la
   bougie 9-10 h donne le biais de 10-11 h, tout MSS contraire est traité comme un fake-out.

Les vidéos d'octobre 2025 (CsV2m7miTyk, 3z6qgc66RA8) montrent une **version antérieure** du modèle 1
(contexte daily/4 h, sweep de London low, filtre FVG 3 min, SMT avec ES).

## Ordre de lecture proposé

Vidéos fondatrices d'abord (définitions formelles), puis la version la plus récente, puis les compléments,
puis les versions antérieures (pour tracer l'évolution).

| # | Vidéo | Pourquoi à ce rang |
|---|---|---|
| 1 | **Tea-SeT3-OU** (2026-05-06) — *This Stupid Simple Strategy Works Everyday* | Première formalisation complète : étapes 1-2-3, 3 modèles d'entrée (breaker, IFVG, OB), règle « 4e bougie » |
| 2 | **4BLGd9GMo8U** (2026-07-29) — *My UPDATED Day Trading Strategy (2026)* | Version « mise à jour » : entrées réduites à IFVG + CISD, fenêtre de timing 1-4 min avant clôture |
| 3 | **6jM0S5_Um9M** (2026-06-09) — *This Simple Scalping Strategy Makes Me Over $30,000/Month* | Règles de gestion : 1 trade/jour, alignement des TF, entrée prématurée = mauvais trade, cas des gros ranges H1 |
| 4 | **3LrXQDS187Y** (2026-09-30) — *This Trading Strategy Makes $1,000 a Day* | Modèle de continuation + modèle FVG étendu au 4 h + table d'alignement complète |
| 5 | **nxYi6bd9enA** (2026-10-06) — *Trading Was Hard, Until I Understood These Two Concepts* | Trade live H1/M5 : exécution réelle et gestion (break-even) |
| 6 | **oSqLOXBP7NY** (2026-10-08) — *If I Had to Make $500 by Tomorrow…* | Trade live : gestion du stop, entrée sur breaker HTF, short refusé |
| 7 | **3z6qgc66RA8** (2025-10-22) — *The Only Setup You Need To Pass A Funded Challenge* | Version 2025 : checklist de biais, filtre FVG 3 min, SMT |
| 8 | **CsV2m7miTyk** (2025-10-17) — *How I Increased Win Rate In Trading* | Version 2025 : contexte daily/4 h, PO3, CISD défini par prix d'ouverture |
| 9 | **v1rIJOeAv2c** (2025-12-24) — *Trading was HARD, until I realized this...* | Modèle séparé (bougie 9-10 h), à traiter à part |

## Lexique des erreurs de transcription automatique

| Transcrit | Sens |
|---|---|
| « unfilled for gap », « for value gap », « reval gap », « revel », « fal gap », « per value gap », « Enfield », « unfield », « unfiltered value gap » | unfilled fair value gap (FVG) |
| « IFBG », « inverse », « inverse fidelity gap » | IFVG (inversion fair value gap) |
| « PD rays », « PDA » | PD arrays |
| « consolation play » | continuation play |
| « ENQ », « Trade of Eate » | NQ ; Tradeify |
| « Tritify », « Traderify », « Trader Five », « Trade the Five », « Traify » | Tradeify (prop firm) |
| « Tradyncer », « Trade Syncer », « trade synch » | TradeSyncer (copie de trades multi-comptes) |
| « ICT HTF/HDF candles by Fadi / by body », « PO3 candles by Lee Dave » | indicateur TradingView affichant les dernières bougies HTF (nom exact à confirmer [VISUEL]) |
| « handles », « points » | points NQ |
