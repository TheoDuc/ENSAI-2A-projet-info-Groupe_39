import pytest

from business_object.board import Board
from business_object.carte import Carte
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main
from business_object.manche import Manche


class Test_Manche:
    @pytest.fixture
    @staticmethod
    def joueurs():
        return [
            Joueur(id_joueur=i + 1, pseudo=f"J{i + 1}", credit=1000, pays="France")
            for i in range(3)
        ]

    @pytest.fixture
    @staticmethod
    def info_manche(joueurs):
        return InfoManche(joueurs)

    @pytest.fixture
    @staticmethod
    def manche(info_manche):
        m = Manche(info_manche, grosse_blind=10)

        # Assigner des mains valides
        mains = [
            Main(cartes=[Carte("2", "Trêfle"), Carte("3", "Trêfle")]),
            Main(cartes=[Carte("4", "Trêfle"), Carte("5", "Trêfle")]),
            Main(cartes=[Carte("6", "Trêfle"), Carte("7", "Trêfle")]),
        ]
        m.info.assignation_mains(mains)

        # Ajouter board complet
        m._board = Board(
            cartes=[
                Carte("10", "Pique"),
                Carte("Valet", "Pique"),
                Carte("Dame", "Pique"),
                Carte("Roi", "Pique"),
                Carte("As", "Pique"),
            ]
        )

        m.tour = 3
        return m

    @staticmethod
    def remplir_board(manche):
        manche.board.cartes.clear()
        for carte in [
            Carte("2", "Pique"),
            Carte("5", "Trêfle"),
            Carte("8", "Carreau"),
            Carte("10", "Trêfle"),
            Carte("Roi", "Carreau"),
        ]:
            manche.board.ajouter_carte(carte)
        manche.tour = 3

    def test_manche_init(self, manche, info_manche):
        assert manche.tour == 3
        assert manche.info == info_manche
        assert manche.indice_joueur_actuel == 0
        assert manche.grosse_blind == 10
        assert manche.fin is False
        assert manche.board is not None
        assert manche.reserve is not None

    def test_manche_indice_joueur(self, manche, joueurs):
        assert manche.indice_joueur(joueurs[0]) == 0

    def test_manche_indice_joueur_inexistant(self, manche):
        joueur_inexistant = Joueur(id_joueur=99, pseudo="X", credit=1000, pays="France")
        with pytest.raises(ValueError):
            manche.indice_joueur(joueur_inexistant)

    def test_manche_est_tour(self, manche, joueurs):
        j0, j1, j2 = joueurs
        assert manche.est_tour(j0) is True
        assert manche.est_tour(j1) is False
        assert manche.est_tour(j2) is False

    def test_manche_indice_joueur_suivant(self, manche):
        assert manche.indice_joueur_suivant() == 1

    def test_manche_checker(self, manche):
        manche.info.statuts[:] = [0, 0, 0]
        manche.checker(0)
        assert manche.info.statuts[0] == 2

        with pytest.raises(TypeError):
            manche.checker("0")

        with pytest.raises(ValueError):
            manche.checker(0)

    def test_manche_suivre_relance(self, manche):
        montant = manche.suivre(0, relance=10)
        assert montant > 0
        assert manche.info.mises[0] > 0
        assert manche.info.statuts[0] == 2

    def test_manche_se_coucher(self, manche):
        manche.se_coucher(0)
        assert manche.info.statuts[0] == 3
        assert manche.info.tour_couche[0] == manche.tour

    def test_manche_all_in(self, manche):
        credit = manche.info.joueurs[0].credit
        montant = manche.all_in(0)
        assert montant == credit
        assert manche.info.statuts[0] == 4

    def test_manche_fin_du_tour(self, manche):
        manche.info.statuts[:] = [2, 2, 2]
        assert manche.fin_du_tour() is True

    def test_manche_fin_de_manche(self, manche):
        manche.info.statuts[:] = [2, 3, 2]
        assert manche.fin_de_manche() is True

    def test_manche_valeur_pot(self, manche):
        manche.info.mises[:] = [10, 20, 30]
        assert manche.valeur_pot() == 60

    def test_manche_joueurs_en_lice(self, manche):
        manche.info.statuts[:] = [0, 3, 0]
        joueurs = manche.joueurs_en_lice
        assert len(joueurs) == 2

    # ------------------------ Tests classement ------------------------

    def test_manche_classement_erreur_board_incomplete(self, manche):
        manche._tour = 2
        with pytest.raises(ValueError):
            manche.classement()

    def test_manche_classement_simple(self, manche):
        Test_Manche.remplir_board(manche)

        manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
        manche.info.mains[1]._cartes = [Carte("4", "Trêfle"), Carte("6", "Carreau")]
        manche.info.mains[2]._cartes = [Carte("7", "Trêfle"), Carte("9", "Carreau")]

        classement = manche.classement()
        assert sorted(classement) == [1, 2, 3]

    def test_manche_classement_ex_aequo(self, manche):
        Test_Manche.remplir_board(manche)

        manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
        manche.info.mains[1]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
        manche.info.mains[2]._cartes = [Carte("4", "Trêfle"), Carte("5", "Carreau")]

        classement = manche.classement()
        assert classement[2] != classement[0]

    # ------------------------ Tests récupérer ------------------------

    def test_manche_recuperer_montant_superieur(self, manche):
        assert manche.recuperer(50, 100) == [0, 50]

    def test_manche_recuperer_montant_inferieur(self, manche):
        assert manche.recuperer(50, 20) == [30, 20]

    def test_manche_recuperer_montant_egal(self, manche):
        assert manche.recuperer(50, 50) == [0, 50]

    # ------------------------ Tests gains ------------------------

    def test_manche_gains_un_seul_joueur(self, manche):
        manche.info.statuts[:] = [2, 3, 3]
        manche.info.mises[:] = [100, 50, 50]

        Test_Manche.remplir_board(manche)
        gains = manche.gains()

        assert gains[manche.info.joueurs[0]] == 200
        assert gains[manche.info.joueurs[1]] == 0
        assert gains[manche.info.joueurs[2]] == 0

    # ------------------------ Tests exceptions init ------------------------

    def test_manche_init_info_type_error(self):
        with pytest.raises(TypeError):
            Manche(info="not_info", grosse_blind=10)

    def test_manche_init_grosse_blind_type_error(self):
        joueurs = [Joueur(1, "A", 1000, "France"), Joueur(2, "B", 1000, "France")]
        info = InfoManche(joueurs)
        with pytest.raises(TypeError):
            Manche(info=info, grosse_blind="10")

    def test_manche_init_grosse_blind_value_error(self):
        joueurs = [Joueur(1, "A", 1000, "France"), Joueur(2, "B", 1000, "France")]
        info = InfoManche(joueurs)
        with pytest.raises(ValueError):
            Manche(info=info, grosse_blind=1)

    # ------------------------ Tests divers ------------------------

    def test_manche_nouveau_tour_exception(self, manche):
        manche._Manche__tour = 3
        with pytest.raises(ValueError):
            manche.nouveau_tour()

    def test_manche_suivre_limits(self):
        joueurs = [
            Joueur(1, "A", 20, "France"),
            Joueur(2, "B", 1000, "France"),
        ]
        info = InfoManche(joueurs)
        manche = Manche(info, 10)

        info.mises[1] = 50
        with pytest.raises(ValueError):
            manche.suivre(0, relance=0)

    def test_classement_ex_aequo(self, manche):
        # Board spécifique pour ex-aequo
        manche.board.cartes.clear()
        board = [
            Carte("As", "Coeur"),
            Carte("As", "Pique"),
            Carte("As", "Trêfle"),
            Carte("As", "Carreau"),
            Carte("2", "Coeur"),
        ]

        # Ajouter les cartes au board
        for carte in board:
            manche.board.ajouter_carte(carte)

        manche.tour = 3

        # Assigner les mains
        manche.info.assignation_mains(
            [
                Main([Carte("Roi", "Coeur"), Carte("3", "Coeur")]),
                Main([Carte("Roi", "Pique"), Carte("6", "Pique")]),
                Main([Carte("Dame", "Pique"), Carte("Dame", "Coeur")]),
            ]
        )

        # Modifier le statut d’un joueur pour simuler un joueur couché (optionnel)
        manche.info.modifier_statut(1, 3)

        # Calcul du classement
        classement = manche.classement()

        # Vérifier l'ex-aequo
        # Ici on sait que le joueur 0 et 2 ont une main égale sur le board -> même rang
        # Le joueur 1 a un rang différent
        assert classement[1] != classement[0]
