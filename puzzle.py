import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Configuration de base
TAILLE_ECRAN = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

# Fonction pour générer une grille initiale
def generer_grille(taille):
    tuiles = list(range(1, taille * taille)) + [None]
    random.shuffle(tuiles)
    return [tuiles[i:i+taille] for i in range(0, len(tuiles), taille)]

# Fonction pour trouver la position de la case vide
def trouver_trou(grille):
    for y, ligne in enumerate(grille):
        for x, tuile in enumerate(ligne):
            if tuile is None:
                return x, y

# Interface pour choisir la taille et le nombre de déplacements \( k \)
def afficher_interface(ecran):
    font = pygame.font.Font(None, 50)
    input_rect = pygame.Rect(250, 400, 150, 50)
    checkbox_3x3 = pygame.Rect(100, 100, 30, 30)
    checkbox_4x4 = pygame.Rect(100, 200, 30, 30)
    bouton_valider = pygame.Rect(250, 500, 150, 50)

    taille_selectionnee = 3
    texte_k = ""
    actif = True

    while actif:
        ecran.fill(BLANC)
        texte_titre = font.render("Les dimensions", True, NOIR)
        ecran.blit(texte_titre, (150, 20))

        # Dessiner les options de taille
        pygame.draw.rect(ecran, NOIR, checkbox_3x3, 2)
        pygame.draw.rect(ecran, NOIR, checkbox_4x4, 2)
        if taille_selectionnee == 3:
            pygame.draw.rect(ecran, VERT, checkbox_3x3)
        else:
            pygame.draw.rect(ecran, VERT, checkbox_4x4)

        texte_3x3 = font.render("3x3", True, NOIR)
        texte_4x4 = font.render("4x4", True, NOIR)
        ecran.blit(texte_3x3, (150, 90))
        ecran.blit(texte_4x4, (150, 190))

        # Zone de saisie pour \( k \)
        texte_k_label = font.render("Nombre de déplacements (k):", True, NOIR)
        pygame.draw.rect(ecran, NOIR, input_rect, 2)
        texte_k_surface = font.render(texte_k, True, NOIR)
        ecran.blit(texte_k_label, (50, 360))
        ecran.blit(texte_k_surface, (input_rect.x + 10, input_rect.y + 10))

        # Bouton valider
        pygame.draw.rect(ecran, BLEU, bouton_valider)
        texte_valider = font.render("Valider", True, BLANC)
        texte_valider_rect = texte_valider.get_rect(center=bouton_valider.center)
        ecran.blit(texte_valider, texte_valider_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if checkbox_3x3.collidepoint(event.pos):
                        taille_selectionnee = 3
                    elif checkbox_4x4.collidepoint(event.pos):
                        taille_selectionnee = 4
                    elif bouton_valider.collidepoint(event.pos):
                        try:
                            k = int(texte_k)
                            if k > 0:
                                return taille_selectionnee, k
                        except ValueError:
                            pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    texte_k = texte_k[:-1]
                else:
                    texte_k += event.unicode

# Fonction pour dessiner la grille
# Fonction pour dessiner la grille
def dessiner_grille(ecran, grille, taille, compteur, k, selectionnee=None):
    # Recalculer la taille des tuiles en fonction de la hauteur de la barre de texte
    HAUTEUR_BARRE_TEXTE = 100  # Espace dédié au texte en haut
    TAILLE_TUILE = (TAILLE_ECRAN - HAUTEUR_BARRE_TEXTE) // taille

    ecran.fill(BLANC)

    # Dessiner la barre supérieure pour les textes
    pygame.draw.rect(ecran, NOIR, (0, 0, TAILLE_ECRAN, HAUTEUR_BARRE_TEXTE))

    # Afficher les informations du compteur et de k
    font = pygame.font.Font(None, 40)
    texte_deplacement = font.render(f"Déplacements: {compteur}/{k}", True, BLANC)
    texte_instruction = font.render(
        "Swap possible !" if compteur == k else "Déplacez les tuiles !", 
        True, VERT if compteur == k else BLANC
    )
    ecran.blit(texte_deplacement, (10, 10))  # Position du texte des déplacements
    ecran.blit(texte_instruction, (10, 50))  # Position des instructions

    # Dessiner la grille en dessous
    for y, ligne in enumerate(grille):
        for x, tuile in enumerate(ligne):
            rect = pygame.Rect(
                x * TAILLE_TUILE, 
                y * TAILLE_TUILE + HAUTEUR_BARRE_TEXTE,  # Décalage vers le bas
                TAILLE_TUILE, 
                TAILLE_TUILE
            )
            if (x, y) == selectionnee:
                pygame.draw.rect(ecran, ROUGE, rect)
            elif tuile is not None:
                pygame.draw.rect(ecran, BLEU, rect)
            pygame.draw.rect(ecran, NOIR, rect, 2)
            if tuile is not None:
                texte = font.render(str(tuile), True, BLANC)
                texte_rect = texte.get_rect(center=rect.center)
                ecran.blit(texte, texte_rect)


# Fonction principale pour le jeu
def jeu_principal(taille, k):
    grille = generer_grille(taille)
    trou = trouver_trou(grille)
    selectionnee = None
    compteur_deplacement = 0
    swap_effectue = False

    def bouger_tuile(grille, trou, direction):
        x, y = trou
        dx, dy = direction
        nx, ny = x + dx, y + dy
        if 0 <= nx < taille and 0 <= ny < taille:
            grille[y][x], grille[ny][nx] = grille[ny][nx], grille[y][x]
            return nx, ny
        return trou

    def est_resolu(grille):
        solution = list(range(1, taille * taille)) + [None]
        return [tuile for ligne in grille for tuile in ligne] == solution

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if compteur_deplacement < k or (compteur_deplacement == 0 and swap_effectue):
                    if event.key == pygame.K_UP:
                        trou = bouger_tuile(grille, trou, (0, -1))
                        compteur_deplacement += 1
                    elif event.key == pygame.K_DOWN:
                        trou = bouger_tuile(grille, trou, (0, 1))
                        compteur_deplacement += 1
                    elif event.key == pygame.K_LEFT:
                        trou = bouger_tuile(grille, trou, (-1, 0))
                        compteur_deplacement += 1
                    elif event.key == pygame.K_RIGHT:
                        trou = bouger_tuile(grille, trou, (1, 0))
                        compteur_deplacement += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = position_souris_en_grille(event.pos, taille)
                if compteur_deplacement < k or (compteur_deplacement == 0 and swap_effectue):
                    if (abs(x - trou[0]) == 1 and y == trou[1]) or (abs(y - trou[1]) == 1 and x == trou[0]):
                        trou = bouger_tuile(grille, trou, (x - trou[0], y - trou[1]))
                        compteur_deplacement += 1
                elif compteur_deplacement == k and not swap_effectue:
                    if selectionnee is None:
                        selectionnee = (x, y)
                    elif selectionnee == (x, y):
                        selectionnee = None
                    else:
                        sel_x, sel_y = selectionnee
                        grille[sel_y][sel_x], grille[y][x] = grille[y][x], grille[sel_y][sel_x]
                        selectionnee = None
                        swap_effectue = True
                        compteur_deplacement = 0
                        swap_effectue = False

        dessiner_grille(ecran, grille, taille, compteur_deplacement, k, selectionnee)
        pygame.display.flip()

        if est_resolu(grille):
            print("Bravo ! Vous avez résolu le puzzle !")
            running = False
 
# Fonction pour convertir la position de la souris en coordonnées de grille
def position_souris_en_grille(pos, taille):
    TAILLE_TUILE = TAILLE_ECRAN // taille
    x, y = pos
    return x // TAILLE_TUILE, y // TAILLE_TUILE

# Démarrage du programme
ecran = pygame.display.set_mode((TAILLE_ECRAN, TAILLE_ECRAN))
taille, k = afficher_interface(ecran)
jeu_principal(taille, k)
pygame.quit()
