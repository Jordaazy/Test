# Phase 4 — Synthèse du backtest

Détail complet (tous les tableaux) : [`rapport_backtest.md`](rapport_backtest.md). Trades de la version de
référence : `trades_reference_15m.csv` (+ 60m, 240m). Grilles : `sensibilite_15m.csv`, `grille_15m.csv`,
`walkforward_15m.csv`. Reproduire : `python3 -m backtest.data <csv Databento> nq.parquet` puis
`python3 -m backtest.run --data nq.parquet --out results`.

**Données** : NQ 1 min Databento, du 2025-01-01 au 2026-10-05 (21 mois). Contrat le plus échangé la veille,
ajusté aux rolls. **Coûts** : 4,50 $ aller-retour, 1 tick de slippage sur les ordres au marché, les stops et
la sortie forcée. **R** = résultat net ÷ risque initial.

**Point de méthode** : les paramètres par défaut ont été fixés d'après les vidéos, **avant** de regarder les
données. Pour la version de référence, 2025 et 2026 sont donc tous deux hors échantillon. Mais l'auteur a
formalisé ses règles en 2026 en montrant des trades de 2026 : cette année peut lui être favorable par
construction.

## 1. Version de référence — FVG 15 min, entrée 1 min

| Période | Trades | Trades/mois | Winrate | R moyen | IC 95 % du R moyen | Profit factor | DD max (R) | Pertes consécutives max |
|---|---|---|---|---|---|---|---|---|
| 21 mois | 119 | 5,7 | 55,5 % | **+0,11** | [−0,03 ; +0,27] | 1,34 | 8,6 | 5 (p95 bootstrap : 8) |
| 2025 | 65 | 5,4 | 50,8 % | **0,00** | [−0,20 ; +0,19] | 1,00 | 8,6 | 4 |
| 2026 (jan.-oct.) | 54 | 5,9 | 61,1 % | **+0,25** | [+0,04 ; +0,46] | 1,94 | 4,2 | 5 |

- Sorties : 43 TP, 31 SL, **45 sorties forcées** à la clôture de C5. Plus d'un trade sur trois n'atteint ni le
  TP ni le SL en 30 min, loin du « TP within the next 5 minutes » qu'il annonce.
- Risque moyen : 44 points ; durée médiane : 16 min. Les coûts pèsent peu (environ 0,01 à 0,03 R).
- Sur 21 mois, l'espérance est positive mais **pas statistiquement établie** (P(R moyen ≤ 0) ≈ 7 %).
  Tout le gain vient de 2026.
- **1 h et 4 h** : trop peu de trades (27 et 7) et un résultat négatif (−0,11 R et −0,33 R).

## 2. Répartition (15 min)

| Session (entrée) | 2025 | 2026 |
|---|---|---|
| NY matin 8:30-12:00 | 36 trades, **+0,15 R** | 29 trades, **+0,38 R** |
| NY après-midi 12:00-16:00 | 29 trades, −0,19 R | 25 trades, +0,10 R |

- **Le matin est meilleur que l'après-midi dans les deux années** : c'est la régularité la plus nette.
  Le creux se situe à 14 h-16 h (−0,30 R sur 25 trades).
- Par jour : le mardi est le meilleur (+0,37 R), le mercredi le pire (−0,25 R, 22 trades). Sur des échantillons
  aussi petits, ces écarts sont compatibles avec le hasard.
- **Entrée W1** (anticipation pendant C3) : 7 trades seulement, −0,16 R. Presque tout passe par **W2**, pendant C4.
- **Sens** : les longs sont positifs dans les deux années (+0,20 et +0,27 R, environ 20 trades par an). Les
  shorts sont négatifs en 2025 (−0,11) et positifs en 2026 (+0,23).

## 3. Robustesse des paramètres — ce qui tient, ce qui s'inverse

Chaque paramètre est varié **seul** autour de la référence (`rapport_backtest.md` §2). Avec environ 50 trades
par an, l'erreur type d'un R moyen est d'environ ±0,13 R : seul un effet de **même signe sur les deux années**
mérite attention.

| Effet | 2025 | 2026 | Lecture |
|---|---|---|---|
| **Displacement de C2** (corps ≥ 1 × ATR14 15 min) | +0,11 (35 tr.) | +0,34 (30 tr.) | même sens sur les deux années ; c'est **sa propre règle** (« not enough displacement ») |
| Corps/range de C2 ≥ 0,5 | +0,11 (50) | +0,25 (46) | idem, plus doux |
| Distance mini à C2 en W1 = 0 | +0,06 | +0,34 | léger |
| Objectif au bord proche vs comblement (moyenne sur la grille) | −0,16 vs −0,04 | +0,17 vs −0,01 | **s'inverse** |
| Stop TP-first vs structure (grille) | −0,12 vs −0,05 | +0,20 vs −0,06 | **s'inverse** |
| CISD par opening price (variante 2025) | +0,39 | −0,01 | **s'inverse** |
| Break-even à +0,5 R | −0,05 | +0,15 | dégrade |
| Session 24 h | −0,04 | −0,03 | dégrade (Asie et Londres sans edge) |

## 4. L'optimisation ne se transfère pas

- Sur la grille de 162 combinaisons (objectif × stop × fenêtres × taille du gap × distance mini), la
  **corrélation entre le R moyen 2025 et le R moyen 2026 vaut −0,76**. Les meilleures combinaisons d'une année
  sont parmi les pires de l'autre : aucun optimum stable.
- **Walk-forward** (6 mois d'entraînement, 3 mois de test, choix lissé par les voisins) : **−0,02 R** sur
  132 trades, contre **+0,07 R** pour la référence fixe sur les mêmes trimestres.
- **Conclusion** : on garde les paramètres fixés d'après les vidéos. Ne pas optimiser sur cet historique.

## 5. Ce qu'on peut en conclure

1. La version mécanique du modèle **n'a pas d'edge démontré sur 21 mois** : +0,11 R par trade, un intervalle de
   confiance qui inclut 0, une année neutre et une année bonne. Le winrate mécanique (55 %) est loin des 72 à 92 %
   de ses titres.
2. Deux pistes **cohérentes avec ses propres règles** et stables sur les deux années : (a) exiger un vrai
   **displacement de C2**, (b) se limiter au **matin de New York**. Les échantillons restent petits (30 à
   40 trades par an), donc ce sont des **hypothèses à valider sur d'autres données**, pas des résultats.
3. Ce que le backtest **ne capte pas** : sa sélection discrétionnaire (« be selective »), les prediction plays,
   sa gestion live (break-even, ajouts de contrats) et ce qu'il réserve à son groupe privé.

## 6. Prochaines étapes proposées

- **Données plus anciennes** (2022-2024, même format Databento) pour tester ces deux hypothèses sans les avoir
  choisies sur ces données : le code est prêt, il suffit de relancer `backtest.data` puis `backtest.run`.
- **Forward test** avec l'indicateur Pine (signaux en temps réel), en comparant aux trades qu'il publie.
- Si tu veux, un **module C** (bougie 9-10 h sur ES) et un **module B** (continuation) dans le même moteur.
