# Permet de recuperer le symbole de chacune des cases de jeu du plateau
def get_plateau_symbole(plateau) :
    plateau_symbole = list(map(lambda ligne_case_jeu : list(map(lambda case_jeu : case_jeu.get_symbole(), ligne_case_jeu)), plateau))

    return plateau_symbole


# Affichage d'un plateau 
def afficher_plateau(plateau):
    result = ""

    plateau_symbole = get_plateau_symbole(plateau)

    for ligne in plateau_symbole:
        result += " ".join(ligne) + "\n"
        print(" ".join(ligne))

    return result


# Affichage d'un couple de plateau
def afficher_couple_plateau(plateau1, plateau2):
    if len(plateau1) != len(plateau2) or len(plateau1[0]) != len(plateau2[0]):
        raise ValueError("Les deux grilles sont de tailles différentes !")
    
    result = ""
    result += "     Vos navires :                      Champ de tir :\n"
    
    plateau1_symbole = get_plateau_symbole(plateau1)
    plateau2_symbole = get_plateau_symbole(plateau2)
    
    for index_ligne in range(len(plateau1_symbole)):
        result += "     " + " ".join(plateau1_symbole[index_ligne]) + "                " + " ".join(
            plateau2_symbole[index_ligne]) + "\n"
    print(result)
    return (result)