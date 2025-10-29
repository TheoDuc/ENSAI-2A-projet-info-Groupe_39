"""Implémentation des tests pour la classe Manche"""

import pytest

from business_object.board import Board
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main
from business_object.manche import Manche
from business_object.reserve import Reserve


class TestManche:
    # Fixtures
    @pytest.fixture
    def joueurs(self):
        return [
            Joueur(1, "Alice", 500, "France"),
            Joueur(2, "Bob", 500, "Canada"),
        ]

    @pytest.fixture
    def info_manche(self, joueurs):
        return InfoManche(joueurs)

    # Tests d’initialisation
    def test_manche_init_succes(self, info_manche):
        # GIVEN
        grosse_blind = 100

        # WHEN
        manche = Manche(info_manche, grosse_blind)

        # THEN
        assert manche.info == info_manche
        assert isinstance(manche.reserve, Reserve)
        assert isinstance(manche.board, Board)
        assert manche.grosse_blind == 100
        assert manche.tour == 0
        assert manche.pot == 0

    @pytest.mark.parametrize(
        "info, grosse_blind, exception, msg",
        [
            ("pas_info", 100, TypeError, "info"),
            (None, "cent", TypeError, "entier"),
            (None, 0, ValueError, "strictement positif"),
            (None, -50, ValueError, "strictement positif"),
        ],
    )
    def test_manche_init_erreurs(self, joueurs, info, grosse_blind, exception, msg):
        # GIVEN
        if info is None:
            info = InfoManche(joueurs)

        # WHEN / THEN
        with pytest.raises(exception, match=msg):
            Manche(info, grosse_blind)

    def test_tours_constante(self):
        # GIVEN / WHEN
        tours = Manche.TOURS()

        # THEN
        assert tours == ("preflop", "flop", "turn", "river")

    def test_manche_str(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)

        # WHEN
        texte = str(manche)

        # THEN
        assert "Manche(" in texte
        assert "tour=0" in texte
        assert "pot=0" in texte
        assert "grosse_blind=100" in texte

    # -------------------- Tests des tours -------------------- #
    def test_preflop(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)

        # WHEN
        manche.preflop()

        # THEN
        assert all(isinstance(m, Main) for m in manche.info.mains)
        assert manche.info.mises[0] == 50
        assert manche.info.mises[1] == 100

    def test_flop(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)

        # WHEN
        manche.flop()

        # THEN
        assert len(manche.board.cartes) == 3
        assert manche.tour == 1

    def test_turn(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)

        # WHEN
        manche.turn()

        # THEN
        assert len(manche.board.cartes) == 1
        assert manche.tour == 1

    def test_river(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)

        # WHEN
        manche.river()

        # THEN
        assert len(manche.board.cartes) == 1
        assert manche.tour == 1

    # -------------------- Tests pot et gestion joueurs -------------------- #
    def test_ajouter_au_pot(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)

        # WHEN
        manche.ajouter_au_pot(200)

        # THEN
        assert manche.pot == 200

    def test_joueur_suivant(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)
        info_manche.tour_couche[0] = True
        info_manche.tour_couche[1] = None

        # WHEN
        indice = manche.joueur_suivant()

        # THEN
        assert indice == 1

    def test_joueur_suivant_tous_couches(self, info_manche):
        # GIVEN
        manche = Manche(info_manche, 100)
        info_manche.tour_couche[:] = [True, True]

        # WHEN / THEN
        with pytest.raises(ValueError, match="Tous les joueurs ne peuvent être couchés."):
            manche.joueur_suivant()
