# Évolution de la stratégie (octobre 2025 → octobre 2026)

Repères datés sur les 9 vidéos transcrites. Les 7 vidéos d'octobre-décembre 2025 sans transcription
pourraient combler des trous (voir `data/classification.csv`).

## Chronologie des versions

| Version | Période | Vidéos | Ce qui caractérise la version |
|---|---|---|---|
| **V0** | oct. 2025 | CsV2m7miTyk (10-17), 3z6qgc66RA8 (10-22) | « unfilled fair value gap strategy » : FVG 15 min / 1 h / 4 h avec **contexte HTF** (high de la veille, FVG daily, London low), checklist de biais, **filtre FVG 3 min**, **SMT** ES, CISD défini par l'**opening price**, entrées en 1/2/3 min, « I go for targets » plutôt que 1:1 strict |
| **V0b** | déc. 2025 | v1rIJOeAv2c (12-24) | Modèle séparé « bougie 9-10 h » sur **ES**, fenêtre 10-11 h |
| **V1** | mai 2026 | Tea-SeT3-OU (05-06) | Formalisation en **3 étapes** ; **3 modèles d'entrée** (breaker, IFVG, OB) ; « new rule » de la 4e bougie ; 15m→1m, 1h→5m ; **pas de biais journalier** ; 1:1 strict |
| **V1.1** | juin 2026 | 6jM0S5_Um9M (06-09) | **Un trade par jour** ; règles de **timing** explicites ; gestion des grands ranges 1 h (50 %) ; CISD = breaker |
| **V2** | juil. 2026 | 4BLGd9GMo8U (07-29) — « UPDATED » | Entrées réduites à **IFVG + CISD** ; fenêtre **1-4 min** ; « mechanical », « I don't trade with discretion » ; C3 avec « big wick » ; « fill the entirety » |
| **V3** | sept.-oct. 2026 | 3LrXQDS187Y (09-30), nxYi6bd9enA (10-06), oSqLOXBP7NY (10-08) | FVG **4 h** et table d'alignement complète ; **modèle de continuation** (CPT) ; objectif « upper portion of the gap » ; en live : **stop large puis BE / swing low**, 250 $/jour par compte ; « wicks do the damage, bodies tell the story » |

## Règles abandonnées ou modifiées

| Règle | Avant | Après | Sources |
|---|---|---|---|
| Contexte HTF (daily / 4 h) | Nécessaire : « then and only then I can scale down to this one minute chart » (V0) | Inutile : « Scalp model, don't need no daily bias » (V1+) | [CsV2m7miTyk @ 0:02:04](https://www.youtube.com/watch?v=CsV2m7miTyk&t=124s) → [Tea-SeT3-OU @ 0:29:10](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1750s) |
| Filtre FVG 3 min de la jambe de sweep | « I can't be long biased until we disrespect this 3minut bearish for rally gap [FVG 3 min] » (V0) | Plus mentionné (V1+) | [3z6qgc66RA8 @ 0:01:21](https://www.youtube.com/watch?v=3z6qgc66RA8&t=81s) |
| SMT avec ES | Confluence (V0) | Plus mentionné | [3z6qgc66RA8 @ 0:02:16](https://www.youtube.com/watch?v=3z6qgc66RA8&t=136s) ; [CsV2m7miTyk @ 0:04:15](https://www.youtube.com/watch?v=CsV2m7miTyk&t=255s) |
| Définition du CISD | Cassure de l'**opening price** de la série de bougies du sweep (V0) | = **breaker** : « low, high, lower low, higher high » (V1.1+) | [CsV2m7miTyk @ 0:10:26](https://www.youtube.com/watch?v=CsV2m7miTyk&t=626s) → [6jM0S5_Um9M @ 0:02:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=146s) |
| Liste des modèles d'entrée | breaker + IFVG + **OB** : « This is the only entry models » (V1) | **IFVG + CISD** (V2) ; l'OB revient en live comme confluence (V3) | [Tea-SeT3-OU @ 0:06:23](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=383s) → [4BLGd9GMo8U @ 0:02:59](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=179s) → [nxYi6bd9enA @ 0:11:53](https://www.youtube.com/watch?v=nxYi6bd9enA&t=713s) |
| TF d'entrée | 1, 2 ou 3 min indifféremment (V0) | Alignement strict 15m→1m / 1h→5m (V1+), avec exceptions | [3z6qgc66RA8 @ 0:02:07](https://www.youtube.com/watch?v=3z6qgc66RA8&t=127s) → [6jM0S5_Um9M @ 0:09:16](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=556s) |
| HTF du FVG | 15 min / 1 h (V0-V2) | + **4 h** (V3) | [3LrXQDS187Y @ 0:23:07](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1387s) |
| Objectif | « My target is the unfilled gap … I don't go for points » (V0) | « always … one-to-one and take out full profits at the unfilled gap » (V1) ; « upper portion » (V3) | [CsV2m7miTyk @ 0:11:29](https://www.youtube.com/watch?v=CsV2m7miTyk&t=689s) → [Tea-SeT3-OU @ 0:18:32](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1112s) → [3LrXQDS187Y @ 0:32:20](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1940s) |
| Gestion | Aucune : 1:1 posé puis laissé courir (V1-V2) | Stop large puis **BE / swing low** (V3, live) | [nxYi6bd9enA @ 0:02:30](https://www.youtube.com/watch?v=nxYi6bd9enA&t=150s) ; [oSqLOXBP7NY @ 0:03:24](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=204s) |
| Fréquence | Plusieurs trades par jour en revue (V0) | **Un trade par jour** (V1.1) | [6jM0S5_Um9M @ 0:02:56](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=176s) |
| Modèle 9-10 h (ES) | Présenté comme « the strategy in of itself » (V0b) | Plus mentionné en 2026 | [v1rIJOeAv2c @ 0:09:51](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=591s) |
| Indicateur HTF | « PO3 candles », 4 bougies (V1) | « ICT HTF candles », 4 puis **6** bougies (V1.1-V3) | [Tea-SeT3-OU @ 0:24:01](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1441s) → [6jM0S5_Um9M @ 0:06:01](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=361s) → [4BLGd9GMo8U @ 0:09:20](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=560s) |

## Ce qui ne change pas d'octobre 2025 à octobre 2026

- Le **noyau** : FVG HTF + 3e bougie qui refuse de continuer + retour vers le gap (« inefficiency », « low volume », « magnet »).
- La **contre-tendance assumée** : « the best possible plays in a trend would be … counter trend play » [3z6qgc66RA8 @ 0:09:44](https://www.youtube.com/watch?v=3z6qgc66RA8&t=584s) ; « we need to retrace back towards that gap, even if we're bullish or bearish » [4BLGd9GMo8U @ 0:14:56](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=896s).
- La visée **1:1** et la logique prop firm (« base hits »).
- La lecture **PO3** de la bougie suivante (open → manipulation → flip → distribution).
