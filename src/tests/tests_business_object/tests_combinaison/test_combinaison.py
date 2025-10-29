from business_object.combinaison.combinaison import AbstractCombinaison


# ---------- Classe concrète pour les tests ----------
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
        return "CombinaisonTest"  # version simple pour utilisateur

    def __repr__(self):
        return (
            f"CombinaisonTest(hauteur='{self.hauteur}', kicker={self.kicker})"  # version technique
        )


# ---------- Tests ----------
class Test_AbstractCombinaison:
    """Tests unitaires simplifiés pour AbstractCombinaison"""

    def test_AbstractCombinaison_attributs(self):
        hauteur = "2"
        kicker = ("3", "4", "5", "6")
        c = CombinaisonTest(hauteur, kicker)
        assert c.hauteur == "2"
        assert c.kicker == ("3", "4", "5", "6")
        assert CombinaisonTest.FORCE() == 0

    def test_AbstractCombinaison_str_et_repr(self):
        c = CombinaisonTest("2", ("3", "4", "5", "6"))
        texte_str = str(c)
        texte_repr = repr(c)
        assert texte_str == "CombinaisonTest"
        assert texte_repr == "CombinaisonTest(hauteur='2', kicker=('3', '4', '5', '6'))"

    def test_AbstractCombinaison_comparaison(self):
        c1 = CombinaisonTest("2", ("3", "4", "5", "6"))
        c2 = CombinaisonTest("2", ("3", "4", "5", "7"))
        assert c1 == CombinaisonTest("2", ("3", "4", "5", "6"))
        assert c1 != c2
        assert (c1 < c2) or (c1 > c2)
