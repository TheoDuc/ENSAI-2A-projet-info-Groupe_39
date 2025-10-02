"""Implémentation des tests pour la classe Reserve"""

import pytest
from test.test_liste_cartes import AbstractListeCartesTest

from business_object.board import Board
from business_object.carte import Carte
from business_object.main import Main
from business_object.reserve import Reserve


class TestReserve(AbstractListeCartesTest):
    @pytest.fixture
    def liste_cartes(self):
        return Reserve([pytest.as_pique, pytest.dix_coeur])

    @pytest.fixture
    def cls(self):
        return Reserve

    def test_reserve_init_defaut(self):
        # GIVEN
        resultat = [
            Carte(valeur, couleur) for valeur in Carte.VALEURS() for couleur in Carte.COULEURS()
        ]

        # WHEN
        reserve = Reserve()

        # THEN
        assert reserve.cartes == resultat

    def test_reserve_bruler(self):
        # GIVEN
        reserve = Reserve([pytest.deux_coeur, pytest.huit_coeur, pytest.valet_trefle])
        resultat = [pytest.huit_coeur, pytest.valet_trefle, pytest.deux_coeur]

        # WHEN
        reserve.bruler()

        # THEN
        assert reserve.cartes == resultat

    def test_reserve_reveler_succes(self):
        # GIVEN
        reserve = Reserve([pytest.as_pique, pytest.as_trefle, pytest.as_coeur])
        board = Board()
        resultat_reserve = [pytest.as_trefle, pytest.as_coeur]
        resultat_board = [pytest.as_pique]

        # WHEN
        reserve.reveler(board)

        # THEN
        assert reserve.cartes == resultat_reserve
        assert board.cartes == resultat_board

    def test_reserve_reveler_echec(self):
        # GIVEN
        reserve = Reserve([pytest.as_pique, pytest.as_trefle, pytest.as_coeur])
        main = Main()
        message_attendu = f"reserve pas de type Reserve : {type(main)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            reserve.reveler(main)

    def test_reserve_distribuer_succes():
        # GIVEN
        reserve = Reserve(
            [pytest.as_pique, pytest.quatre_trefle, pytest.valet_carreau, pytest.valet_coeur]
        )
        n_joueurs = 2
        resultat = [
            Main(pytest.as_pique, pytest.valet_carreau),
            Main(pytest.quatre_trefle, pytest.valet_coeur),
        ]
        resultat_reserve = []

        # WHEN
        mains = reserve.distribuer(n_joueurs)

        # THEN
        assert mains == resultat
        assert reserve.cartes == resultat_reserve
