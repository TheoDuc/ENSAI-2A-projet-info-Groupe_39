"""Implémentation des tests pour la classe Manche"""

import pytest
from business_object.manche import Manche
from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from business_object.board import Board


class TestManche:

    def test_manche_init_succes(self):
        # GIVEN
        info = InfoManche()
        reserve = Reserve()
        board = Board()
        grosse_blind = 100

        # WHEN
        manche = Manche(info, reserve, board, grosse_blind)

        # THEN
        assert manche.info == info
        assert manche.reserve == reserve
        assert manche.board == board
        assert manche.grosse_blind == 100
        assert manche.tour == 0
        assert manche.pot == 0

    @pytest.mark.parametrize(
        "info, reserve, board, grosse_blind, exception, msg",
        [
            ("pas_info", Reserve(), Board(), 100, TypeError, "info"),
            (InfoManche(), "pas_reserve", Board(), 100, TypeError, "reserve"),
            (InfoManche(), Reserve(), "pas_board", 100, TypeError, "board"),
            (InfoManche(), Reserve(), Board(), "cent", TypeError, "grosse_blind"),
            (InfoManche(), Reserve(), Board(), 0, ValueError, "grosse blind"),
            (InfoManche(), Reserve(), Board(), -50, ValueError, "grosse blind"),
        ]
    )
    def test_manche_init_erreurs(self, info, reserve, board, grosse_blind, exception, msg):
        # GIVEN / WHEN / THEN
        with pytest.raises(exception, match=msg):
            Manche(info, reserve, board, grosse_blind)

    def test_tours_constante(self):
        # GIVEN / WHEN
        tours = Manche.TOURS()

        # THEN
        assert tours == ("preflop", "flop", "turn", "river")
