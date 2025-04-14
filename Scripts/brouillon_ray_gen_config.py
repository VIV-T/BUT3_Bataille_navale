"""
import ray
from copy import deepcopy

# Initialiser Ray
ray.init()

@ray.remote
def generer_configurations_parallele(plateau_cible, navires, navires_coules, nb_hits, index):
    configurations = []

    # Fonction recursive de generation.
    def generer(index):
        if index == len(navires):
            if configuration_valide(plateau_cible, navires, nb_hits):
                # conversion du plateau pour utiliser les symboles
                plateau_cible_symbole = get_plateau_symbole(plateau_cible)
                configurations.append([ligne[:] for ligne in plateau_cible_symbole])
            return

        # Placement du navire dans la configuration
        navire = navires[index]
        taille = navire.get_taille()
        for ligne in range(len(plateau_cible)):
            for colonne in range(len(plateau_cible[0])):
                for horizontal in [True, False]:
                    if est_valide(plateau_cible, ligne, colonne, taille, horizontal):
                        placer_navire(plateau_cible, ligne, colonne, horizontal, navire)
                        generer(index + 1)
                        retirer_navire(plateau_cible, ligne, colonne, taille, horizontal)

    generer(index)
    return configurations

def generer_configurations_parallelized(plateau_cible, navires: set):
    # Vérification des navires coulés à partir du plateau_cible
    navires_coules = set()
    nb_hits = 0  # Utile pour les critères de validité des configs

    for row in plateau_cible:
        for tile in row:
            if tile.get_statut() == "cast":
                navires_coules = navires_coules.union({tile.get_navire()})
            elif tile.get_statut() == "hit":
                nb_hits += 1

    # Si un ou plusieurs navires ont été coulé, on les supprime du dict
    navires_bis = deepcopy(navires)
    if len(navires_coules) > 0:
        for navire_coule in navires_coules:
            for navire in navires_bis:
                if navire == navire_coule:
                    navires.remove(navire)

    # transformation du set en list pour pouvoir faire de la recursivité
    navires = list(navires)

    # Lancer les tâches parallèles
    futures = [generer_configurations_parallele.remote(deepcopy(plateau_cible), navires, navires_coules, nb_hits, 0) for _ in range(ray.available_resources().get('CPU', 1))]

    # Collecter les résultats
    all_configurations = ray.get(futures)

    # Fusionner les résultats
    configurations = [config for sublist in all_configurations for config in sublist]

    return configurations
"""