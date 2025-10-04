"""Implémentation des tests pour la classe Brelan"""

import pytest

from business_object.combinaison.brelan import Brelan


# ---------- Classe de tests ----------
class Test_Brelan:
    def test_creation_brelan(self):
        # GIVEN
        hauteur = "Dame"
        kicker = ("10", "8")

        # WHEN
        b = Brelan(hauteur, kicker)

        # THEN
        assert b.hauteur == "Dame"
        assert b.kicker == ("10", "8")
        assert Brelan.FORCE() == 3

    def test_comparaison_brelan(self):
        # GIVEN
        b_dame = Brelan("Dame", ("10", "8"))
        b_valet = Brelan("Valet", ("Roi", "9"))

        # WHEN / THEN
        assert b_dame > b_valet
        assert b_valet < b_dame
        assert b_dame == Brelan("Dame", ("10", "8"))

    def test_egalite_et_non_egalite(self):
        # GIVEN
        b_dame = Brelan("Dame", ("10", "8"))
        b_valet = Brelan("Valet", ("Roi", "9"))

        # WHEN / THEN
        assert b_dame == Brelan("Dame", ("10", "8"))
        assert b_dame != b_valet

    def test_creation_brelan_invalide(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(ValueError):
            Brelan(12, ("10", "8"))

    def test_str_repr_brelan(self):
        # GIVEN
        b = Brelan("Dame", ("10", "8"))

        # WHEN
        texte_str = str(b)
        texte_repr = repr(b)

        # THEN
        assert "Brelan" in texte_str
        assert "Dame" in texte_str
        assert texte_repr == texte_str
