import random
########################################## IA intermediaire ##########################################
def trouver_coordonnees_ciblees(plateau_cible) :
    liste_coord_ciblees = []

    for nb_ligne in range(len(plateau_cible)) :
        for nb_colonne in range(len(plateau_cible[0])) :
            if plateau_cible[nb_ligne][nb_colonne].get_statut() != None :
                liste_coord_ciblees.append((nb_ligne, nb_colonne))

    return liste_coord_ciblees

def trouver_coord_case_adjacente(plateau_cible) :
    for nb_ligne in range(len(plateau_cible)) : 
        for nb_colonne in range(len(plateau_cible[0])) : 
            # Si la case a été touchée : cibler les cases adjacentes.
            if plateau_cible[nb_ligne][nb_colonne].get_statut() == "hit" :
                liste_coord_adjacentes = [
                    (nb_ligne-1, nb_colonne),
                    (nb_ligne+1, nb_colonne),
                    (nb_ligne, nb_colonne-1),
                    (nb_ligne, nb_colonne+1)
                ]
                for couple_coord in liste_coord_adjacentes :
                    try : 
                        # on ne veut pas de coordonnées negatives !!!
                        if couple_coord[0]<0 or couple_coord[1]<0 :
                            raise ValueError
                        
                        # Si la case adjacente n'a pas encore ete ciblee, on renvoie ses coordonnees
                        if plateau_cible[couple_coord[0]][couple_coord[1]].get_symbole() == "-" :
                            ligne = couple_coord[0]
                            colonne = couple_coord[1]
                            return ligne, colonne
                    except :
                        pass
    return -1, -1


