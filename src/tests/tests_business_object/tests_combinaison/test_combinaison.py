from business_object.combinaison.combinaison import AbstractCombinaison


# ---------- Classe concrète pour les tests ----------
class CombinaisonTest(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 0

    @classmethod
    def est_present(cls, cartes):
        return False

    @classmethod
    def from_cartes(cls, cartes):
        return cls("2", ("3",))


# ---------- Tests ----------
class Test_AbstractCombinaison:
    """Tests unitaires simplifiés pour AbstractCombinaison"""

    def test_attributs(self):
        # GIVEN : hauteur et kicker
        hauteur = "2"
        kicker = ("3",)

        # WHEN : création d'une combinaison
        c = CombinaisonTest(hauteur, kicker)

        # THEN : vérification des attributs
        assert c.hauteur == "2"
        assert c.kicker == ("3",)
        assert CombinaisonTest.FORCE() == 0

    def test_str_et_repr(self):
        # GIVEN : une combinaison
        c = CombinaisonTest("2", ("3",))

        # WHEN : conversion en str et repr
        texte_str = str(c)
        texte_repr = repr(c)

        # THEN : représentations
        assert texte_str == "CombinaisonTest(2, ('3',))"
        assert texte_repr == texte_str

    def test_comparaison(self):
        # GIVEN : deux combinaisons
        c1 = CombinaisonTest("2", ("3",))
        c2 = CombinaisonTest("2", ("4",))

        # THEN : égalité et ordre
        assert c1 == CombinaisonTest("2", ("3",))
        assert c1 != c2
        # Comparaison basée sur kicker si FORCE identique
        assert (c1 < c2) or (c1 > c2)
