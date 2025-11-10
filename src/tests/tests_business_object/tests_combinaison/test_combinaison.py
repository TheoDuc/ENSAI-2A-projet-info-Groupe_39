import pytest
from combinaison.combinaison import AbstractCombinaison


# --- Classe factice corrigée pour tests ---
class CombinaisonTest(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        # force fixe pour cette combinaison factice
        return 1

    @classmethod
    def est_present(cls, cartes):
        return True

    @classmethod
    def from_cartes(cls, cartes):
        return cls("As")


# --- Parametrize exhaustif pour init et properties ---
@pytest.mark.parametrize(
    "hauteur,kicker,expected_hauteur,expected_kicker",
    [
        ("As", None, "As", None),
        (["Roi"], None, "Roi", None),
        (("Dame",), None, "Dame", None),
        (["10", "9"], ["8"], ["10", "9"], "8"),
        ("Valet", ["2", "3"], "Valet", ("2", "3")),
        ("As", "Roi", "As", "Roi"),
        (["7"], ("6",), "7", "6"),
        (("5", "4"), ("3", "2"), ["5", "4"], ("3", "2")),
    ],
)
def test_init_et_properties_exhaustif(hauteur, kicker, expected_hauteur, expected_kicker):
    c = CombinaisonTest(hauteur, kicker)
    assert c.hauteur == expected_hauteur
    assert c.kicker == expected_kicker


# --- Test _valeur_comparaison exhaustif ---
@pytest.mark.parametrize(
    "hauteur,kicker",
    [
        ("As", None),
        ("Roi", "Dame"),
        (["10", "9"], ["8"]),
        (("5", "4"), ("3", "2")),
    ],
)
def test_valeur_comparaison_exhaustif(hauteur, kicker):
    c = CombinaisonTest(hauteur, kicker)
    valeur = c._valeur_comparaison()
    assert valeur[0] == CombinaisonTest.FORCE()  # <-- note les parenthèses
    assert all(isinstance(v, int) for v in valeur[1])
    assert all(isinstance(k, int) for k in valeur[2])


# --- Test comparateurs exhaustif ---
def test_comparaison_exhaustif():
    c1 = CombinaisonTest("As", "Roi")
    c2 = CombinaisonTest("As", "Dame")
    c3 = CombinaisonTest("As", "Roi")
    c4 = CombinaisonTest("Roi", None)

    assert c1 > c2
    assert c2 < c1
    assert c1 == c3
    assert c1 != c2
    assert c2 < c4  # test force plus faible


# --- Test __str__ et __repr__ exhaustif ---
@pytest.mark.parametrize(
    "hauteur,kicker",
    [
        ("As", None),
        ("Roi", "Dame"),
        (["10", "9"], ["8"]),
    ],
)
def test_repr_str_exhaustif(hauteur, kicker):
    c = CombinaisonTest(hauteur, kicker)
    s = str(c)
    r = repr(c)
    if isinstance(hauteur, (list, tuple)) and len(hauteur) > 1:
        for h in hauteur:
            assert h in s or " et " in s
    else:
        if hauteur == "As":
            assert "d'As" in s
        else:
            assert hauteur in s
    if kicker is not None:
        if isinstance(kicker, (list, tuple)):
            for k in kicker:
                assert k in r
        else:
            assert kicker in r
    else:
        assert "kicker" not in r


# --- Test verifier_min_cartes ---
def test_verifier_min_cartes_exhaustif():
    # cas ok
    CombinaisonTest.verifier_min_cartes([1, 2, 3, 4, 5])
    CombinaisonTest.verifier_min_cartes([1, 2, 3, 4, 5, 6], n=5)
    # cas erreur
    with pytest.raises(ValueError):
        CombinaisonTest.verifier_min_cartes([1, 2, 3], n=5)
