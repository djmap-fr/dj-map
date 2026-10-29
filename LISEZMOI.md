# DJ Map — mise à jour automatique des dates

Un « robot » (GitHub Actions) lance `update_dates.py` chaque matin. Le script demande les dates à Ticketmaster et écrit `events.json`. La carte (hébergée sur GitHub Pages) lit ce fichier. Après l'installation, tu n'as plus rien à faire.

## Installation (une seule fois)

1. **Clé Ticketmaster (gratuite, immédiate)** : crée un compte sur https://developer.ticketmaster.com puis copie ta « Consumer Key » (dans « My Apps »).
2. **Compte GitHub** : https://github.com (gratuit). Crée un dépôt **public** nommé `dj-map`.
3. **Envoie les fichiers** : « Add file » > « Upload files », glisse tout le contenu du dossier. Le dossier caché `.github` ne passe parfois pas : dans ce cas « Add file » > « Create new file », nom `.github/workflows/update.yml`, colle le contenu du fichier.
4. **Ajoute la clé en secret** : Settings > Secrets and variables > Actions > « New repository secret ». Nom : `TICKETMASTER_KEY`, valeur : ta clé.
5. **Active le site** : Settings > Pages > « Deploy from a branch », branche `main`, dossier `/ (root)`. Adresse : `https://TON-PSEUDO.github.io/dj-map/`.
6. **Premier lancement** : onglet Actions > « Mise à jour des dates » > « Run workflow ».

## À savoir
- Ticketmaster ne couvre pas tous les clubs ni tous les DJ. `manual_events.json` contient des dates ajoutées à la main (festivals, avec leur lien officiel) ; tu peux y en ajouter d'autres.
- Le script ne garde un artiste que si son nom est identique : mieux vaut une date manquante qu'une fausse.
- Ajouter un DJ : son nom dans `djs.json` et sa fiche (nom, style, biographie) dans `index.html`.
