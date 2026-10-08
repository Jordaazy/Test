# Résultats du backtest — modèle A (unfilled FVG)

Données : NQ continu 1 min (Databento GLBX.MDP3), 2025-01-01 → 2026-10-05, front month au volume de la veille, ajustement par différence. Coûts par défaut : 4,50 $ aller-retour + 1 tick de slippage (entrée marché, stop, sortie forcée). R = résultat net ÷ risque initial.

> **Lecture de la séparation IS / OOS.** Les valeurs par défaut ont été fixées à partir des vidéos, *avant* de voir les données : pour la version de référence, 2025 comme 2026 sont hors échantillon. En revanche, l'auteur a formalisé ses règles en 2026 en montrant des trades de 2026 : cette période peut être favorable à ses règles par construction (biais de sélection des exemples). La séparation IS 2025 / OOS 2026 sert surtout à juger l'optimisation (grille, walk-forward).

## 1. Version de référence (valeurs par défaut)

Paramètres : `strategy/parametres.json` (défauts). In-sample = 2025, out-of-sample = 2026-01 → 2026-10.

| HTF | période | trades | trades_par_mois | winrate | R_moyen (expectancy) | R_median | t_stat | R_total | profit_factor | gain_moyen_R | perte_moyenne_R | drawdown_max_R | pertes_consecutives_max | sorties_TP_SL_temps | risque_moyen_pts | duree_mediane_min | usd_par_contrat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 15 min | complet | 119 | 5.7 | 0.555 | 0.112 | 0.245 | 1.46 | 13.3 | 1.34 | 0.791 | -0.733 | 8.6 | 5 | 43/31/45 | 44.5 | 16 | 15914 |
| 15 min | IS 2025 | 65 | 5.4 | 0.508 | -0.001 | 0.025 | -0.01 | -0 | 1 | 0.747 | -0.771 | 8.6 | 4 | 20/20/25 | 42.4 | 16 | 3937 |
| 15 min | OOS 2026 | 54 | 5.9 | 0.611 | 0.247 | 0.516 | 2.23 | 13.3 | 1.94 | 0.834 | -0.675 | 4.2 | 5 | 23/11/20 | 47.1 | 13 | 11977 |
| 60 min | complet | 27 | 1.3 | 0.37 | -0.11 | -0.27 | -0.64 | -3 | 0.77 | 0.978 | -0.749 | 7 | 6 | 9/10/8 | 72.1 | 50 | 2123 |
| 60 min | IS 2025 | 10 | 0.8 | 0.3 | -0.269 | -0.642 | -0.95 | -2.7 | 0.51 | 0.933 | -0.784 | 5.4 | 6 | 2/5/3 | 59.2 | 57 | 1850 |
| 60 min | OOS 2026 | 17 | 1.9 | 0.412 | -0.016 | -0.202 | -0.07 | -0.3 | 0.96 | 0.997 | -0.725 | 3.4 | 3 | 7/5/5 | 79.6 | 50 | 273 |
| 240 min | complet | 7 | 0.3 | 0.286 | -0.332 | -0.512 | -1.14 | -2.3 | 0.35 | 0.614 | -0.711 | 3.6 | 5 | 1/3/3 | 144.9 | 90 | -8061 |
| 240 min | IS 2025 | 5 | 0.4 | 0.2 | -0.464 | -0.512 | -1.84 | -2.3 | 0.09 | 0.23 | -0.637 | 2.5 | 4 | 0/2/3 | 151.1 | 90 | -9102 |
| 240 min | OOS 2026 | 2 | 0.2 | 0.5 | -0.003 | -0.003 |  | -0 | 0.99 | 0.999 | -1.005 | 1 | 1 | 1/1/0 | 129.4 | 75 | 1041 |


### Entonnoir (15 min)

| index | nombre |
|---|---|
| signaux (événements) | 878 |
| dont W1 | 196 |
| dont W2 | 682 |
| rejet : stop_plus_serre_que_structure | 562 |
| rejet : position_ou_ordre_en_cours | 68 |
| rejet : plafond_journalier | 119 |
| rejet : objectif_deja_depasse | 10 |
| trades | 119 |


### Robustesse statistique (15 min, rééchantillonnage de l'ordre des trades)

