"""
Classe ChoixStrategie()
Il s'agit de la classe qui permet l'interaction avec l'utilisateur pour son choix de strategie
(=placement de ses navires dans la grille de jeu).
ATTENTION : beaucoup d'inputs !

Fonctionnement :
    Guider l'utilisateur dans ses choix et actions jusqu'à qu'il se voit attribué un stratégie.
    Il peut choisir entre :

        - Créer une strategie :
            Appel de la classe CreationStrategie().
            Appel de la methode get() de cette même classe après la création.

        - Choisir une strategie existante :
            Afficher la liste des strategie présentent dans le referentiel.
            Proposer à l'utilisateur de choisir l'une des strategie affichée

    Il doit ensuite confirmer son choix.


Input :
    - pseudo_joueur : le pseudo du joueur, ex : 'mon_pseudo'

    - navires : Il s'agit d'un set d'instance de la classe Navire.
                    Ces instances contiennent toute les informations nécessaire pour la classe Strategie.

    - mode_jeu : Une instance de la classe ModeJeu qui contient les caractéristiques du mode de jeu.
                    Cela aura une influence sur les inputs demandées à l'utilisateur.

    - grille : Instance de la classe Grille. Elle permet l'affichage des strategies. Définie par défault à 10x10.



Méthode de classe :
    - lire_fichier_sauvegarde : permet de récupérer les données auvegardée dans le fichier csv : "sauvegardes_strategie.csv"
                                Les données sont sauvegardées dans la variable de classe 'self.referentiel', c'est un Dataframe pandas.

    - ecrire_fichier_sauvegarde : permet d'écrire dans le fichier : "sauvegardes_strategie.csv"
                                    Cette écriture se fait à partir d'un Dataframe pandas, la variable 'self.referentiel'


    - main() : méthode principale du programme qui agit comme une interface utilisateur.
                Dans cette méthode nous guidons l'utilisateur dans ses choix afin de lui proposer une expérience de jeu optimale.
                cf. 'Fonctionnement'

    - valider_input_utilisateur(): Prend en input une requette faite à l'utilisateur, ainsi que 2 choix possible pour l'utilisateur. (str)
                                    Cette méthode permet de vérifier si l'utilisateur à bien saisi un choix cohérent.
                                    Elle permet d'éviter des erreurs liées aux input.
"""
import os
import pandas as pd

from unidecode import unidecode
from Grille import Grille, afficher_grille
from Strategie import Strategie, FactoryStrategie
from CreationStrategie import FactoryCreationStrategie
from ModeJeu import ModeJeu


