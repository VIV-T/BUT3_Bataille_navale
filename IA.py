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
from Tools_IA import generer_configurations, genere_matrice_proba, get_coord_from_matrice_proba, trouver_coordonnees_ciblees, trouver_coord_case_adjacente
from Tools import afficher_plateau

class IA():
    def get_level(self) :
        return self._level

    def __init__(self, level : str):
        self._level = level 


    def play_IA(self, plateau_cible, navires :set) :
        match self._level :
            case "débutant" :
                ligne, colonne = self.play_debutant(plateau_cible=plateau_cible)
            case "intermédiaire" :
                ligne, colonne = self.play_intermediaire(plateau_cible=plateau_cible, navires=navires)
            case "avancé" :
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
     

    def play_avance(self, plateau_cible, navires :set):
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