- **complet** : `{"expectancy_IC95": [-0.03, 0.266], "P(expectancy<=0)": 0.067, "drawdown_R_p50_p95": [6.1, 11.3], "pertes_consecutives_p95": 8}`
- **IS 2025** : `{"expectancy_IC95": [-0.202, 0.192], "P(expectancy<=0)": 0.491, "drawdown_R_p50_p95": [6.9, 14.4], "pertes_consecutives_p95": 9}`
- **OOS 2026** : `{"expectancy_IC95": [0.039, 0.458], "P(expectancy<=0)": 0.011, "drawdown_R_p50_p95": [3.1, 6.2], "pertes_consecutives_p95": 6}`


### 15 min — par session **et par année** (une régularité doit tenir dans les deux)

| session | annee | trades | winrate | R_moyen |
|---|---|---|---|---|
| NY après-midi | 2025 | 29 | 0.414 | -0.19 |
| NY après-midi | 2026 | 25 | 0.52 | 0.095 |
| NY matin | 2025 | 36 | 0.583 | 0.152 |
| NY matin | 2026 | 29 | 0.69 | 0.379 |


**modele × année**

| modele | annee | trades | R_moyen |
|---|---|---|---|
| CISD | 2025 | 7 | 0.368 |
| CISD | 2026 | 2 | 0.995 |
| IFVG | 2025 | 58 | -0.045 |
| IFVG | 2026 | 52 | 0.218 |


**dir × année**

| dir | annee | trades | R_moyen |
|---|---|---|---|
| -1 | 2025 | 42 | -0.11 |
| -1 | 2026 | 33 | 0.234 |
| 1 | 2025 | 23 | 0.198 |
| 1 | 2026 | 21 | 0.268 |


**fenetre × année**

| fenetre | annee | trades | R_moyen |
|---|---|---|---|
| W1 | 2025 | 3 | -0.358 |
| W1 | 2026 | 4 | -0.017 |
| W2 | 2025 | 62 | 0.017 |
| W2 | 2026 | 50 | 0.268 |


### 15 min — par session

| index | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| NY après-midi | 54 | 0.463 | -0.058 | -3.1 |
| NY matin | 65 | 0.631 | 0.253 | 16.4 |


### 15 min — par heure d'entrée (ET)

| t_entree | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| 8 | 13 | 0.538 | 0.04 | 0.5 |
| 9 | 14 | 0.643 | 0.241 | 3.4 |
| 10 | 22 | 0.682 | 0.313 | 6.9 |
| 11 | 16 | 0.625 | 0.354 | 5.7 |
| 12 | 15 | 0.6 | 0.092 | 1.4 |
| 13 | 14 | 0.571 | 0.218 | 3.1 |
| 14 | 16 | 0.375 | -0.306 | -4.9 |
| 15 | 9 | 0.222 | -0.298 | -2.7 |


### 15 min — par jour

| t_entree | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| jeu | 23 | 0.565 | 0.052 | 1.2 |
| lun | 22 | 0.5 | 0.072 | 1.6 |
| mar | 28 | 0.679 | 0.373 | 10.4 |
| mer | 22 | 0.364 | -0.251 | -5.5 |
| ven | 24 | 0.625 | 0.234 | 5.6 |


### 15 min — par fenêtre d'entrée

| fenetre | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| W1 | 7 | 0.429 | -0.163 | -1.1 |
| W2 | 112 | 0.562 | 0.129 | 14.4 |


### 15 min — par modèle d'entrée

| modele | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| CISD | 9 | 0.778 | 0.508 | 4.6 |
| IFVG | 110 | 0.536 | 0.079 | 8.7 |


### 15 min — par sens (1 = long)

| dir | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| -1 | 75 | 0.507 | 0.041 | 3.1 |
| 1 | 44 | 0.636 | 0.232 | 10.2 |


### 15 min — par motif de sortie

| raison | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| SL | 31 | 0 | -1.022 | -31.7 |
| TP | 43 | 1 | 0.992 | 42.6 |
| temps | 45 | 0.511 | 0.052 | 2.3 |


### 15 min — C3 a balayé l'extrême de C2 ?

