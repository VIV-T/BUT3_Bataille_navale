'''
La classe de CreationStrategie() est appelée par la classe ChoixStrategie() et appelle la classe FactoryStrategie().
Elle permet de créer une nouvelle stratégie valide en demandant les inputs nécessaires à l'utilisateur.
ATTENTION : beaucoup d'inputs !

Input :
    - navires : Il s'agit d'un set d'instance de la classe Navire.
            Ces instances contiennent toute les informations nécessaire pour la classe Strategie.

    - grille : Instance de la classe Grille.


Méthode de classe :
    - input_donnees_placement_navire : Methode permettant de définir les inputs nécessaires au placement d'un navire :
                                                - coordonnée sur les lignes
                                                - coordonnée sur les colonnes
                                                - orientation


    - creer_strategie : Permet de créer une stratégie.
                        => demande de toutes les informations nécessaires à l'utilisateur à l'aide d'inputs.
                        => pour chaque navire : appel de la methode 'input_donnees_placement_navire'
'''
from Grille import Grille
import pandas as pd
from Strategie import FactoryStrategie, Strategie


class CreationStrategie():
    # Getters
    def get_navires(self):
        return self._navires

    def get_grille(self):
        return self._grille

    def get_instance_strategie(self):
        return self.instance_strategie

    # Setters
    def set_navires(self, navires=None):
        if navires is None:
            navires = self.navires
        self._navires = navires

    def set_grille(self, grille=None):
        if grille is None:
            grille = self.grille
        self._grille = grille
        self._grille.create()

        self.premiere_ligne_grille = 1
        self.derniere_ligne_grille = self.grille.get_nb_lignes()
        self.premiere_colonne_grille = 1
        self.derniere_colonne_grille = self.grille.get_nb_colonnes()

    def __init__(self, navires: set, grille : Grille):
        # Variables privées
        self._navires: set
        self._grille: Grille

        # Variables publiques
        self.navires = navires
        self.grille = grille
        self.instance_strategie : Strategie|None = None

        self.premiere_ligne_grille: int
        self.derniere_ligne_grille: int
        self.premiere_colonne_grille: int
        self.derniere_colonne_grille: int

        self.inputs_strategie = pd.DataFrame({"nom": [], "taille": [], "coord_x": [], "coord_y": [], "orientation": []})

    # Fonction principale : elle permet la création de l'objet strategie : {nom : [taille, coord_x, coord_y, sens]}
    # Cet objet strategie reuni les placement de tous les navires dans la grille.
    # Il faut bien sur que la strategie soit valide après sa création sinon cela n'aurait aucun sens.
    # Par 'valide' il faut entendre que la stratégie respecte les règles du jeu.
    def creer_strategie(self):
        print('Pour chacun des navires, vous devez choisir ses coordonnées en ligne, en colonne, '
              'et son orientation (Nord, Est, Sud, Ouest).')
        print("")

        coord_ligne: int
        coord_colonne: int
        sens: str
        taille: int

        # il faut boucler sur tous les navires du référentiel
        # on ne peut pas choisir de ne pas placer un navire, c'est impossible !
        for navire in self.navires:
            new_data = self.input_donnees_placement_navire(navire)
            self.inputs_strategie.loc[len(self.inputs_strategie.index)] = new_data
            self.instance_strategie = FactoryStrategie(self.inputs_strategie, self.navires, grille=self.get_grille(),
                                                       complete=False).get_strategie()

            while not self.instance_strategie.verifier_placabilite():
                print('Stratégie invalide !!!')
                print('Vous devez re-saisir les caractéristiques du dernier navire.')
                print(
                    "L'orientation choisie peut être mauvaise, il est aussi possible que votre choix de placement soit incorrect (chevauchement de 2 navires)\n")
                self.inputs_strategie[f'{navire}'] = self.input_donnees_placement_navire(navire)
                # initialisation de l'instance de la classe Strategie
                self.instance_strategie = FactoryStrategie(self.inputs_strategie, self.navires,
                                                           grille=self.get_grille(), complete=False).strategie

            print("Voici votre strategie actuelle :\n")
            self.instance_strategie.affichage_strategie()

        return self.instance_strategie

    # Il s'agit principalement d'une fonction d'input avec beaucoup de condition sur le placement des navires.
    # Le but est de poser un cadre au placement des navires afin que les navires puisse être représentés dans la grille ensuite.
    def input_donnees_placement_navire(self, navire):
        nom = navire.get_nom()
        taille = navire.get_taille()

        print("Les caractéristiques de la grille de jeu sont :")
        print(f"Nombre de lignes : {self.derniere_ligne_grille}")
        print(f"Nombre de colonnes : {self.derniere_colonne_grille}\n")
        print(f'Choisissez les caractéritiques du navire suivant : {nom} (longueur : {taille}).')
        coord_valides = False

        while not coord_valides:
            coord_ligne = input('Numéro de ligne : ')
            coord_colonne = input('Numéro de colonne : ')

            try:
                coord_ligne = int(coord_ligne)
                coord_colonne = int(coord_colonne)
                if coord_ligne <= self.derniere_ligne_grille and coord_ligne >= self.premiere_ligne_grille:
                    if coord_colonne <= self.derniere_colonne_grille and coord_colonne >= self.premiere_colonne_grille:
                        coord_valides = True
                    else:
                        print(
                            f"Les coordonnées doivent être des nombres compris entre {self.premiere_colonne_grille} et {self.derniere_colonne_grille}")
                else:
                    print(
                        f"Les coordonnées doivent être des nombres compris entre {self.premiere_ligne_grille} et {self.derniere_ligne_grille}")

            except:
                print("Veuillez rentrer un nombre !")

        # Gestion des cas en bord de grille + les coins
        sens_valide = False

        while not sens_valide:

            # La condition de validité du sens du navire dépend de la taille de ce dernier,
            # Exemple : un navire de taille 4 peut se positionner sur la 3ème ligne,
            # mais il ne peut dans ce cas pas s'orienter vers le nord !
            if coord_ligne < taille:
                # Coin supérieur gauche
                if coord_colonne < taille:
                    sens = input("Choisissez l'orientation du navire : (E/S)\n")
                    sens = sens.upper()
                    if sens == 'E' or sens == 'S':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

                # Coin supérieur droit
                elif coord_colonne + taille > self.derniere_colonne_grille + 1:
                    sens = input("Choisissez l'orientation du navire : (S/O)\n")
                    sens = sens.upper()
                    if sens == 'S' or sens == 'O':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

                # Première ligne sans les coins
                else:
                    sens = input("Choisissez l'orientation du navire : (E/S/O)\n")
                    sens = sens.upper()
                    if sens == 'S' or sens == 'O' or sens == 'E':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

            # Dernière ligne
            elif coord_ligne + taille > self.derniere_ligne_grille + 1:
                # Coin inférieur gauche
                if coord_colonne < taille:
                    sens = input("Choisissez l'orientation du navire : (E/N)\n")
                    sens = sens.upper()
                    if sens == 'E' or sens == 'N':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

                # Coin inférieur droit
                elif coord_colonne + taille > self.derniere_colonne_grille + 1:
                    sens = input("Choisissez l'orientation du navire : (N/O)\n")
                    sens = sens.upper()
                    if sens == 'N' or sens == 'O':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

                # Dernière ligne sans les coins
                else:
                    sens = input("Choisissez l'orientation du navire : (E/N/O)\n")
                    sens = sens.upper()
                    if sens == 'N' or sens == 'O' or sens == 'E':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')


            # Cas des lignes générales
            else:
                # Première colonne sans les coins
                if coord_colonne < taille:
                    sens = input("Choisissez l'orientation du navire : (E/N/S)\n")
                    sens = sens.upper()
                    if sens == 'E' or sens == 'S' or sens == 'N':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

                # Dernière colonne sans les coins
                elif coord_colonne + taille > self.derniere_colonne_grille + 1:
                    sens = input("Choisissez l'orientation du navire : (N/O/S)\n")
                    sens = sens.upper()
                    if sens == 'S' or sens == 'O' or sens == 'N':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

                # Cas général
                else:
                    sens = input("Choisissez l'orientation du navire : (N/E/S/O)\n")
                    sens = sens.upper()
                    if sens == 'E' or sens == 'S' or sens == 'O' or sens == 'N':
                        sens_valide = True
                    else:
                        print('Orientation du navire non valide.')

        print("")
        return [nom, taille, coord_ligne, coord_colonne, sens]


class FactoryCreationStrategie():
    def get_instance_strategie(self):
        return self.strategie

    def __init__(self, navires: set, grille):
        self.creation_strategie = CreationStrategie(navires, grille)
        self.creation_strategie.set_navires()
        self.creation_strategie.set_grille()
        self.creation_strategie.creer_strategie()
        self.strategie = self.creation_strategie.get_instance_strategie()
