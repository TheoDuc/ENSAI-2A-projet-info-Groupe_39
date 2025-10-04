"""Implémentation des tests pour la classe AbstractCombinaison"""

from business_object.combinaison.combinaison import AbstractCombinaison


# ---------- Classe concrète pour les tests ----------
class Combinaison(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 0

    @classmethod
    def est_present(cls, cartes):
        return False  # Pas de logique réelle nécessaire pour le test

    @classmethod
    def from_cartes(cls, cartes):
        return cls("2", ())  # Retourne une instance simple


# ---------- Classe de tests ----------
class Test_Combinaison:
    """Tests unitaires pour la classe AbstractCombinaison"""

    def test_attributs(self):
        # GIVEN
        hauteur = "2"
        kicker = ("3",)

        # WHEN
        combinaison = Combinaison(hauteur, kicker)

        # THEN
        assert combinaison.hauteur == "2"
        assert combinaison.kicker == ("3",)
        assert combinaison.FORCE() == 0

    def test_str_repr(self):
        # GIVEN
        combinaison = Combinaison("2", ("3",))

        # WHEN
        texte_str = str(combinaison)
        texte_repr = repr(combinaison)

        # THEN
        assert texte_str == "Combinaison(2, ('3',))"
        assert texte_repr == texte_str

    def test_comparaison(self):
        # GIVEN
        class CombinaisonA(AbstractCombinaison):
            @classmethod
            def FORCE(cls) -> int:
                return 1

            @classmethod
            def est_present(cls, cartes):
                return False

            @classmethod
            def from_cartes(cls, cartes):
                return cls("3")

        class CombinaisonB(AbstractCombinaison):
            @classmethod
            def FORCE(cls) -> int:
                return 0

            @classmethod
            def est_present(cls, cartes):
                return False

            @classmethod
            def from_cartes(cls, cartes):
                return cls("2")

        # WHEN
        a = CombinaisonA("3")
        b = CombinaisonB("2")

        # THEN
        assert a > b
        assert b < a
        assert a != b
