import pygame
import random

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
TAILLE_ECRAN = 600
TAILLE_TUILE = TAILLE_ECRAN // 3
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)

# Création de la fenêtre
ecran = pygame.display.set_mode((TAILLE_ECRAN, TAILLE_ECRAN))
pygame.display.set_caption("Puzzle 3x3")

# Fonction pour générer une grille initiale
def generer_grille():
    tuiles = list(range(1, 9)) + [None]  # Numéros de 1 à 8, plus une case vide
    random.shuffle(tuiles)  # Mélanger les numéros
    return [tuiles[i:i+3] for i in range(0, len(tuiles), 3)]  # Créer une grille 3x3

# Fonction pour dessiner la grille
def dessiner_grille(ecran, grille):
    ecran.fill(BLANC)
    font = pygame.font.Font(None, 100)
    for y, ligne in enumerate(grille):
        for x, tuile in enumerate(ligne):
            if tuile is not None:
                # Dessiner chaque tuile
                rect = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
                pygame.draw.rect(ecran, BLEU, rect)
                pygame.draw.rect(ecran, NOIR, rect, 2)
                texte = font.render(str(tuile), True, BLANC)
                texte_rect = texte.get_rect(center=rect.center)
                ecran.blit(texte, texte_rect)
            else:
                # Dessiner le trou (vide)
                pygame.draw.rect(ecran, NOIR, (x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE), 2)

# Fonction pour trouver la position de la case vide
def trouver_trou(grille):
    for y, ligne in enumerate(grille):
        for x, tuile in enumerate(ligne):
            if tuile is None:
                return x, y

# Fonction pour déplacer une tuile
def bouger_tuile(grille, trou, direction):
    x, y = trou
    dx, dy = direction
    nx, ny = x + dx, y + dy
    if 0 <= nx < 3 and 0 <= ny < 3:
        grille[y][x], grille[ny][nx] = grille[ny][nx], grille[y][x]
        return nx, ny
    return trou

# Fonction pour vérifier si le puzzle est résolu
def est_resolu(grille):
    solution = list(range(1, 9)) + [None]
    return [tuile for ligne in grille for tuile in ligne] == solution

# Initialisation
grille = generer_grille()
trou = trouver_trou(grille)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                trou = bouger_tuile(grille, trou, (0, -1))  # Déplace la tuile du haut vers le bas
            elif event.key == pygame.K_DOWN:
                trou = bouger_tuile(grille, trou, (0, 1))  # Déplace la tuile du bas vers le haut
            elif event.key == pygame.K_LEFT:
                trou = bouger_tuile(grille, trou, (-1, 0))  # Déplace la tuile de gauche vers la droite
            elif event.key == pygame.K_RIGHT:
                trou = bouger_tuile(grille, trou, (1, 0))  # Déplace la tuile de droite vers la gauche

    # Dessiner la grille à chaque itération
    dessiner_grille(ecran, grille)
    pygame.display.flip()

    # Vérifier si le puzzle est résolu
    if est_resolu(grille):
        print("Bravo ! Vous avez résolu le puzzle !")
        running = False

# Quitter Pygame
pygame.quit()
