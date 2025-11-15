import pytest

from business_object.board import Board
from business_object.carte import Carte
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main
from business_object.manche import Manche

# ------------------------ Fixtures ------------------------


@pytest.fixture
def joueurs():
    return [
        Joueur(id_joueur=i + 1, pseudo=f"J{i + 1}", credit=1000, pays="France") for i in range(2)
    ]


@pytest.fixture
def info_manche(joueurs):
    return InfoManche(joueurs)


@pytest.fixture
def manche(info_manche):
    m = Manche(info_manche, grosse_blind=10)

    # Assigner des mains valides aux joueurs
    mains = [
        Main(cartes=[Carte("As", "Coeur"), Carte("Roi", "Coeur")]),
        Main(cartes=[Carte("Dame", "Trêfle"), Carte("Valet", "Trêfle")]),
        # Ajouter autant de Main que de joueurs
    ]
    m.info.assignation_mains(mains)

    # Initialiser un board avec des cartes
    m._board = Board(
        cartes=[
            Carte("10", "Pique"),
            Carte("9", "Coeur"),
            Carte("8", "Carreau"),
            Carte("7", "Trêfle"),
            Carte("6", "Coeur"),
        ]
    )

    # Forcer le tour à la river
    m.tour = 3

    return m


# ------------------------ Helpers ------------------------


def remplir_board(manche):
    """Remplit le board avec 5 cartes et force le tour à 3"""
    cartes = [
        Carte("10", "Pique"),
        Carte("Valet", "Pique"),
        Carte("Dame", "Pique"),
        Carte("Roi", "Pique"),
        Carte("As", "Pique"),
    ]
    manche.board._cartes = cartes
    manche._tour = 3  # indispensable pour passer le test classement


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
    j0, j1 = joueurs
    assert manche.est_tour(j0) is True
    assert manche.est_tour(j1) is False


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
    manche.info.statuts[:] = [0, 2]
    assert manche.joueurs_en_lice == [0, 2]


# ------------------------ Tests classement ------------------------


def test_classement_erreur_board_incomplete(manche):
    manche._tour = 2  # board non complet
    with pytest.raises(RuntimeError):
        manche.classement()


def test_classement_simple(manche):
    remplir_board(manche)
    # Chaque joueur a une main différente
    manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Trêfle")]
    manche.info.mains[1]._cartes = [Carte("4", "Trêfle"), Carte("5", "Trêfle")]
    manche.info.mains[2]._cartes = [Carte("6", "Trêfle"), Carte("7", "Trêfle")]

    classement = manche.classement()
    assert len(classement) == 3
    assert sorted(classement) == [1, 2, 3]  # aucun ex-aequo


def test_classement_ex_aequo(manche):
    remplir_board(manche)
    # Deux joueurs identiques -> ex-aequo
    manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Trêfle")]
    manche.info.mains[1]._cartes = [Carte("2", "Trêfle"), Carte("3", "Trêfle")]
    manche.info.mains[2]._cartes = [Carte("6", "Trêfle"), Carte("7", "Trêfle")]

    classement = manche.classement()
    assert classement[0] == classement[1]
    assert classement[2] > classement[0]