| sweep_c2 | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| False | 49 | 0.531 | 0.032 | 1.5 |
| True | 70 | 0.571 | 0.168 | 11.8 |


### 15 min — par mois

| t_entree | trades | winrate | R_moyen | R_total |
|---|---|---|---|---|
| 2025-01 | 3 | 0.667 | 0.498 | 1.5 |
| 2025-02 | 3 | 0.667 | 0.005 | 0 |
| 2025-03 | 6 | 0.833 | 0.377 | 2.3 |
| 2025-04 | 4 | 0.75 | 0.36 | 1.4 |
| 2025-05 | 11 | 0.636 | 0.217 | 2.4 |
| 2025-06 | 1 | 0 | -0.626 | -0.6 |
| 2025-07 | 7 | 0.143 | -0.73 | -5.1 |
| 2025-08 | 5 | 0.6 | 0.267 | 1.3 |
| 2025-09 | 5 | 0.4 | -0.15 | -0.7 |
| 2025-10 | 6 | 0.167 | -0.321 | -1.9 |
| 2025-11 | 7 | 0.571 | 0.034 | 0.2 |
| 2025-12 | 7 | 0.429 | -0.112 | -0.8 |
| 2026-01 | 4 | 0.75 | 0.323 | 1.3 |
| 2026-02 | 5 | 0.6 | 0.108 | 0.5 |
| 2026-03 | 7 | 0.857 | 0.723 | 5.1 |
| 2026-04 | 10 | 0.4 | 0.066 | 0.7 |
| 2026-05 | 7 | 0.857 | 0.646 | 4.5 |
| 2026-06 | 3 | 0.667 | 0.328 | 1 |
| 2026-07 | 6 | 0.333 | -0.164 | -1 |
| 2026-08 | 5 | 1 | 0.884 | 4.4 |
| 2026-09 | 7 | 0.286 | -0.45 | -3.2 |


## 2. Sensibilité, un paramètre à la fois (15 min)

Chaque ligne change **un seul** paramètre par rapport à la référence. On cherche des zones stables, pas le maximum.

