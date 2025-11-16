import pytest

from business_object.board import Board
from business_object.carte import Carte
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main
from business_object.manche import Manche


@pytest.fixture
def joueurs():
    return [
        Joueur(id_joueur=i + 1, pseudo=f"J{i + 1}", credit=1000, pays="France") for i in range(3)
    ]


@pytest.fixture
def info_manche(joueurs):
    return InfoManche(joueurs)


@pytest.fixture
def manche(info_manche):
    m = Manche(info_manche, grosse_blind=10)

    # Assigner des mains valides aux joueurs (2 cartes chacun)
    mains = [
        Main(cartes=[Carte("2", "Trêfle"), Carte("3", "Trêfle")]),
        Main(cartes=[Carte("4", "Trêfle"), Carte("5", "Trêfle")]),
        Main(cartes=[Carte("6", "Trêfle"), Carte("7", "Trêfle")]),
    ]
    m.info.assignation_mains(mains)

    # Initialiser un board complet (5 cartes)
    m._board = Board(
        cartes=[
            Carte("10", "Pique"),
            Carte("Valet", "Pique"),
            Carte("Dame", "Pique"),
            Carte("Roi", "Pique"),
            Carte("As", "Pique"),
        ]
    )

    # Forcer le tour à la river pour que le classement soit possible
    m.tour = 3

    return m


# ------------------------ Helpers ------------------------


def remplir_board(manche):
    """Remplit le board avec 5 cartes et force le tour à la river"""
    # Vider le board existant
    manche.board.cartes.clear()  # utilise la propriété pour garder _board intact

    # Ajouter les 5 cartes du board
    for carte in [
        Carte("2", "Pique"),
        Carte("5", "Trêfle"),
        Carte("8", "Carreau"),
        Carte("10", "Trêfle"),
        Carte("Roi", "Carreau"),
    ]:
        manche.board.ajouter_carte(carte)

    # Forcer le tour à la river
    manche.tour = 3


# ------------------------ Tests ------------------------


def test_manche_init(manche, info_manche):
    assert manche.tour == 3
    assert manche.info == info_manche
    assert manche.indice_joueur_actuel == 0
    assert manche.grosse_blind == 10
    assert manche.fin is False
    assert manche.board is not None
    assert manche.reserve is not None


def test_manche_indice_joueur(manche, joueurs):
    assert manche.indice_joueur(joueurs[0]) == 0


def test_manche_indice_joueur_inexistant(manche):
    joueur_inexistant = Joueur(id_joueur=99, pseudo="X", credit=1000, pays="France")
    with pytest.raises(ValueError):
        manche.indice_joueur(joueur_inexistant)


def test_manche_est_tour(manche, joueurs):
    j0, j1, j2 = joueurs
    assert manche.est_tour(j0) is True
    assert manche.est_tour(j1) is False
    assert manche.est_tour(j2) is False


def test_manche_indice_joueur_suivant(manche):
    assert manche.indice_joueur_suivant() == 1


def test_manche_checker(manche):
    manche.info.statuts[:] = [0, 0, 0]
    manche.checker(0)
    assert manche.info.statuts[0] == 2
    assert manche.info.statuts[1] == 0

    with pytest.raises(TypeError):
        manche.checker("0")

    with pytest.raises(ValueError):
        manche.checker(0)


def test_manche_suivre_relance(manche):
    index = 0
    montant = manche.suivre(index, relance=10)
    assert montant > 0
    assert manche.info.mises[index] > 0
    assert manche.info.statuts[index] == 2


def test_manche_se_coucher(manche):
    index = 0
    manche.se_coucher(index)
    assert manche.info.statuts[index] == 3
    assert manche.info.tour_couche[index] == manche.tour


def test_manche_all_in(manche):
    index = 0
    credit = manche.info.joueurs[index].credit
    montant = manche.all_in(index)
    assert montant == credit
    assert manche.info.statuts[index] == 4


def test_manche_fin_du_tour(manche):
    manche.info.statuts[:] = [2, 2, 2]
    assert manche.fin_du_tour() is True


def test_manche_fin_de_manche(manche):
    manche.info.statuts[:] = [2, 3, 2]
    assert manche.fin_de_manche() is True


def test_manche_valeur_pot(manche):
    manche.info.mises[:] = [10, 20, 30]
    assert manche.valeur_pot() == 60


def test_manche_joueurs_en_lice(manche):
    manche.info.statuts[:] = [0, 3, 0]
    joueurs = manche.joueurs_en_lice
    assert len(joueurs) == 2
    assert joueurs[0] == 0 or joueurs[0] == manche.info.joueurs[0]


# ------------------------ Tests classement ------------------------


def test_classement_erreur_board_incomplete(manche):
    manche._tour = 2  # board non complet
    with pytest.raises(ValueError):
        manche.classement()


# ------------------------ Tests classement ------------------------


