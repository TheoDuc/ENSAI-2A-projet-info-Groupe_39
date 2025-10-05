"""Implémentation des tests pour la classe Board"""

import pytest

from business_object.board import Board
from tests.tests_business_object.test_liste_cartes import AbstractListeCartesTest


class TestBoard(AbstractListeCartesTest):
    @pytest.fixture
    def liste_cartes(self):
        return Board([pytest.as_pique, pytest.dix_coeur])

    @pytest.fixture
    def cls(self):
        return Board

    def test_board_init_defaut(self):
        # GIVEN
        resultat = []
        resultat = []

        # WHEN
        board = Board(None)

        # THEN
        assert board.cartes == resultat

    def test_board_init_trop_grand(self, liste_cartes):
        # GIVEN
        cartes = [
            pytest.as_pique,
            pytest.dix_coeur,
            pytest.as_pique,
            pytest.dix_coeur,
            pytest.as_pique,
            pytest.dix_coeur,
        ]
        message_attendu = f"Le nombre de carte dans le board est trop grand : {len(cartes)}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Board(cartes)