def cibler_coord_cross_random(plateau_cible, navires) : 
    ## Tir croisé aléatoire
    # A partir du plateau cible => trouver la longueur minimale d'un navire
    longueur_min = min(list(map(lambda navire : navire.get_taille(),navires)))
    liste_coord_ciblee = trouver_coordonnees_ciblees(plateau_cible=plateau_cible)


    # Evitons de tirer sur des coordonnees deja ciblees...
    while True :
        # les facteur a permettent de tirer aleatoirement dans la grille
        # le facteur b, commun aux lignes et colonnes, permet de s'assurer de quadriller la grille selon la taille minimale.
        a_ligne = random.randint(0, len(plateau_cible[0])//2)
        a_colonne = random.randint(0, len(plateau_cible[0])//2)
        b = random.randint(0, longueur_min-1)

        ligne = longueur_min*a_ligne+b
        colonne = longueur_min*a_colonne+b

        if (ligne, colonne) not in liste_coord_ciblee :
            if ligne < len(plateau_cible) and colonne < len(plateau_cible[0]) :
                break
        
    return ligne, colonne



########################################## IA avancé ##########################################

### Verifier le nombre de case deja ciblee
def check_nb_targeted_tile(plateau_cible) :
    nb_targeted_tiles = 0

    for ligne in plateau_cible :
        for tile in ligne :
            if tile.get_statut() is not None :
                nb_targeted_tiles += 1

    return nb_targeted_tiles



### Toutes les configurations possibles

from Scripts.Tools import get_plateau_symbole, afficher_plateau

# Permet de vérifier pour chaque navire qu'il est possible de le placer de facon 'valide' dans le plateau_cible 
def placement_navire_valide(plateau_cible, ligne, colonne, taille, horizontal):
    if horizontal:
        # condition sur la taille du plateau et du navire
        if colonne + taille > len(plateau_cible[0]):
            return False
        
        # vérification pour chaque case qu'elle n'est pas déjà été ratée ou coulée
        for i in range(taille):
            if plateau_cible[ligne][colonne + i].get_symbole() != "-":
                if plateau_cible[ligne][colonne + i].get_statut() != "hit" :
                    return False
                
    else:
        # condition sur la taille du plateau et du navire
        if ligne + taille > len(plateau_cible):
            return False
        
        # vérification pour chaque case qu'elle n'est pas déjà été ratée ou coulée
        for i in range(taille):
            if plateau_cible[ligne + i][colonne].get_symbole() != "-":
                if plateau_cible[ligne + i][colonne].get_statut() != "hit" :
                    return False
                
    return True



# Placement d'un navire dans le plateau_cible (pour une configuration)
def placer_navire(plateau_cible, ligne, colonne, horizontal, navire):
    if horizontal:
        for i in range(navire.get_taille()):
            if plateau_cible[ligne][colonne + i].get_statut() != "hit" :
                plateau_cible[ligne][colonne + i].set_navire(navire)
    else:
        for i in range(navire.get_taille()):
            if plateau_cible[ligne + i][colonne].get_statut() != "hit" :
                plateau_cible[ligne + i][colonne].set_navire(navire)



# On retire le navire du plateau_cible (pour une configuration)
def retirer_navire(grille, ligne, colonne, taille, horizontal):
    if horizontal:
        for i in range(taille):
            if grille[ligne][colonne + i].get_statut() != 'hit' and grille[ligne][colonne + i].get_statut() != 'fail':
                grille[ligne][colonne + i].set_navire(None)
    else:
        for i in range(taille):
            if grille[ligne + i][colonne].get_statut() != 'hit' and grille[ligne + i][colonne].get_statut() != 'fail':
                grille[ligne + i][colonne].set_navire(None)


# Vérification que la configuration suit les critères de validités :
#   - Placement de tous les navires "vivants" => prise en compte des "hits" ("touchés") nécéssaires.
#   - Prise en comptes des cases "touché" => s'assurer de la continuité entre les case navires et "touché" => si le nombre de tile occupée est la bonne, cela veut dire qu'un navire a été superposé à chaque "X" du plateau. 
def configuration_valide(plateau_cible, navires, nb_hits):
    # set de symbole : permet de compter les symbole dans le plateau 
    symboles_navires = {navire.get_symbole() for navire in navires}
    # comptage du nombre de case devant être occupées
    critere_tiles_occupee = sum([navire.get_taille() for navire in navires])
    
    # conversion pour pouvoir chercher les symbole dans le plateau
    plateau_cible_symbole = get_plateau_symbole(plateau_cible)
    nb_cell_navires = 0 
    # Comptage du nomnre de symbole dans le plateau
    for row in plateau_cible_symbole:
        for cell in row:
            if cell in symboles_navires:
                nb_cell_navires += 1

    # Ajout des "hits"
    nb_occuped_tiles = nb_hits + nb_cell_navires
    # Si le 1er critère n'est pas respectés => return False
    if critere_tiles_occupee != nb_occuped_tiles : 
        return False

    return True


# Permet de generer toutes les configurations envisageable pour un plateau cible et une liste de navires.
def generer_configurations(plateau_cible, navires : set):
    configurations = []

    # Vérification des navires coulés à partir du plateau_cible
    # Parcours de toutes les tiles pour identifier les navires coulés en fonction du statut de la tile.
    navires_coules = set()
    nb_hits = 0  # Utile pour les critères de validité des configs

    for row in plateau_cible :
        for tile in row : 
            if tile.get_statut() == "cast" :
                navires_coules = navires_coules.union({tile.get_navire()})

            elif tile.get_statut() == "hit" :
                nb_hits += 1
            

    # Si un ou plusieurs navires ont été coulé, 
    # on les supprime du dict qui va servir a trouver toutes les configuration possible avec les navires restant.
    # navire_bis permet simplement de pouvoir iterer sur navire en modifiant ses element sans obtenir d'erreur 
    navires_bis = deepcopy(navires)
    if len(navires_coules) > 0 :
        for navire_coule in navires_coules :
            for navire in navires_bis :
                if navire == navire_coule : 
                    navires.remove(navire)

    # transformation du set en list pour pouvoir faire de la recursivité
    navires = list(navires)
    # creation d'un plateau vierge pour test

    # Fonction recursive de generation.
    def generer(index):
        if index == len(navires):
            if configuration_valide(plateau_cible, navires, nb_hits):
                afficher_plateau(plateau_cible)
                print("")
                print("")
                # conversion du plateau pour utiliser les symboles 
                # -> plus simple dans le calcul de densité de probabilité
                plateau_cible_symbole = get_plateau_symbole(plateau_cible)
                configurations.append([ligne[:] for ligne in plateau_cible_symbole])
            return

        # Placement du navire dans la configuration
        navire = navires[index]
        taille = navire.get_taille()
        for ligne in range(len(plateau_cible)):
            for colonne in range(len(plateau_cible[0])):
                for horizontal in [True, False]:
                    if placement_navire_valide(plateau_cible, ligne, colonne, taille, horizontal):
                        placer_navire(plateau_cible, ligne, colonne, horizontal, navire)
                        generer(index + 1)
                        retirer_navire(plateau_cible, ligne, colonne, taille, horizontal)

    generer(0)
    return configurations



### Densité de proba
from copy import deepcopy
import numpy as np

# Remplacement des symbole de navire par des 1 et le reste des case par des 0
# Permet ensuite de calculer la densité de probalité pour un plateau_cible
def analyse_config(config):
    res = deepcopy(config)

    for nb_ligne in range(len(config)) : 
        for nb_colonne in range(len(config[nb_ligne])) :
            match config[nb_ligne][nb_colonne] :
                case "-" :
                    res[nb_ligne][nb_colonne] = 0
                case "0" :
                    res[nb_ligne][nb_colonne] = 0
                case "X" :
                    res[nb_ligne][nb_colonne] = 0
                case _ :
                    res[nb_ligne][nb_colonne] = 1
    return np.array(res)


# Generation de la matrice de densité de probabilité
def genere_matrice_proba(all_config : list) : 
    liste_analyse_placement = []

    for config in all_config : 
        liste_analyse_placement.append(analyse_config(config))

    densite_proba_np = sum(liste_analyse_placement)/len(all_config)

    # conversion en list(list) a la place d'un np array
    densite_proba = densite_proba_np.tolist()

    return densite_proba


# Permet de récupérer les coordonnées basées sur la matrice de densité de probabilité
def get_coord_from_matrice_proba(matrice_proba):
    # Identifier le max dans la matrice de densité de proba
    maximum = max(max(ligne) for ligne in matrice_proba)
    ligne, colonne = 0,0

    # Identification des index relatifs à la case ciblée
    for nb_ligne in range(len(matrice_proba)) :
        for nb_colonne in range(len(matrice_proba[nb_ligne])) :
            if maximum == matrice_proba[nb_ligne][nb_colonne] :
                ligne = nb_ligne
                colonne = nb_colonne
                break
        
    return ligne, colonne
