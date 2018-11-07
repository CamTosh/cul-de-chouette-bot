# Cul De Chouette Discord Bot

Warning, this Cul de Chouette Bot is Français !

- Python 3.5

`python3 -m pip install -r requirements.txt`

Tu l'installes, tu le lances "normalement" (avec un fichier de conf en ".ini",
faut suivre la doc de CmdBot)

## Les règles

Pour le moment, on utilise les règles les plus simples possibles. À savoir, les
combinaisons de base :

* Chouette,
* Velute,
* Chouette Velute
* Cul de Chouette
* Suite (dans le cadre de la suite, on doit dire "grelotte ça picote".
  Normalement, il ne peut pas y avoir d'ex-aequo.)

Les autres règles seront (peut-être) implémentées dans le futur. Si tu es sage.

## Commandes

Les commandes indiquées comme *direct* doivent être précédées du nom du bot. Exemple : `!qdc init`

> Les commandes indiquées comme "admin" ne peuvent être lancées que par un des admins définis dans la configuration.

* `!qdc init` : [*direct*, *admin*] - démarre les inscriptions au jeu.
* `!qdc moi` : s'inscrire au jeu
* `!qdc start` ou `commencer`: [*direct*, *admin*] - une fois les inscriptions terminées, on démarre
  le jeu.
* `!qdc roll` ou `jouer`: le joueur dont c'est le tour lance les dés.
* `!qdc scores`: indique les scores des joueurs.
* `!qdc status` ou `statut`: [*direct*] - donne le statut du jeu et le score.
* `!qdc stop`: [*direct*, *admin*] - arrête la partie
