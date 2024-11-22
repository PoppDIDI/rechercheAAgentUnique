# solver.py

import heapq
import random

class Noeud:
    def __init__(self, grille, parent=None, g=0, h=0):
        self.grille = grille  # état du puzzle
        self.parent = parent  # parent du nœud (pour retrouver le chemin)
        self.g = g  # coût depuis le départ
        self.h = h  # heuristique
        self.f = g + h  # coût total f = g + h

    def __lt__(self, autre):
        return self.f < autre.f


def distance_manhattan(grille, taille):
    distance = 0
    for y in range(taille):
        for x in range(taille):
            tuile = grille[y][x]
            if tuile is None:
                continue
            cible_x = (tuile - 1) % taille
            cible_y = (tuile - 1) // taille
            distance += abs(x - cible_x) + abs(y - cible_y)
    return distance


def est_resolu(grille, taille):
    objectif = list(range(1, taille * taille)) + [None]
    return [tuile for ligne in grille for tuile in ligne] == objectif


def trouver_trou(grille):
    for y in range(len(grille)):
        for x in range(len(grille[0])):
            if grille[y][x] is None:
                return x, y
    return -1, -1


def a_star(grille_initiale, taille, max_swaps):
    h = distance_manhattan(grille_initiale, taille)
    noeud_initial = Noeud(grille_initiale, g=0, h=h)
    
    open_list = []
    heapq.heappush(open_list, noeud_initial)
    
    closed_list = set()
    
    while open_list:
        courant = heapq.heappop(open_list)
        
        if est_resolu(courant.grille, taille):
            solution = []
            while courant:
                solution.append(courant.grille)
                courant = courant.parent
            return solution[::-1]
        
        closed_list.add(tuple(tuple(ligne) for ligne in courant.grille))
        
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = trouver_trou(courant.grille)
            nx, ny = x + direction[0], y + direction[1]
            
            if 0 <= nx < taille and 0 <= ny < taille:
                grille_successeur = [ligne.copy() for ligne in courant.grille]
                grille_successeur[y][x], grille_successeur[ny][nx] = grille_successeur[ny][nx], grille_successeur[y][x]
                
                if tuple(tuple(ligne) for ligne in grille_successeur) in closed_list:
                    continue
                
                g_successeur = courant.g + 1
                h_successeur = distance_manhattan(grille_successeur, taille)
                successeur = Noeud(grille_successeur, parent=courant, g=g_successeur, h=h_successeur)
                
                heapq.heappush(open_list, successeur)
    
    return None


def generer_etat_aleatoire(taille, max_swaps):
    grille = list(range(1, taille * taille)) + [None]
    for _ in range(max_swaps):
        random.shuffle(grille)
    return [grille[i:i+taille] for i in range(0, len(grille), taille)]


def resoudre_puzzle():
    taille = 3
    
    etat_0_swap = generer_etat_aleatoire(taille, 0)
    print("Résolution avec 0-swap:")
    solution_0_swap = a_star(etat_0_swap, taille, max_swaps=0)
    if solution_0_swap:
        for etat in solution_0_swap:
            for ligne in etat:
                print(ligne)
            print("------")
    else:
        print("Pas de solution trouvée pour 0-swap.")
    
    etat_10_swap = generer_etat_aleatoire(taille, 10)
    print("Résolution avec 10-swap:")
    solution_10_swap = a_star(etat_10_swap, taille, max_swaps=10)
    if solution_10_swap:
        for etat in solution_10_swap:
            for ligne in etat:
                print(ligne)
            print("------")
    else:
        print("Pas de solution trouvée pour 10-swap.")


