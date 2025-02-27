'''
Fichier principal du projet.

Contient la fonction lancer_partie() ou du code correspondant à ça.
Cette fonction réalise les appels nécéssaire au bon déroulement de la partie.
Elle permet de regrouper les phases d'initialisation et de jeu :
 - La phase d'initialisation concerne la gestion/ création des paraètres, stratégie, etc...
 - La phase de jeu lance la partie avec la classe BatailleNavale() avec les paramètres définis précédement.

La fin de partie est gérée dans la classe BatailleNavale().
'''
import os

import pandas as pd

from ChoixStrategie import FactoryChoixStrategie
from Strategie import FactoryStrategie
from BatailleNavale import BatailleNavale
from Grille import Grille
from Navire import Navire
from ChoixModeJeu import FactoryChoixModeJeu


# Fonction d'input.
# Prend en parametre le n° du joueur.
# Demande le nom du joueur.
# Appel de la classe ChoisirStrategie() pour le joueur concerné.
# La fonction renvoie une liste qui contient le nom du joueur saisi
# et sa strategie sous la forme d'une instance de la classe Strategie.
def choix_nom_et_strategie_joueur(numero_joueur, navires : Navire, grille : Grille, mode_jeu : str):
    # initialisation de variables locales
    pseudo_joueur = ''
    # Le booléen choix_valide_joueur permet de gérer les cas d'erreur sur les inputs et d'y répondre de manière efficace :
    # en redemandant à l'utilisateur de rentrer sa données en précisant pourquoi cela n'a pas marché la 1ère fois.
    choix_valide_joueur = False

    while not choix_valide_joueur :
        os.system('cls')
        pseudo_joueur = input(f"Joueur {numero_joueur}, quel est votre pseudo ? \n")

        try :
            pseudo_joueur = pseudo_joueur.replace(" ", "")
            assert len(pseudo_joueur) < 15
            if not pseudo_joueur.isalnum() :
                raise ValueError
            elif pseudo_joueur == '_Ordinateur':
                raise ZeroDivisionError
            choix_valide_joueur = True
        except AssertionError :
            print("\nLe nom du joueur est trop long !\n")
            input("Tapez 'entrer' pour continuer\n")
        except ValueError :
            print('\nLe nom doit être composé de lettres et/ou de chiffres.\n')
            input("Tapez 'entrer' pour continuer\n")
        except ZeroDivisionError :
            print("\nCe pseudo est privatisé, vous ne pouvez pas l'utiliser. Choisissez en un autre :\n")
            input("Tapez 'entrer' pour continuer\n")

    print("")
    strategie_joueur = FactoryChoixStrategie(pseudo_joueur, navires=navires, grille =grille, mode_jeu=mode_jeu).get_strategie()

    return [pseudo_joueur, strategie_joueur]



if __name__ == "__main__":
    os.system('cls')
    print('Bienvenue dans le jeu de Bataille Navale !')

    ### Choix mode de jeu (normal - 10*10, blitz - 5*5, personnalisé - dépend des choix du joueur)
    # /!\ Cela implique une modification des classes de création et d'enregistrement de stratégie (prise en compte du mode de jeu)
    choix_mode_jeu = FactoryChoixModeJeu()

    ### Initialisation des navires - a modifier en fonction des mode de jeux
    navires = choix_mode_jeu.get_navires()
    grille = choix_mode_jeu.get_grille()
    mode_jeu = choix_mode_jeu.get_mode_jeu()

    ### Choix de l'adversaire
    choix_adversaire=''

    # Le booléen choix_valide_joueur permet de gérer les cas d'erreur sur les inputs et d'y répondre de manière efficace :
    # en redemandant à l'utilisateur de rentrer sa données en précisant pourquoi cela n'a pas marché la 1ère fois.
    choix_adversaire_valide = False
    while not choix_adversaire_valide :
        # Choix de l'adversaire + rajouter une gestion d'erreur + texte de réponse adapté à la variable.
        choix_adversaire = input("Voulez-vous jouer contre un joueur ou contre l'ordinateur ? (joueur / ordinateur)\n")

        try :
            choix_adversaire = choix_adversaire.lower()
            choix_adversaire = choix_adversaire.replace(" ", "")
            assert choix_adversaire == 'ordinateur' or choix_adversaire == 'joueur'
            choix_adversaire_valide = True
        except AssertionError :
            print('Erreur !\nVeuillez saisir une valeur valide.\n')

    print("")
    choix_adversaire.lower()



    ### Choix des stratégie -> appel de la classe ChoixStrategie()
    if choix_adversaire == 'joueur' :
        # 1er joueur
        informations_j1 = choix_nom_et_strategie_joueur(1, navires=navires, grille=grille, mode_jeu=mode_jeu)
        nom_j1 = informations_j1[0]
        strategie_j1 = informations_j1[1]

        print("")

        # 2eme joueur
        informations_j2 = choix_nom_et_strategie_joueur(2, navires=navires, grille=grille, mode_jeu=mode_jeu)
        nom_j2 = informations_j2[0]
        strategie_j2 = informations_j2[1]

    elif choix_adversaire == 'ordinateur':
        # 1er joueur
        information_j1 = choix_nom_et_strategie_joueur(1, navires=navires, grille=grille, mode_jeu=mode_jeu)
        nom_j1 = information_j1[0]
        strategie_j1 = information_j1[1]

        # Rajouter du code pour initialiser la strategie de l'ordinateur (définie par défault).
        # La privatisation (théorique) du nom permet dans la classe BatailleNavale() de passer le jeu de l'ordinateur en auto.
        nom_j2 = '_Ordinateur'
        # modifier ici, popur que l'ordinateur est une strategie aléatoire parmis les stratégies enregistrées.
        data_inputs_strategie = {"nom": ["torpilleur", "sous-marin", "frégate", "cuirassé", "porte-avions"],
                                 "taille": [2, 3, 3, 4, 5], "coord_x": [1, 5, 3, 5, 9],
                                 "coord_y": [1, 1, 5, 6, 9], "orientation": ["S", "S", "E", "O", "N"]}
        inputs_strategie = pd.DataFrame(data_inputs_strategie)
        strategie_j2 = FactoryStrategie(inputs_strategie,
                                 navires,
                                 Grille(10, 10)).get_strategie()

    BatailleNavale(navires, strategie_j1, strategie_j2, Grille(10,10),nom_j1, nom_j2)