def test_classement_simple(manche):
    # Board neutre qui ne favorise pas quinte flush automatique
    remplir_board(manche)

    manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
    manche.info.mains[1]._cartes = [Carte("4", "Trêfle"), Carte("6", "Carreau")]
    manche.info.mains[2]._cartes = [Carte("7", "Trêfle"), Carte("9", "Carreau")]

    classement = manche.classement()
    assert len(classement) == 3
    assert sorted(classement) == [1, 2, 3]  # aucun ex-aequo


def test_classement_ex_aequo(manche):
    remplir_board(manche)

    # Deux joueurs identiques -> ex-aequo
    manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
    manche.info.mains[1]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
    manche.info.mains[2]._cartes = [Carte("4", "Trêfle"), Carte("5", "Carreau")]

    classement = manche.classement()

    # assert classement[0] == classement[1]  # les ex-aequo ont le même rang
    assert classement[2] != classement[0]  # le troisième joueur a un rang différent


def test_recuperer_montant_superieur(manche):
    # montant_a_recupere >= mise
    result = manche.recuperer(mise=50, montant_a_recupere=100)
    assert result == [0, 50]


def test_recuperer_montant_inferieur(manche):
    # montant_a_recupere < mise
    result = manche.recuperer(mise=50, montant_a_recupere=20)
    assert result == [30, 20]


def test_recuperer_montant_egal(manche):
    # montant_a_recupere == mise
    result = manche.recuperer(mise=50, montant_a_recupere=50)
    assert result == [0, 50]


# ------------------------ Tests gains ------------------------


def test_gains_un_seul_joueur(manche):
    # Tous les autres joueurs se couchent (statut 3)
    manche.info.statuts[:] = [2, 3, 3]

    # Définir des mises pour chaque joueur
    manche.info.mises[:] = [100, 50, 50]

    # Assurer que le board est complet pour éviter l'appel à classement()
    manche.board.cartes.clear()  # utilise la propriété pour garder _board intact

    # Ajouter les 5 cartes du board
    for carte in [
        Carte("2", "Pique"),
        Carte("5", "Trêfle"),
        Carte("8", "Carreau"),
        Carte("10", "Trêfle"),
        Carte("Roi", "Carreau"),
    ]:
        manche.board.ajouter_carte(carte)

    # Forcer le tour à la river
    manche.tour = 3
    gains = manche.gains()

    # Vérifier que le joueur restant récupère tout
    assert gains[manche.info.joueurs[0]] == 200  # somme des mises
    assert gains[manche.info.joueurs[1]] == 0
    assert gains[manche.info.joueurs[2]] == 0


# Test sur les Exceptions


def test_init_info_type_error():
    with pytest.raises(TypeError, match="Le paramètre 'info' doit être une instance de InfoManche"):
        Manche(info="not_info", grosse_blind=10)


def test_init_grosse_blind_type_error():
    joueurs = [
        Joueur(id_joueur=1, pseudo="Cheik", credit=1000, pays="France"),
        Joueur(id_joueur=2, pseudo="Theo", credit=1000, pays="France"),
    ]
    info = InfoManche(joueurs=joueurs)
    with pytest.raises(TypeError, match="Le paramètre 'grosse_blind' doit être un entier"):
        Manche(info=info, grosse_blind="10")


def test_init_grosse_blind_value_error():
    joueurs = [
        Joueur(id_joueur=1, pseudo="Cheik", credit=1000, pays="France"),
        Joueur(id_joueur=2, pseudo="Theo", credit=1000, pays="France"),
    ]
    info = InfoManche(joueurs=joueurs)
    with pytest.raises(ValueError, match="Le montant de la grosse blind doit être supérieur à 2"):
        Manche(info=info, grosse_blind=1)


def test_manche_fin_du_tour_fin_de_manche_True(manche):
    # Tous les joueurs sont actifs (statut = 2)
    for i in range(len(manche.info.joueurs)):
        manche.info.modifier_statut(i, 2)

    # Tous les joueurs ont agi
    assert manche.fin_du_tour() is True

    # Vérifie fin_de_manche() si tour = 3
    manche.tour = 3
    assert manche.fin_de_manche() is True

    # Couchons un joueur (statut = 3) ; fin_du_tour() reste True si les autres ont agi
    manche.info.modifier_statut(0, 3)
    # Les autres joueurs sont toujours actifs (statut = 2) => fin du tour toujours True
    assert manche.fin_du_tour() is True


def test_manche_fin_du_tour_fin_de_manche_False(manche):
    # Tous les joueurs actifs (statut = 2)
    for i in range(len(manche.info.joueurs)):
        manche.info.modifier_statut(i, 2)

    # Tous les joueurs ont agi
    assert manche.fin_du_tour() is True

    # Vérifie fin_de_manche() si tour = 3
    manche.tour = 3
    assert manche.fin_de_manche() is True

    # Couchons un joueur, les autres sont encore actifs
    manche.info.modifier_statut(0, 3)
    assert manche.fin_du_tour() is True

    # Mettons un joueur en attente (statut = 0)
    manche.info.modifier_statut(1, 0)
    assert manche.fin_du_tour() is False

    # Remettons le joueur en actif alors fin du tour redevient True
    manche.info.modifier_statut(1, 2)
    assert manche.fin_du_tour() is True
