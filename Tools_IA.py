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
    # conversion du plateau pour utiliser les symboles
    plateau_cible_symbole = get_plateau_symbole(plateau_cible)


    def generer(index):
        if index == len(navires):
            if configuration_valide(plateau_cible, navires, nb_hits):
                afficher_plateau(plateau_cible)
                print("")
                print("")
                configurations.append([ligne[:] for ligne in plateau_cible])
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



# imports additionnels
from Navire import FactoryNavire
from Grille import Grille
from Strategie import FactoryStrategie
import pandas as pd

if __name__=="__main__" :
    ### SetUp
    cuirasse = FactoryNavire(nom="cuirassé", taille=4).get_navire()
    fregate = FactoryNavire(nom="frégate", taille=3).get_navire()
    sous_marin = FactoryNavire(nom="sous-marin", taille=3).get_navire()
    torpilleur = FactoryNavire(nom="torpilleur", taille=2).get_navire()
    porte_avions = FactoryNavire(nom="porte-avions", taille=5).get_navire()

    navires = {cuirasse, fregate, sous_marin, torpilleur, porte_avions}

    grille = Grille(10,10)
    grille.create()
    plateau_cible = grille.get_plateau()

    plateau_cible[0][0].set_statut("hit")
    plateau_cible[2][2].set_statut("fail")

    #afficher_plateau(plateau=plateau_cible)

    all_config = generer_configurations(plateau_cible=plateau_cible, navires=navires)