| paramètre | valeur | IS_trades | IS_winrate | IS_R_moyen | IS_PF | IS_DD_R | OOS_trades | OOS_winrate | OOS_R_moyen | OOS_PF | OOS_DD_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (référence) |  | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| ltf_map | {"15": 2, "60": 3} | 26 | 0.5 | 0.078 | 1.22 | 3.9 | 11 | 0.545 | 0.13 | 1.44 | 2.2 |
| session_et | ["00:00", "24:00"] | 143 | 0.476 | -0.043 | 0.9 | 13.5 | 128 | 0.516 | -0.027 | 0.93 | 10 |
| session_et | ["09:30", "11:30"] | 17 | 0.529 | -0.053 | 0.87 | 3.3 | 14 | 0.786 | 0.61 | 8.62 | 1 |
| session_et | ["09:30", "16:00"] | 55 | 0.473 | -0.083 | 0.8 | 8.5 | 46 | 0.609 | 0.269 | 2.2 | 3.4 |
| max_trades_par_jour | 2 | 75 | 0.507 | 0.01 | 1.03 | 10.3 | 64 | 0.594 | 0.168 | 1.56 | 3.2 |
| max_trades_par_jour | 3 | 79 | 0.494 | -0.015 | 0.96 | 11.3 | 66 | 0.576 | 0.158 | 1.53 | 3.4 |
| max_trades_par_jour | 99 | 79 | 0.494 | -0.015 | 0.96 | 11.3 | 66 | 0.576 | 0.158 | 1.53 | 3.4 |
| gap_min_points | 2 | 59 | 0.508 | -0.014 | 0.96 | 8.6 | 48 | 0.625 | 0.264 | 2.08 | 3.2 |
| gap_min_points | 5 | 49 | 0.531 | 0.03 | 1.09 | 5.4 | 46 | 0.63 | 0.28 | 2.2 | 3.2 |
| c3_regle | "sweep_c2" | 40 | 0.5 | 0.017 | 1.05 | 5.2 | 36 | 0.667 | 0.32 | 2.72 | 1.5 |
| c3_regle | "sweep_c2+wick" | 27 | 0.481 | -0.079 | 0.79 | 5.1 | 25 | 0.56 | 0.186 | 1.71 | 2.3 |
| c3_wick_min | 0.5 | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| c2_displacement_atr_k | 0.75 | 44 | 0.591 | 0.066 | 1.19 | 4.9 | 39 | 0.59 | 0.243 | 1.99 | 3.2 |
| c2_displacement_atr_k | 1.0 | 35 | 0.6 | 0.107 | 1.36 | 3.9 | 30 | 0.633 | 0.344 | 2.9 | 1.2 |
| c2_displacement_atr_k | 1.5 | 19 | 0.526 | 0.171 | 1.6 | 3.2 | 13 | 0.615 | 0.354 | 2.89 | 1.1 |
| c2_body_ratio_min | 0.5 | 50 | 0.58 | 0.112 | 1.34 | 4.5 | 46 | 0.609 | 0.249 | 2.03 | 2.2 |
| c2_body_ratio_min | 0.7 | 31 | 0.645 | 0.157 | 1.54 | 3.6 | 27 | 0.593 | 0.203 | 1.76 | 2 |
| consommer_si_gap_touche | false | 71 | 0.507 | 0.016 | 1.04 | 10.8 | 60 | 0.6 | 0.232 | 1.84 | 2 |
| w1_actif | false | 64 | 0.516 | 0.02 | 1.06 | 7.2 | 52 | 0.635 | 0.296 | 2.27 | 2.1 |
| w1_minutes_avant_cloture | {"15": 2} | 65 | 0.508 | -0.001 | 1 | 8.6 | 53 | 0.623 | 0.272 | 2.09 | 3.1 |
| w1_minutes_avant_cloture | {"15": 6} | 65 | 0.508 | -0.012 | 0.97 | 9.4 | 56 | 0.607 | 0.238 | 1.88 | 4.2 |
| w1_minutes_avant_cloture | {"60": 5} | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| w1_distance_c2_frac | 0 | 76 | 0.539 | 0.063 | 1.18 | 7.1 | 63 | 0.667 | 0.336 | 2.41 | 4.2 |
| w1_distance_c2_frac | 0.15 | 68 | 0.515 | 0.002 | 1.01 | 8.4 | 57 | 0.614 | 0.246 | 1.92 | 4.2 |
| w1_distance_c2_frac | 0.5 | 64 | 0.516 | 0.016 | 1.04 | 7.6 | 52 | 0.635 | 0.296 | 2.27 | 2.1 |
| w2_actif | false | 3 | 0.333 | -0.358 | 0.48 | 2.1 | 4 | 0.5 | -0.017 | 0.97 | 2.1 |
| w2_flip_requis | true | 22 | 0.545 | 0.053 | 1.12 | 4.4 | 17 | 0.588 | 0.192 | 1.59 | 2.6 |
| sortie_forcee | "cloture_C4" | 65 | 0.431 | -0.021 | 0.91 | 6 | 54 | 0.463 | 0.05 | 1.21 | 4.3 |
| sortie_forcee | "jamais" | 65 | 0.508 | 0.002 | 1 | 8.6 | 54 | 0.648 | 0.287 | 1.8 | 4.1 |
| modeles | ["IFVG"] | 60 | 0.483 | -0.044 | 0.89 | 10.5 | 52 | 0.596 | 0.218 | 1.8 | 4.2 |
| modeles | ["CISD"] | 7 | 0.714 | 0.368 | 3.14 | 1 | 3 | 1 | 0.682 |  | 0 |
| modeles | ["IFVG", "CISD", "OB"] | 65 | 0.523 | 0.016 | 1.04 | 8.6 | 55 | 0.6 | 0.224 | 1.81 | 4.2 |
| modeles | ["CISD_OPEN"] | 62 | 0.694 | 0.394 | 3.1 | 2.7 | 34 | 0.471 | -0.014 | 0.97 | 5.8 |
| fractal_n | 1 | 75 | 0.56 | 0.096 | 1.3 | 6.3 | 61 | 0.59 | 0.203 | 1.68 | 4.2 |
| fractal_n | 3 | 61 | 0.508 | 0.005 | 1.01 | 8.4 | 52 | 0.596 | 0.218 | 1.8 | 4.2 |
| fenetre_structure_debut | "ouverture_C2" | 61 | 0.492 | 0.009 | 1.03 | 7.5 | 50 | 0.62 | 0.254 | 2.05 | 2.1 |
| ifvg_min_points | 1 | 57 | 0.579 | 0.113 | 1.37 | 2.9 | 49 | 0.571 | 0.188 | 1.65 | 3.2 |
| ifvg_min_points | 2 | 50 | 0.6 | 0.177 | 1.69 | 2.1 | 40 | 0.55 | 0.156 | 1.52 | 3.5 |
| type_ordre | "limite_zone" | 85 | 0.553 | 0.044 | 1.12 | 5.1 | 79 | 0.633 | 0.218 | 1.72 | 4.1 |
| tp_profondeur | 0.25 | 83 | 0.53 | 0.016 | 1.04 | 5.7 | 75 | 0.6 | 0.192 | 1.67 | 4.4 |
| tp_profondeur | 0.5 | 110 | 0.5 | -0.048 | 0.88 | 15.3 | 87 | 0.586 | 0.113 | 1.35 | 7.8 |
| tp_profondeur | 1.0 | 146 | 0.5 | -0.033 | 0.91 | 9.3 | 111 | 0.55 | 0.046 | 1.14 | 6 |
| stop_mode | "STRUCTURE" | 181 | 0.475 | -0.044 | 0.9 | 17.2 | 147 | 0.429 | -0.12 | 0.75 | 20 |
| stop_mode | "C3_EXTREME" | 186 | 0.484 | -0.045 | 0.9 | 25.9 | 150 | 0.453 | -0.097 | 0.81 | 15.6 |
| stop_buffer_ticks | 0 | 68 | 0.515 | 0.013 | 1.03 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| stop_buffer_ticks | 4 | 64 | 0.5 | -0.016 | 0.96 | 9.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| distance_tp_min_points | {"15": 5} | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| distance_tp_min_points | {"15": 12} | 63 | 0.492 | -0.037 | 0.9 | 10.9 | 52 | 0.615 | 0.258 | 2.02 | 3.1 |
| distance_tp_min_points | {"15": 20} | 54 | 0.537 | 0.052 | 1.16 | 3.6 | 48 | 0.646 | 0.311 | 2.41 | 2.1 |
| be_a_R | 0.5 | 65 | 0.354 | -0.053 | 0.83 | 9.9 | 54 | 0.426 | 0.146 | 1.67 | 3.2 |
| be_a_R | 0.7 | 65 | 0.431 | -0.025 | 0.93 | 8.9 | 54 | 0.556 | 0.252 | 2.17 | 2.6 |
| grand_range_points_1h | 100 | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| grand_range_points_1h | 200 | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| grand_range_points_1h | null | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| slippage_ticks_marche_et_stop | 0 | 68 | 0.515 | 0.022 | 1.06 | 8.2 | 54 | 0.611 | 0.253 | 1.98 | 4.1 |
| slippage_ticks_marche_et_stop | 2 | 64 | 0.5 | -0.024 | 0.94 | 10 | 54 | 0.611 | 0.241 | 1.9 | 4.2 |
| limite_trade_through_ticks | 0 | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |


