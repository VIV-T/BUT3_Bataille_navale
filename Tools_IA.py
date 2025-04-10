### Toutes les configurations possibles

from Tools import get_plateau_symbole, afficher_plateau


def est_valide(plateau_cible, ligne, colonne, taille, horizontal):
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


# Placement d'un navire dans le plateau_cible (pour une config)
def placer_navire(plateau_cible, ligne, colonne, horizontal, navire):
    if horizontal:
        for i in range(navire.get_taille()):
            if plateau_cible[ligne][colonne + i].get_statut() != "hit" :
                plateau_cible[ligne][colonne + i].set_navire(navire)
    else:
        for i in range(navire.get_taille()):
            if plateau_cible[ligne + i][colonne].get_statut() != "hit" :
                plateau_cible[ligne + i][colonne].set_navire(navire)



# On retire le navire du plateau_cible 
def retirer_navire(grille, row, col, taille, horizontal):
    if horizontal:
        for i in range(taille):
            if grille[row][col + i].get_statut() != 'hit' and grille[row][col + i].get_statut() != 'fail':
                grille[row][col + i].set_navire(None)
    else:
        for i in range(taille):
            if grille[row + i][col].get_statut() != 'hit' and grille[row + i][col].get_statut() != 'fail':
                grille[row + i][col].set_navire(None)


# Vérification que la configuration suit les cirtères de validités :
#   - Placement de tous les navires "vivants" => prise en compte des "hits" ("touchés") nécéssaires.
#   - Prise en comptes des cases "touché" => s'assurer de la continuité entre les case navires et "touché" => si le nombre de tile occupée est la bonne, cela veut dire qu'un navire a été superposé à chaque "X" du plateau. 
def configuration_valide(plateau_cible, navires, nb_hits):
    ### 1er critère
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

    ### 2nd critère 


    return True



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
            

    # Si un ou plusieurs navires ont été coulé, les supprime du dict qui va servir a trouver toutes les configuration possible avec les navires restant.
    if len(navires_coules) > 0 :
        for navire in navires_coules :
            navires.remove(navire)

    # transformation du set en list pour pouvoir faire de la recursivité
    navires = list(navires)
    # creation d'un plateau vierge pour test

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

        navire = navires[index]
        taille = navire.get_taille()
        for ligne in range(len(plateau_cible)):
            for colonne in range(len(plateau_cible[0])):
                for horizontal in [True, False]:
                    if est_valide(plateau_cible, ligne, colonne, taille, horizontal):
                        placer_navire(plateau_cible, ligne, colonne, horizontal, navire)
                        generer(index + 1)
                        retirer_navire(plateau_cible, ligne, colonne, taille, horizontal)

    generer(0)
    return configurations



### Densité de proba
from copy import deepcopy
import numpy as np

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



def genere_matrice_proba(all_config : list) : 
    liste_analyse_placement = []

    for config in all_config : 
        liste_analyse_placement.append(analyse_config(config))

    densite_proba_np = sum(liste_analyse_placement)/len(all_config)

    # conversion en list(list) a la place d'un np array
    densite_proba = densite_proba_np.tolist()

    return densite_proba


def get_ligne_colonne_matrice_proba(matrice_proba):
    # Identifier le max dans la matrice de densité de proba
    maximum = max(max(ligne) for ligne in matrice_proba)

    # Identification des index relatifs à la case ciblée
    for nb_ligne in range(len(matrice_proba)) :
        for nb_colonne in range(len(matrice_proba[nb_ligne])) :
            if maximum == matrice_proba[nb_ligne][nb_colonne] :
                ligne = nb_ligne
                colonne = nb_colonne
                break
        
    return ligne, colonne



### Imports additionnels
from Navire import FactoryNavire
from Grille import Grille
from Strategie import FactoryStrategie

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__=="__main__" :
    ### SetUp
    cuirasse = FactoryNavire(nom="cuirassé", taille=4).get_navire()
    fregate = FactoryNavire(nom="frégate", taille=3).get_navire()
    sous_marin = FactoryNavire(nom="sous-marin", taille=3).get_navire()
    torpilleur = FactoryNavire(nom="torpilleur", taille=2).get_navire()
    porte_avions = FactoryNavire(nom="porte-avions", taille=5).get_navire()

    navires = {cuirasse, fregate, sous_marin, torpilleur, porte_avions}
    navires_test = {cuirasse, sous_marin, torpilleur}

    grille = Grille(10,10)
    grille.create()

    grille_test = Grille(5,5)
    grille_test.create()

    plateau_cible = grille_test.get_plateau()

    plateau_cible[0][0].set_statut("hit")
    plateau_cible[2][2].set_statut("fail")

    #afficher_plateau(plateau=plateau_cible)
    #print("")

    all_config = generer_configurations(plateau_cible=plateau_cible, navires=navires_test)

    nb_total_config = len(all_config)

    print(f"""
          Le nombre total de configuration possible est : {nb_total_config}
          """)


    matrice_proba = genere_matrice_proba(all_config=all_config)

    sns.heatmap(matrice_proba)

    ligne, colonne = get_ligne_colonne_matrice_proba(matrice_proba=matrice_proba)

    print(ligne, colonne)

    
    plt.show()
