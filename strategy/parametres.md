# Paramètres (généré depuis `parametres.json`, ne pas éditer à la main)

Paramètres du modèle A (unfilled FVG). 'default' = version de référence (strategy/questions.md, section « Décisions à valider »). 'test' = plage de robustesse. 'q' = question associée. 'statut' = origine de la valeur : EXPLICITE (dite par lui), PROPOSITION (il ne chiffre rien), CHOIX (convention technique).

## cadre

| Paramètre | Défaut | Plage de test | Statut | Q | Note |
|---|---|---|---|---|---|
| `instrument` | `NQ` | `NQ` | EXPLICITE | Q17 | MNQ = même signal |
| `htf_minutes` | `15` | `15` · `60` · `240` | EXPLICITE | Q13 | 15 min = cœur du modèle |
| `ltf_map` | `{"15": 1, "60": 5, "240": 15}` | `{"15": 2, "60": 3}` | EXPLICITE | Q13 | exceptions 2 min / 3 min observées |
| `session_et` | `["08:30", "16:00"]` | `["00:00", "24:00"]` · `["09:30", "11:30"]` · `["09:30", "16:00"]` | PROPOSITION | Q12 | fenêtre d'ENTRÉE ; les positions peuvent sortir après |
| `max_trades_par_jour` | `1` | `1` · `2` · `3` · `99` | EXPLICITE | Q11 |  |
| `ancrage_4h_et` | `18:00` | `18:00` · `00:00` | CHOIX | Q16 |  |

## setup_htf

| Paramètre | Défaut | Plage de test | Statut | Q | Note |
|---|---|---|---|---|---|
| `gap_min_points` | `0.25` | `0.25` · `2` · `5` | PROPOSITION | Q5 |  |
| `c3_regle` | `close_inside` | `close_inside` · `sweep_c2` · `sweep_c2+wick` | EXPLICITE | Q3 | close_inside : c(C3) < h(C2) pour un FVG haussier |
| `c3_wick_min` | `0.3` | `0.3` · `0.5` | PROPOSITION | Q3 | utilisé seulement si c3_regle contient wick |
| `c2_displacement_atr_k` | `0` | `0` · `0.75` · `1.0` · `1.5` | PROPOSITION | Q4 | 0 = filtre désactivé ; corps(C2) >= k * ATR14(HTF) |
| `c2_body_ratio_min` | `0` | `0` · `0.5` · `0.7` | PROPOSITION | Q4 |  |
| `consommer_si_gap_touche` | `True` | `True` · `False` | PROPOSITION | Q19 |  |

## timing

| Paramètre | Défaut | Plage de test | Statut | Q | Note |
|---|---|---|---|---|---|
| `w1_actif` | `True` | `True` · `False` | EXPLICITE | Q6 |  |
| `w1_minutes_avant_cloture` | `{"15": 4, "60": 10, "240": 30}` | `{"15": 2}` · `{"15": 6}` · `{"60": 5}` | EXPLICITE (15 et 60) / PROPOSITION (240) | Q6 |  |
| `w1_distance_c2_frac` | `0.25` | `0` · `0.15` · `0.25` · `0.5` | PROPOSITION | Q7 | |prix - extrême(C2)| >= frac * range(C2) |
| `w2_actif` | `True` | `True` · `False` | EXPLICITE | Q6 |  |
| `w2_flip_requis` | `False` | `False` · `True` | PROPOSITION | Q6 |  |
| `sortie_forcee` | `cloture_C5` | `cloture_C4` · `cloture_C5` · `jamais` | PROPOSITION | Q10 |  |

## entree_ltf

| Paramètre | Défaut | Plage de test | Statut | Q | Note |
|---|---|---|---|---|---|
| `modeles` | `["IFVG", "CISD"]` | `["IFVG"]` · `["CISD"]` · `["IFVG", "CISD", "OB"]` · `["CISD_OPEN"]` | EXPLICITE (V2) | Q8 |  |
| `fractal_n` | `2` | `1` · `2` · `3` | PROPOSITION | Q8 |  |
| `fenetre_structure_debut` | `ouverture_C3` | `ouverture_C3` · `ouverture_C2` | PROPOSITION | Q8 | début de la fenêtre où l'on cherche swings / FVG LTF ; il parle de la structure « within that third candle » |
| `ifvg_min_points` | `0.25` | `0.25` · `1` · `2` | PROPOSITION | Q8 |  |
| `type_ordre` | `marche_cloture` | `marche_cloture` · `limite_zone` | EXPLICITE (les deux sont utilisés) | Q9 |  |

## sortie

| Paramètre | Défaut | Plage de test | Statut | Q | Note |
|---|---|---|---|---|---|
| `tp_profondeur` | `0` | `0` · `0.25` · `0.5` · `1.0` | CONTRADICTOIRE → défaut sur V3 | Q1 | 0 = bord proche, 1 = comblement total |
| `stop_mode` | `TP_FIRST` | `TP_FIRST` · `STRUCTURE` · `C3_EXTREME` | CONTRADICTOIRE | Q2 |  |
| `stop_buffer_ticks` | `2` | `0` · `2` · `4` | PROPOSITION | Q2 |  |
| `rr` | `1.0` | `1.0` | EXPLICITE | — | non optimisé : c'est une règle du modèle |
| `distance_tp_min_points` | `{"15": 8, "60": 15, "240": 25}` | `{"15": 5}` · `{"15": 12}` · `{"15": 20}` | PROPOSITION | Q5 |  |
| `be_a_R` | `null` | `null` · `0.5` · `0.7` | PROPOSITION | Q14 | null = pas de break-even |
| `grand_range_points_1h` | `150` | `100` · `150` · `200` · `null` | EXPLICITE | Q15 | au-delà : entrée seulement en limite à 50 % du range de C3 ; null = règle désactivée |

## couts

| Paramètre | Défaut | Plage de test | Statut | Q | Note |
|---|---|---|---|---|---|
| `commission_aller_retour_usd` | `4.5` | `4.5` | PROPOSITION | Q18 | à remplacer par tes frais réels |
| `slippage_ticks_marche_et_stop` | `1` | `0` · `1` · `2` | PROPOSITION | Q18 |  |
| `limite_trade_through_ticks` | `1` | `0` · `1` | CHOIX | Q18 | une limite n'est remplie que si le prix la dépasse d'1 tick |
| `meme_bougie_sl_tp` | `SL_dabord` | `SL_dabord` | CHOIX | Q18 | hypothèse pessimiste en 1 min ; affinable avec des données 1 s |