## 3. Grille de robustesse (162 combinaisons, 15 min)

- combinaisons à expectancy > 0 : **10% en IS**, **45% en OOS**, 9% dans les deux ;
- corrélation IS → OOS de l'expectancy entre combinaisons : **-0.76** (proche de 0 ou négative = le classement IS ne prédit rien).


**Moyenne sur la grille par `tp_profondeur`**

| tp_profondeur | IS_R_moyen | OOS_R_moyen | IS_trades | OOS_trades |
|---|---|---|---|---|
| 0 | -0.163 | 0.169 | 81.981 | 70.019 |
| 0.5 | -0.05 | 0.039 | 105.296 | 85.037 |
| 1 | -0.041 | -0.005 | 122.944 | 97.87 |


**Moyenne sur la grille par `stop_mode`**

| stop_mode | IS_R_moyen | OOS_R_moyen | IS_trades | OOS_trades |
|---|---|---|---|---|
| STRUCTURE | -0.053 | -0.063 | 138.802 | 113.074 |
| TP_FIRST | -0.117 | 0.199 | 68.012 | 55.543 |


**Moyenne sur la grille par `fenetres`**

| fenetres | IS_R_moyen | OOS_R_moyen | IS_trades | OOS_trades |
|---|---|---|---|---|
| W1 | -0.157 | 0.092 | 41.111 | 34.741 |
| W1+W2 | -0.044 | 0.039 | 142.407 | 112.833 |
| W2 | -0.053 | 0.072 | 126.704 | 105.352 |


