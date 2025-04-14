"""
Classe servant a definir la facon dont l'ordinateur joue - en fonction de son niveau.

On instancie la classe IA en precisant son niveau : 
 - debutant : des tir randoms
 - moyen : adoption d'une strategie de tir croisés (dépend de la taille du plus petit navire)
 - avancé : calcul de densité de probabilité + tir croisés
 - pro : mettre en place un réseau de neuronnes ?

"""
import random
import seaborn as sns
import matplotlib.pyplot as plt
import os
from Tools_IA import generer_configurations, genere_matrice_proba, get_coord_from_matrice_proba, trouver_coord_case_adjacente, check_nb_targeted_tile, cibler_coord_cross_random
from Tools import afficher_plateau

class IA():
    def get_level(self) :
        return self._level

    def __init__(self, level : str):
        self._level = level 


    def play_IA(self, plateau_cible, navires :set) :
        match self._level :
            case "debutant" :
                ligne, colonne = self.play_debutant(plateau_cible=plateau_cible)
            case "intermediaire" :
                ligne, colonne = self.play_intermediaire(plateau_cible=plateau_cible, navires=navires)
            case "avance" :
                ligne, colonne = self.play_avance(plateau_cible=plateau_cible, navires=navires)
            case "pro" :
                pass
            case _ :
                raise ValueError("Le niveau de l'IA n'est pas correctement défini.")

        # Ajout de 1 pour passer des index (liste python) au coordonnées du plateau.
        return ligne+1, colonne+1

    # tir sur des coordonnées aléatoires
    def play_debutant(self, plateau_cible) :
        ligne = random.randint(0, len(plateau_cible[0]))
        colonne = random.randint(0, len(plateau_cible[1]))

        return ligne, colonne
    
    # tir sur des coordonnées aléatoires selon le schema en croix - depend de la taille du plus petit navire
    # strategie : tir en croix + chasse quand "hit"
    def play_intermediaire(self, plateau_cible, navires) :
        ## Recherche de navires touchés (case adjacentes)
        ligne, colonne = trouver_coord_case_adjacente(plateau_cible=plateau_cible)
        # Si une case adjacente non ciblée à été trouvée, on renvoie ses coordonnées.
        if ligne != -1 :
            return ligne, colonne



        nb_targeted_tile = check_nb_targeted_tile(plateau_cible=plateau_cible)
        if nb_targeted_tile < 7 :
            coord_valides = False 
            while not coord_valides : 
                ligne, colonne = cibler_coord_cross_random(plateau_cible=plateau_cible, navires=navires)
                if ligne > 3 and ligne < 8 and colonne > 3 and colonne < 8 :
                            coord_valides = True
        else : 
            ligne, colonne = cibler_coord_cross_random(plateau_cible=plateau_cible, navires=navires)
            
        return ligne, colonne
     

    def play_avance(self, plateau_cible, navires :set):

        nb_targeted_tile = check_nb_targeted_tile(plateau_cible=plateau_cible)
        ligne, colonne = self.play_intermediaire(plateau_cible, navires)



        if nb_targeted_tile > 30 : 
            all_config = generer_configurations(plateau_cible=plateau_cible, navires=navires)

            matrice_proba = genere_matrice_proba(all_config=all_config)

            # enregistrement de la matrice de densité
            sns.heatmap(matrice_proba)
            try : 
                os.remove('proba_densite.png')
            except :
                pass
            plt.savefig('proba_densite.png')
            plt.close()
            

            ligne, colonne = get_coord_from_matrice_proba(matrice_proba)

        return ligne, colonne
