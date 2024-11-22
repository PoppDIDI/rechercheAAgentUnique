# Jeu de Puzzle Glissant (3x3 et 4x4)

Un jeu de puzzle glissant développé avec Python et Pygame. L'utilisateur peut choisir entre un puzzle de 3x3 ou 4x4 et configurer le nombre de déplacements \( k \) avant de pouvoir effectuer un swap. Après chaque cycle \( k \), un swap unique est autorisé.

---

## Fonctionnalités

- **Choix de la taille du puzzle** : L'utilisateur peut sélectionner entre un puzzle de **3x3** ou **4x4**.
- **Personnalisation des déplacements (\( k \))** : L'utilisateur peut entrer un nombre \( k \) pour déterminer combien de déplacements sont nécessaires avant qu'un swap soit autorisé.
- **Interface utilisateur intuitive** :
  - Un menu pour configurer les paramètres (taille du puzzle et \( k \)).
  - Les informations sur les déplacements et instructions sont clairement affichées au-dessus du puzzle.

---


### Utilisation
1. **Menu de configuration** :
   - Sélectionnez *3x3* ou *4x4* en cliquant sur les cases correspondantes.
   - Entrez un nombre dans la zone de texte pour configurer \( k \).
   - Cliquez sur "Valider" pour démarrer le jeu.
2. **Jeu** :
   - Déplacez les tuiles adjacentes à la case vide en utilisant les **flèches** ou **clic gauche**.
   - Après \( k \) déplacements, vous pouvez effectuer un swap en cliquant sur deux tuiles.
   - Résolvez le puzzle en plaçant les numéros dans l'ordre croissant.

---

## Fonctionnalités Techniques
  - Flèches pour déplacer les tuiles.
  - Clic souris pour déplacer les tuiles ou effectuer un swap.

---

## Technologies Utilisées

- **Python 3** : Langage principal.
- **Pygame** : Bibliothèque pour gérer l'affichage graphique, les événements oriente-souris, et l'interaction utilisateur.