**Moyenne sur la grille par `gap_min_points`**

| gap_min_points | IS_R_moyen | OOS_R_moyen | IS_trades | OOS_trades |
|---|---|---|---|---|
| 0.25 | -0.054 | 0.009 | 110.13 | 89.815 |
| 2 | -0.105 | 0.076 | 104.981 | 85.778 |
| 5 | -0.095 | 0.119 | 95.111 | 77.333 |


**Moyenne sur la grille par `distance_tp_min_points`**

| distance_tp_min_points | IS_R_moyen | OOS_R_moyen | IS_trades | OOS_trades |
|---|---|---|---|---|
| 5 | -0.081 | 0.064 | 104.87 | 84.426 |
| 8 | -0.078 | 0.064 | 104.093 | 84.426 |
| 12 | -0.095 | 0.075 | 101.259 | 84.074 |


**Les 10 meilleures combinaisons en IS et leur résultat OOS** (pour mesurer la dégradation)

| index | tp_profondeur | stop_mode | fenetres | gap_min_points | distance_tp_min_points | IS_trades | IS_winrate | IS_R_moyen | IS_PF | IS_DD_R | OOS_trades | OOS_winrate | OOS_R_moyen | OOS_PF | OOS_DD_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 71 | 0.5 | TP_FIRST | W1 | 5 | 12 | 8 | 0.5 | 0.079 | 1.19 | 3.3 | 6 | 0.667 | 0.326 | 1.97 | 1 |
| 70 | 0.5 | TP_FIRST | W1 | 5 | 8 | 8 | 0.5 | 0.079 | 1.19 | 3.3 | 6 | 0.667 | 0.326 | 1.97 | 1 |
| 69 | 0.5 | TP_FIRST | W1 | 5 | 5 | 8 | 0.5 | 0.079 | 1.19 | 3.3 | 6 | 0.667 | 0.326 | 1.97 | 1 |
| 123 | 1 | TP_FIRST | W1 | 5 | 5 | 28 | 0.536 | 0.045 | 1.11 | 5.3 | 20 | 0.45 | 0.036 | 1.09 | 2.4 |
| 124 | 1 | TP_FIRST | W1 | 5 | 8 | 28 | 0.536 | 0.045 | 1.11 | 5.3 | 20 | 0.45 | 0.036 | 1.09 | 2.4 |
| 24 | 0 | TP_FIRST | W2 | 5 | 5 | 49 | 0.531 | 0.036 | 1.11 | 5.1 | 45 | 0.622 | 0.264 | 2.11 | 3.2 |
| 25 | 0 | TP_FIRST | W2 | 5 | 8 | 49 | 0.531 | 0.036 | 1.11 | 5.1 | 45 | 0.622 | 0.264 | 2.11 | 3.2 |
| 7 | 0 | TP_FIRST | W1+W2 | 5 | 8 | 49 | 0.531 | 0.03 | 1.09 | 5.4 | 46 | 0.63 | 0.28 | 2.2 | 3.2 |
| 6 | 0 | TP_FIRST | W1+W2 | 5 | 5 | 49 | 0.531 | 0.03 | 1.09 | 5.4 | 46 | 0.63 | 0.28 | 2.2 | 3.2 |
| 19 | 0 | TP_FIRST | W2 | 0.25 | 8 | 64 | 0.516 | 0.02 | 1.06 | 7.2 | 52 | 0.635 | 0.296 | 2.27 | 2.1 |


## 4. Walk-forward (15 min) — 6 mois d'entraînement, 3 mois de test

Choix = tp_profondeur / stop_mode / fenetres / gap_min_points / distance_tp_min_points ; sélection lissée par les voisins pour éviter de choisir un pic isolé.

