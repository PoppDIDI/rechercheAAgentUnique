import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
TAILLE_ECRAN = 600
TAILLE_TUILE = TAILLE_ECRAN // 3
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)

# Création de la fenêtre
ecran = pygame.display.set_mode((TAILLE_ECRAN, TAILLE_ECRAN))
pygame.display.set_caption("Puzzle 3x3 - K-swap")

# Fonction pour générer une grille initiale
def generer_grille():
    tuiles = list(range(1, 9)) + [None]  # Numéros de 1 à 8, plus une case vide
    random.shuffle(tuiles)  # Mélanger les numéros
    return [tuiles[i:i+3] for i in range(0, len(tuiles), 3)]  # Créer une grille 3x3

# Fonction pour dessiner la grille
def dessiner_grille(ecran, grille, compteur, k, selectionnee=None):
    ecran.fill(BLANC)
    font = pygame.font.Font(None, 50)
    for y, ligne in enumerate(grille):
        for x, tuile in enumerate(ligne):
            rect = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
            if (x, y) == selectionnee:
                pygame.draw.rect(ecran, ROUGE, rect)
            elif tuile is not None:
                pygame.draw.rect(ecran, BLEU, rect)
            pygame.draw.rect(ecran, NOIR, rect, 2)
            if tuile is not None:
                texte = font.render(str(tuile), True, BLANC)
                texte_rect = texte.get_rect(center=rect.center)
                ecran.blit(texte, texte_rect)

    # Afficher les informations du compteur et de k
    texte_deplacement = font.render(f"Déplacements: {compteur}", True, NOIR)
    texte_k = font.render(f"Swaps restants: {k}", True, NOIR)
    ecran.blit(texte_deplacement, (10, 10))
    ecran.blit(texte_k, (10, 60))

# Fonction pour afficher une boîte de dialogue pour entrer \(k\)
def entrer_k(ecran):
    font = pygame.font.Font(None, 50)
    input_rect = pygame.Rect(150, 250, 300, 50)
    actif = True
    texte = ""
    while actif:
        ecran.fill(BLANC)
        texte_titre = font.render("Entrez le nombre de swaps (k):", True, NOIR)
        ecran.blit(texte_titre, (50, 150))
        pygame.draw.rect(ecran, NOIR, input_rect, 2)
        texte_surface = font.render(texte, True, NOIR)
        ecran.blit(texte_surface, (input_rect.x + 10, input_rect.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Appuyer sur Entrée pour valider
                    try:
                        return int(texte)  # Retourner \( k \) comme entier
                    except ValueError:
                        texte = ""  # Réinitialiser si la valeur n'est pas valide
                elif event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]  # Supprimer le dernier caractère
                else:
                    texte += event.unicode  # Ajouter le caractère tapé

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

# Fonction pour convertir la position de la souris en coordonnées de grille
def position_souris_en_grille(pos):
    x, y = pos
    return x // TAILLE_TUILE, y // TAILLE_TUILE

# Initialisation
grille = generer_grille()
trou = trouver_trou(grille)
selectionnee = None  # Position de la tuile sélectionnée pour k-swap

# Demander le nombre initial de swaps
k = entrer_k(ecran)
compteur_deplacement = 0

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Déplacement avec les flèches du clavier
            if event.key == pygame.K_UP:
                trou = bouger_tuile(grille, trou, (0, -1))  # Déplace la tuile du haut vers le bas
                compteur_deplacement += 1
            elif event.key == pygame.K_DOWN:
                trou = bouger_tuile(grille, trou, (0, 1))  # Déplace la tuile du bas vers le haut
                compteur_deplacement += 1
            elif event.key == pygame.K_LEFT:
                trou = bouger_tuile(grille, trou, (-1, 0))  # Déplace la tuile de gauche vers la droite
                compteur_deplacement += 1
            elif event.key == pygame.K_RIGHT:
                trou = bouger_tuile(grille, trou, (1, 0))  # Déplace la tuile de droite vers la gauche
                compteur_deplacement += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                x, y = position_souris_en_grille(event.pos)
                if selectionnee is None:
                    # Si la tuile cliquée est adjacente au trou, déplacer la tuile
                    if (abs(x - trou[0]) == 1 and y == trou[1]) or (abs(y - trou[1]) == 1 and x == trou[0]):
                        trou = bouger_tuile(grille, trou, (x - trou[0], y - trou[1]))
                    else:
                        selectionnee = (x, y)
                elif selectionnee == (x, y):
                    selectionnee = None
                elif k > 0:
                    # Effectuer un swap uniquement si k > 0
                    sel_x, sel_y = selectionnee
                    grille[sel_y][sel_x], grille[y][x] = grille[y][x], grille[sel_y][sel_x]
                    selectionnee = None
                    k -= 1  # Décrémente le compteur de swaps restants

    # Dessiner la grille
    dessiner_grille(ecran, grille, compteur_deplacement, k, selectionnee)
    pygame.display.flip()

    # Vérifier si le puzzle est résolu
    if est_resolu(grille):
        print("Bravo ! Vous avez résolu le puzzle !")
        running = False

# Quitter Pygame
pygame.quit()
