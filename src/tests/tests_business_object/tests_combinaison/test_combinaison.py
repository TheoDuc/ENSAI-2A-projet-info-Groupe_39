import pytest

from business_object.carte import Carte
from business_object.combinaison.combinaison import AbstractCombinaison


class CombinaisonTest(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 0

    @classmethod
    def est_present(cls, cartes):
        return len(cartes) >= 1

    @classmethod
    def from_cartes(cls, cartes):
        hauteur = "2"
        kicker = ("3", "4", "5", "6")
        return cls(hauteur, kicker)

    def __str__(self):
        return "CombinaisonTest"

    def __repr__(self):
        return f"CombinaisonTest(hauteur='{self.hauteur}', kicker={self.kicker})"


# ---------- Tests ----------
class Test_AbstractCombinaison:
    """Tests unitaires complets pour AbstractCombinaison"""

    def test_attributs_base(self):
        c = CombinaisonTest("2", ("3", "4", "5", "6"))
        assert c.hauteur == "2"
        assert c.kicker == ("3", "4", "5", "6")
        assert CombinaisonTest.FORCE() == 0

    def test_str_et_repr(self):
        c = CombinaisonTest("2", ("3", "4", "5", "6"))
        assert str(c) == "CombinaisonTest"
        assert repr(c) == "CombinaisonTest(hauteur='2', kicker=('3', '4', '5', '6'))"

    def test_comparaison(self):
        c1 = CombinaisonTest("2", ("3", "4", "5", "6"))
        c2 = CombinaisonTest("2", ("3", "4", "5", "7"))
        assert c1 == CombinaisonTest("2", ("3", "4", "5", "6"))
        assert c1 != c2
        assert (c1 < c2) or (c1 > c2)

    def test_verifier_min_cartes(self):
        # devrait passer
        AbstractCombinaison.verifier_min_cartes([1, 2, 3, 4, 5])
        # devrait lever ValueError
        with pytest.raises(ValueError):
            AbstractCombinaison.verifier_min_cartes([1, 2], n=5)

    def test_init_variante_hauteur_kicker(self):
        # kicker None
        c = CombinaisonTest("As", None)
        assert c.kicker is None

        # kicker string
        c = CombinaisonTest("As", "Roi")
        assert c.kicker == "Roi"

        # kicker tuple
        c = CombinaisonTest("Roi", ("Dame", "Valet"))
        assert c.kicker == ("Dame", "Valet")

        # hauteur list >1 élément
        c = CombinaisonTest(["As", "Roi"], "Dame")
        assert c.hauteur == ["As", "Roi"]
        assert c.kicker == "Dame"

        # hauteur list 1 élément
        c = CombinaisonTest(["As"], "Dame")
        assert c.hauteur == "As"

    def test_fmt_valeurs(self):
        c = CombinaisonTest("As", None)
        # tuple d'un seul élément
        assert c._fmt_valeurs(("As",)) == "As"
        # tuple de plusieurs éléments
        assert c._fmt_valeurs(("As", "Roi")) == "As et Roi"
        # liste
        assert c._fmt_valeurs(["As", "Roi"]) == "As et Roi"
        # None
        assert c._fmt_valeurs(None) is None

    def test_valeur_comparaison_variante(self):
        # kicker None
        c = CombinaisonTest("As", None)
        force, hauteur_vals, kicker_vals = c._valeur_comparaison()
        assert force == 0
        assert hauteur_vals == (Carte.VALEURS().index("As"),)
        assert kicker_vals == ()

        # kicker tuple
        c = CombinaisonTest("Roi", ("Dame", "Valet"))
        force, hauteur_vals, kicker_vals = c._valeur_comparaison()
        assert hauteur_vals == (Carte.VALEURS().index("Roi"),)
        assert kicker_vals == (
            Carte.VALEURS().index("Dame"),
            Carte.VALEURS().index("Valet"),
        )