| entraînement | test | choix | score_entr. | R_moyen_entr. | test_trades | test_R_moyen | référence_test_trades | référence_test_R_moyen |
|---|---|---|---|---|---|---|---|---|
| 2025-01 → 2025-07 | 2025-07 → 2025-10 | 0 / TP_FIRST / W1+W2 / 0.25 / 5 | 0.252 | 0.249 | 17 | -0.266 | 17 | -0.266 |
| 2025-04 → 2025-10 | 2025-10 → 2026-01 | 0 / STRUCTURE / W1+W2 / 5 / 8 | -0.011 | -0.009 | 39 | -0.079 | 20 | -0.124 |
| 2025-07 → 2026-01 | 2026-01 → 2026-04 | 1.0 / STRUCTURE / W2 / 2 / 8 | 0.091 | 0.146 | 42 | -0.037 | 16 | 0.431 |
| 2025-10 → 2026-04 | 2026-04 → 2026-07 | 0 / TP_FIRST / W2 / 0.25 / 5 | 0.27 | 0.123 | 19 | 0.272 | 20 | 0.308 |
| 2026-01 → 2026-07 | 2026-07 → 2026-10 | 0 / TP_FIRST / W1+W2 / 5 / 5 | 0.402 | 0.391 | 15 | 0.05 | 18 | 0.016 |
| 2026-04 → 2026-10 | 2026-10 → 2027-01 | 0 / TP_FIRST / W1+W2 / 5 / 12 | 0.229 | 0.159 | 0 |  | 0 |  |


**Tous les trimestres de test mis bout à bout**

| version | trades | trades_par_mois | winrate | R_moyen (expectancy) | R_median | t_stat | R_total | profit_factor | gain_moyen_R | perte_moyenne_R | drawdown_max_R | pertes_consecutives_max | sorties_TP_SL_temps | risque_moyen_pts | duree_mediane_min | usd_par_contrat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| walk-forward (paramètres choisis) | 132 | 7.3 | 0.447 | -0.024 | -0.133 | -0.33 | -3.2 | 0.94 | 0.854 | -0.735 | 13.3 | 11 | 46/42/44 | 45.8 | 14 | -3029 |
| référence fixe | 91 | 5.1 | 0.516 | 0.07 | 0.025 | 0.78 | 6.3 | 1.2 | 0.825 | -0.737 | 8 | 5 | 32/26/33 | 42.6 | 14 | 8475 |


## 5. Sensibilité aux coûts (15 min)

| slippage_ticks | commission_usd | IS_trades | IS_winrate | IS_R_moyen | IS_PF | IS_DD_R | OOS_trades | OOS_winrate | OOS_R_moyen | OOS_PF | OOS_DD_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 68 | 0.515 | 0.03 | 1.08 | 7.9 | 54 | 0.611 | 0.26 | 2.02 | 4.1 |
| 0 | 4.5 | 68 | 0.515 | 0.022 | 1.06 | 8.2 | 54 | 0.611 | 0.253 | 1.98 | 4.1 |
| 0 | 6 | 68 | 0.515 | 0.019 | 1.05 | 8.3 | 54 | 0.611 | 0.251 | 1.97 | 4.1 |
| 1 | 0 | 65 | 0.508 | 0.008 | 1.02 | 8.3 | 54 | 0.611 | 0.254 | 1.98 | 4.1 |
| 1 | 4.5 | 65 | 0.508 | -0.001 | 1 | 8.6 | 54 | 0.611 | 0.247 | 1.94 | 4.2 |
| 1 | 6 | 65 | 0.508 | -0.004 | 0.99 | 8.7 | 54 | 0.611 | 0.245 | 1.93 | 4.2 |
| 2 | 0 | 64 | 0.5 | -0.016 | 0.96 | 9.6 | 54 | 0.611 | 0.248 | 1.94 | 4.2 |
| 2 | 4.5 | 64 | 0.5 | -0.024 | 0.94 | 10 | 54 | 0.611 | 0.241 | 1.9 | 4.2 |
| 2 | 6 | 64 | 0.5 | -0.027 | 0.93 | 10.1 | 54 | 0.611 | 0.239 | 1.89 | 4.3 |


_Calcul : 345 s._
