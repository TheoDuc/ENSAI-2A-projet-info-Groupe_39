import pytest

from business_object.combinaison.combinaison import AbstractCombinaison


class CombinaisonConcrete(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 0

    @classmethod
    def est_present(cls, cartes):
        # Retourne False pour les tests, pas de logique nécessaire
        return False

    @classmethod
    def from_cartes(cls, cartes):
        # Retourne un objet avec hauteur "2" et kicker vide
        return cls("2", ())


@pytest.fixture
def combinaison():
    return CombinaisonConcrete("2", ("3",))


def test_attributs(combinaison):
    assert combinaison.hauteur == "2"
    assert combinaison.kicker == ("3",)
    assert combinaison.FORCE() == 0


def test_str_repr(combinaison):
    assert str(combinaison) == "CombinaisonConcrete(2, ('3',))"
    assert repr(combinaison) == str(combinaison)


def test_comparaison():
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

    a = CombinaisonA("3")
    b = CombinaisonB("2")

    assert a > b
    assert b < a
    assert a != b
