"""Implémentation des tests pour la classe Carre"""

import pytest

from business_object.combinaison.carre import Carre


# ---------- Classe de tests ----------
class Test_Carre:
    def test_creation_carre(self):
        # GIVEN
        hauteur = "Dame"
        kicker = ("10", "8", "7")

        # WHEN
        c = Carre(hauteur, kicker)

        # THEN
        assert c.hauteur == "Dame"
        assert c.kicker == ("10", "8", "7")
        assert Carre.FORCE() == 7

    def test_comparaison_carre(self):
        # GIVEN
        c_dame = Carre("Dame", ("10", "8", "7"))
        c_valet = Carre("Valet", ("Roi", "9", "6"))

        # WHEN / THEN
        assert c_dame > c_valet
        assert c_valet < c_dame
        assert c_dame == Carre("Dame", ("10", "8", "7"))

    def test_egalite_et_non_egalite(self):
        # GIVEN
        c_dame = Carre("Dame", ("10", "8", "7"))
        c_valet = Carre("Valet", ("Roi", "9", "6"))

        # WHEN / THEN
        assert c_dame == Carre("Dame", ("10", "8", "7"))
        assert c_dame != c_valet

    def test_creation_carre_invalide(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(ValueError):
            Carre(12, ("10", "8", "7"))

    def test_str_repr_carre(self):
        # GIVEN
        c = Carre("Dame", ("10", "8", "7"))

        # WHEN
        texte_str = str(c)
        texte_repr = repr(c)

        # THEN
        assert "Carre" in texte_str
        assert "Dame" in texte_str
        assert texte_repr == texte_str
