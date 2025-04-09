"""
Classe servant a definir la facon dont l'ordinateur joue - en fonction de son niveau.

On instancie la classe IA en precisant son niveau : 
 - debutant : des tir randoms
 - moyen : adoption d'une strategie de tir croisés (dépend de la taille du plus petit navire)
 - avancé : calcul de densité de probabilité + tir croisés
 - pro : mettre en place un réseau de neuronnes ?

"""
import random


class IA():
    def __init__(self, level : str):
        self._level = level 


    def play_IA(self, plateau_cible) :
        match self.level :
            case "débutant" :
                ligne, colonne = self.play_debutant(plateau_cible=plateau_cible)
            case "intermédiaire" :
                pass
            case "avancé" :
                pass
            case "pro" :
                pass


    # tir sur des coordonnées aléatoires
    def play_debutant(self, plateau_cible) :
        ligne = random.randint(0, len(plateau_cible[0]))
        colonne = random.randint(0, len(plateau_cible[1]))

        return ligne, colonne
    

    def play_avance(self, plateau_cible):
        pass