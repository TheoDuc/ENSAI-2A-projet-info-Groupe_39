import pytest

from business_object.carte import Carte
from business_object.combinaison.combinaison import AbstractCombinaison


# Classe concrète minimale pour les tests
class CombinaisonTest(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 0

    @classmethod
    def est_present(cls, cartes):
        return len(cartes) >= 1

    @classmethod
    def from_cartes(cls, cartes):
        return cls("2", ("3", "4", "5", "6"))

    def __str__(self):
        return "CombinaisonTest"

    def __repr__(self):
        return f"CombinaisonTest(hauteur='{self.hauteur}', kicker={self.kicker})"


class TestAbstractCombinaison:
    def test_attributs_str_repr(self):
        # kicker comme tuple
        c = CombinaisonTest("As", ("Roi", "Dame"))
        assert c.hauteur == "As"
        assert c.kicker == ("Roi", "Dame")
        assert str(c) == "CombinaisonTest"
        assert repr(c) == "CombinaisonTest(hauteur='As', kicker=('Roi', 'Dame'))"

        # kicker comme str
        c2 = CombinaisonTest("10", "Valet")
        assert c2.kicker == "Valet"

        # kicker None
        c3 = CombinaisonTest("2", None)
        assert c3.kicker is None

        # hauteur comme list de 1 élément
        c4 = CombinaisonTest(["3"], "4")
        assert c4.hauteur == "3"

        # hauteur comme list de plusieurs éléments
        c5 = CombinaisonTest(["5", "6"], ["7", "8"])
        assert c5.hauteur == ["5", "6"]
        assert c5.kicker == ("7", "8")

    def test_valeur_comparaison_et_comparaison(self):
        c1 = CombinaisonTest("As", ("Roi", "Dame"))
        c2 = CombinaisonTest("As", ("Roi", "Valet"))
        # égalité avec lui-même
        c_copy = CombinaisonTest("As", ("Roi", "Dame"))
        assert c1 == c_copy
        assert c1 != c2
        assert (c1 < c2) or (c1 > c2)

        # vérifie que la valeur de comparaison correspond aux indices Carte.VALEURS()
        force, hauteur_vals, kicker_vals = c1._valeur_comparaison()
        assert force == 0
        assert hauteur_vals == (Carte.VALEURS().index("As"),)
        assert kicker_vals == (
            Carte.VALEURS().index("Roi"),
            Carte.VALEURS().index("Dame"),
        )

    def test_verifier_min_cartes(self):
        AbstractCombinaison.verifier_min_cartes([1, 2, 3, 4, 5])
        # doit lever une exception si moins de 5 cartes
        with pytest.raises(ValueError):
            AbstractCombinaison.verifier_min_cartes([1, 2], n=5)

    def test_from_cartes_et_est_present(self):
        cartes = [Carte("2", "Coeur")]
        c = CombinaisonTest.from_cartes(cartes)
        assert isinstance(c, CombinaisonTest)
        assert CombinaisonTest.est_present(cartes)
        assert not CombinaisonTest.est_present([])
