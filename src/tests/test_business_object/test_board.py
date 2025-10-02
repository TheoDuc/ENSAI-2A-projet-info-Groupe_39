"""Implémentation des tests pour la classe Board"""

import pytest
from tests.test_liste_cartes import AbstractListeCartesTest

from business_object.board import Board


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

        # WHEN
        board = Board()

        # THEN
        assert board.cartes == resultat
