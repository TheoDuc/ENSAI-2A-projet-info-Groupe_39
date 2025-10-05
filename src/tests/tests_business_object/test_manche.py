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
        grosse_blind = 100

        # WHEN
        manche = Manche(info, grosse_blind)

        # THEN
        assert manche.info == info
        assert manche.reserve == Reserve(None)
        assert manche.board == Board([])
        assert manche.grosse_blind == 100
        assert manche.tour == 0
        assert manche.pot == 0

    @pytest.mark.parametrize(
        "info, grosse_blind, exception, msg",
        [
            ("pas_info", 100, TypeError, "info"),
            (InfoManche(), "cent", TypeError, "grosse_blind"),
            (InfoManche(), 0, ValueError, "grosse blind"),
            (InfoManche(), -50, ValueError, "grosse blind"),
        ]
    )
    def test_manche_init_erreurs(self, info, grosse_blind, exception, msg):
        # GIVEN / WHEN / THEN
        with pytest.raises(exception, match=msg):
            Manche(info, grosse_blind)

    def test_tours_constante(self):
        # GIVEN / WHEN
        tours = Manche.TOURS()

        # THEN
        assert tours == ("preflop", "flop", "turn", "river")

    def test_manche_str(self):
        # GIVEN
        info = InfoManche()
        grosse_blind = 100

        # WHEN
        manche = Manche(info, grosse_blind)

        # THEN
        assert str(manche) == "Manche(tour=0, pot=0, grosse_blind=100, board=[])"