class ChoixStrategie():
    # Getters
    def get_referentiel(self):
        return self.referentiel

    def get_strategie(self):
        return self.strategie

    # Constructeur
    def __init__(self, pseudo_joueur: str, navires: set, mode_jeu: ModeJeu, grille=Grille(10, 10)):
        self.mode_jeu: ModeJeu = mode_jeu
        self.navires = navires
        self.referentiel: pd.DataFrame = pd.DataFrame({
            "mode_jeu": [],
            "index_strategie": [],
            "nom": [],
            "taille": [],
            "coord_x": [],
            "coord_y": [],
            "orientation": [],
        })

        self.instance_grille = grille
        self.pseudo_joueur = pseudo_joueur
        self.strategie: Strategie | None = None

    # Lecture du fichier et récupération des inputs_strategie enregistrées dans le référentiel.
    def lire_fichier_sauvegarde(self):
        self.referentiel = pd.read_csv('sauvegardes_strategies.csv', encoding="UTF-8")

    # On écrit le fichier de sauvegarde à partir des données du référentiel.
    def ecrire_fichier_sauvegarde(self):
        self.referentiel.to_csv('sauvegardes_strategies.csv', index=False, encoding="UTF-8")

    # Méthode principale qui appelle toutes les autres en fonction des choix du joueur.
    def main(self):

        os.system('cls')
        print(f"C'est à {self.pseudo_joueur} de choisir sa stratégie de bataille.\n")
        df_mode_jeu = self.referentiel[self.referentiel.mode_jeu == self.mode_jeu.get_nom()]

        if len(df_mode_jeu) > 0:
            choix_choisir_creer = f"{self.pseudo_joueur}, voulez-vous choisir une stratégie enregistrée ou en créer une nouvelle ?"
            choix_choisir = 'choisir'
            choix_creer = 'creer'
            # validation de l'input avec la méthode associée
            choix = self.valider_input_utilisateur(choix_choisir_creer, choix_choisir, choix_creer)
        else:
            print("Il n'existe aucune strategie enregistrée pour ce mode de jeu.\nVous devez créer votre strategie.")
            input("Tapez 'entrer' pour continuer.\n")
            os.system('cls')
            choix = 'creer'

        # Définition des variables associée aux choix OUI/NON.
        # Utile pour la méthode de validation d'input.
        choix_oui = 'o'
        choix_non = 'n'

        if choix == 'creer':
            # Appel de la classe CreationStrategie() -> lancement du code de création
            # Appel de la methode get_instance_strategie() qui retourne l'instance de la classe Strategie() créée.
            creation_strategie = FactoryCreationStrategie(self.navires, self.instance_grille)
            self.strategie = creation_strategie.get_instance_strategie()

            # Création de la chaine rentrée ensuite en paramètre de la fonction input()
            choix_action_enregistrement = "Voulez-vous enregistrer la stratégie créée ?"
            # validation de l'input avec la méthode associée
            choix_enregistrement = self.valider_input_utilisateur(choix_action_enregistrement, choix_oui, choix_non)

            if choix_enregistrement == 'o':
                # Ajout des inputs de la stratégie au référentiel.
                # il s'agit ici des informations permettant d'instancier la classe Strategie
                new_inputs_strategie = self.strategie.get_informations()
                try:
                    index_strategie = max(self.referentiel["index_strategie"]) + 1
                except:
                    index_strategie = 1

                for line in new_inputs_strategie.values:
                    new_data = [self.mode_jeu.get_nom(), index_strategie] + list(line)
                    self.referentiel.loc[len(self.referentiel.index)] = new_data

                print("La stratégie a bien été enregistrée.")
            else:
                print('Vous avez choisi de ne pas enregistrer la strategie.')

            # Affichage de la strategie du joueur + Fin du main
            print("")
            print(f"{self.pseudo_joueur}, votre stratégie a bien été définie.")
            print("")

            self.instance_grille.create()
            self.strategie.placement_navires(self.instance_grille.plateau, self.strategie.informations)
            afficher_grille(self.instance_grille.plateau)
            # permet au joueur d'apprécier l'affichage de sa strategie et l'input sert aussi de confirmation
            input("Tapez 'entrer' pour continuer\n")
            return True

        elif choix == 'choisir':

            strategie_correctement_choisie = False
            while not strategie_correctement_choisie:
                self.instance_grille.create()
                print('Voici la liste des stratégies enregistrée :')

                # correspondance avec le mode de jeu
                df_strategie_to_choose = self.referentiel[self.referentiel.mode_jeu == self.mode_jeu.get_nom()]
                # extraction de l'ensemble des index_strategie correspondant au premier critère de filtrage (mode_jeu)
                liste_index_strategie = set(df_strategie_to_choose.index_strategie)
                # Boucle pour l'affichage
                for i in liste_index_strategie:
                    print(f"Strategie n°{i} :")
                    # affichage des lignes & colonnes concernées
                    print(self.referentiel[self.referentiel.index_strategie == i].iloc[:, 2:])
                    print("------------------")
                print("")

                valider_choix_numero_strategie = False

                while not valider_choix_numero_strategie:
                    choix_numero_strategie = input(
                        "Quelle stratégie voulez-vous choisir ?  (Choisir une numéro de stratégie)\n")
                    print("")

                    try:
                        choix_numero_strategie = int(choix_numero_strategie)

                        # On associe la strategie choisie en input à la variable locale strategie_choisie.
                        inputs_strategie_choisie = self.referentiel[
                            self.referentiel.index_strategie == choix_numero_strategie]

                        strategie_choisie = FactoryStrategie(inputs_strategie_choisie, self.navires,
                                                             self.instance_grille).strategie
                        print(strategie_choisie.get_informations())

                        valider_choix_numero_strategie = True
                    except IndexError:
                        print(f"La stratégie n°{choix_numero_strategie} n'existe pas !")
                        print("Choisissez une stratégie existante.")
                    except:
                        print("Erreur de saisie !")
                        print('Choisissez le numéro de la stratégie parmis les stratégie existantes.')

                print(f"Vous avez choisi la stratégie n°{choix_numero_strategie} :\n")

                # On place la strategie dans la grille
                strategie_choisie.placement_navires(self.instance_grille.plateau, strategie_choisie.informations)
                # On l'affiche
                afficher_grille(self.instance_grille.plateau)

                # Confirmation du choix de la strategie
                choix_action_confirmation_strategie = "Confirmez votre choix ?"
                # validation de l'input
                confirmation_choix_strategie = self.valider_input_utilisateur(choix_action_confirmation_strategie,
                                                                              choix_oui, choix_non)

                # Condition de sortie de boucle -> OK
                if confirmation_choix_strategie == 'o':
                    print(f'Vous avez bien choisi la stratégie n°{choix_numero_strategie}')
                    self.strategie = strategie_choisie
                    strategie_correctement_choisie = True

            # Affichage de la strategie du joueur + Fin du main
            print("")
            print(f"{self.pseudo_joueur}, votre stratégie a bien été définie.")
            print("")

            self.instance_grille.create()
            self.strategie.placement_navires(self.instance_grille.plateau, self.strategie.informations)
            afficher_grille(self.instance_grille.plateau)
            # permet au joueur d'apprécier l'affichage de sa strategie et l'input sert aussi de confirmation
            input("\nTapez 'entrer' pour continuer\n")
            return True

    # Méthode permettant de protéger les inputs utilisateur et de gérer les cas d'erreur.
    def valider_input_utilisateur(self, requette: str, choix_1: str, choix_2: str):
        # condition de validité de l'input
        validite_choix_utilisateur = False

        # boucle de vérification / modification de la valeur précédente.
        while not validite_choix_utilisateur:
            choix_utilisateur = input(requette + '  (' + choix_1 + '/' + choix_2 + ')\n')

            try:
                # Suppression des accents potentiels
                choix_utilisateur = unidecode(choix_utilisateur)
                # Passage de la chaine en minuscule
                choix_utilisateur = choix_utilisateur.lower()
                choix_1 = choix_1.lower()
                choix_2 = choix_2.lower()

                assert choix_utilisateur == choix_1 or choix_utilisateur == choix_2
                validite_choix_utilisateur = True

            except AssertionError:
                print("Erreur de saisie !")
                print("Vous devez choisir l'une des propositions\n")
            except:
                print('Erreur !')
                print('Suivez les instructions pour pouvoir jouer correctement !\n')

        print("")
        return choix_utilisateur


class FactoryChoixStrategie():
    def get_strategie(self):
        return self.choix_strategie.get_strategie()

    def __init__(self, pseudo_joueur, navires, mode_jeu: ModeJeu, grille=Grille(10, 10), test: bool = False):
        self.choix_strategie = ChoixStrategie(pseudo_joueur, navires, mode_jeu, grille)
        self.choix_strategie.lire_fichier_sauvegarde()
        if not test:
            self.choix_strategie.main()
        self.choix_strategie.ecrire_fichier_sauvegarde()
