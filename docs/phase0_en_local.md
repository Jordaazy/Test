# Lancer la Phase 0 sur ton ordinateur (plan B)

À utiliser seulement si YouTube bloque la collecte depuis le serveur cloud
(« Sign in to confirm you're not a bot »). Durée : ~20 min d'installation + 30 à 60 min de collecte
(l'ordinateur doit rester allumé et connecté ; on peut s'arrêter et reprendre).

---

## Étape 1 — Installer Python (3.10 ou plus)

**Windows**
1. Va sur https://www.python.org/downloads/ et clique sur le gros bouton « Download Python 3.x ».
2. Lance le fichier téléchargé.
3. **Important** : en bas de la première fenêtre, coche **« Add python.exe to PATH »**, puis clique **« Install Now »**.

**Mac**
1. Va sur https://www.python.org/downloads/ et télécharge la version macOS.
2. Ouvre le `.pkg` et suis l'installation (Continuer → Accepter → Installer).

## Étape 2 — Installer Node.js (version 22 ou plus)

yt-dlp en a besoin pour décoder les protections JavaScript de YouTube.

1. Va sur https://nodejs.org/ et télécharge la version **LTS**.
2. Installe-la avec les options par défaut (Windows : Next → Next → Install ; Mac : `.pkg`).

## Étape 3 — Installer Git

**Windows** : https://git-scm.com/download/win → télécharge « Git for Windows », installe avec les options
par défaut (il inclut « Git Credential Manager », qui gérera la connexion à GitHub).

**Mac** : rien à télécharger. Git sera proposé automatiquement à l'étape 4 : si une fenêtre
« Les outils de développement en ligne de commande sont requis » apparaît, clique **Installer**,
attends la fin, puis relance la commande.

## Étape 4 — Ouvrir un terminal et vérifier

**Windows** : menu Démarrer → tape `PowerShell` → ouvre **Windows PowerShell**.
**Mac** : `Cmd + Espace` → tape `Terminal` → Entrée.

> Ferme et rouvre le terminal après les installations, sinon il ne « voit » pas les nouveaux programmes.

Tape ces commandes une par une (Entrée après chacune) :

| Windows | Mac | Résultat attendu |
|---|---|---|
| `py --version` | `python3 --version` | `Python 3.10` ou plus |
| `node --version` | `node --version` | `v22...` ou plus |
| `git --version` | `git --version` | `git version ...` |

Si une commande répond « introuvable / not found » : réinstalle le programme concerné (sous Windows,
vérifie la case « Add python.exe to PATH ») puis rouvre le terminal.

## Étape 5 — Télécharger le projet

Même commandes sur Windows et Mac :

```
cd ~
git clone https://github.com/Jordaazy/Test.git
cd Test
git checkout claude/amas-pft-phase0
```

Le dossier du projet est maintenant dans ton dossier personnel, sous le nom `Test`.

## Étape 6 — Installer les dépendances (dans un environnement isolé)

**Windows**
```
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

**Mac**
```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Attendu : quelques lignes de téléchargement, puis `Successfully installed ... yt-dlp ...`.

## Étape 7 — Faire un essai sur 3 vidéos (~1 min)

**Windows** : `.venv\Scripts\python scripts\run_phase0.py --test`
**Mac** : `.venv/bin/python scripts/run_phase0.py --test`

À la fin, un **RÉSUMÉ PHASE 0** s'affiche. L'essai est bon si tu vois :
`Avec métadonnées complètes (dates) : 3` et `Transcriptions propres (.md) : 3`.

## Étape 8 — Lancer la collecte complète (30 à 60 min)

**Windows** : `.venv\Scripts\python scripts\run_phase0.py`
**Mac** : `.venv/bin/python scripts/run_phase0.py`

- Laisse le terminal ouvert et l'ordinateur allumé (désactive la mise en veille).
- Si ça s'interrompt (coupure, fermeture, erreur), **relance exactement la même commande** :
  elle reprend là où elle s'était arrêtée.
- Si le résumé indique « Incomplet », relance la commande une seconde fois.
- Si tu vois beaucoup d'erreurs `429` ou « not a bot », attends 1 h puis relance avec un rythme plus lent :
  ajoute ` --sleep 4` à la fin de la commande.

Contrôle : ouvre le dossier `Test\data\transcripts` (Windows) ou `Test/data/transcripts` (Mac) ;
il doit contenir des centaines de fichiers `.md` nommés `AAAA-MM-JJ_titre_id.md`.

## Étape 9 — Envoyer les données sur GitHub

1. Indique ton identité à Git (une seule fois) :
   ```
   git config --global user.name "Ton nom"
   git config --global user.email "ton-email@exemple.com"
   ```
2. Enregistre et envoie :
   ```
   git add data
   git commit -m "Phase 0 : données collectées"
   git push
   ```
3. Connexion GitHub au moment du `git push` :
   - **Windows** : une fenêtre « Connect to GitHub » s'ouvre → **Sign in with your browser** → autorise.
   - **Mac** : Git demande `Username` puis `Password`. Le mot de passe GitHub **ne marche pas** ici,
     il faut un *jeton* :
     1. Sur https://github.com/settings/personal-access-tokens/new : nom « phase0 »,
        expiration 7 jours, *Repository access* → **Only select repositories** → `Jordaazy/Test`,
        *Permissions* → **Contents : Read and write** → **Generate token**.
     2. Copie le jeton (il commence par `github_pat_`).
     3. Dans le terminal : `Username` = ton nom d'utilisateur GitHub, `Password` = colle le jeton
        (rien ne s'affiche quand tu colles, c'est normal) → Entrée.

Le push est réussi si la dernière ligne ressemble à
`claude/amas-pft-phase0 -> claude/amas-pft-phase0`. Préviens Claude : la suite (classement, ordre de lecture)
se fait à partir de là.

---

## En cas de problème

| Message | Solution |
|---|---|
| `'py' n'est pas reconnu` / `python3: command not found` | Python mal installé ou pas dans le PATH → étape 1, puis rouvrir le terminal |
| `No supported JavaScript runtime` | Node.js absent ou trop ancien → étape 2 (version 22+), rouvrir le terminal |
| `Sign in to confirm you're not a bot` | attendre 1 h, relancer avec `--sleep 4` ; sinon prévenir Claude |
| `HTTP Error 429` | trop de requêtes → même solution |
| `error: externally-managed-environment` | tu as oublié `.venv` : refais l'étape 6 exactement |
| `fatal: not a git repository` | tu n'es pas dans le dossier : tape `cd ~/Test` |
| `Échec à l'étape ...` | copie les 20 dernières lignes du terminal à Claude |
