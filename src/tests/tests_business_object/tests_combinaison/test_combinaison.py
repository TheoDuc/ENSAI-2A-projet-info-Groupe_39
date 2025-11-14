import pytest
from business_object.combinaison.combinaison import AbstractCombinaison


class CombinaisonTest(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 1

    @classmethod
    def est_present(cls, cartes):
        return True

    @classmethod
    def from_cartes(cls, cartes):
        return cls("As")


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
def test_combinaison_init_et_properties(hauteur, kicker, expected_hauteur, expected_kicker):
    # GIVEN: Une hauteur et un kicker
    c = CombinaisonTest(hauteur, kicker)

    # WHEN: On accède aux propriétés
    h = c.hauteur
    k = c.kicker

    # THEN: Les propriétés doivent correspondre aux valeurs normalisées
    assert h == expected_hauteur
    assert k == expected_kicker


# ===========================================
# Test _valeur_comparaison
# ===========================================
@pytest.mark.parametrize(
    "hauteur,kicker",
    [
        ("As", None),
        ("Roi", "Dame"),
        (["10", "9"], ["8"]),
        (("5", "4"), ("3", "2")),
    ],
)
def test_combinaison_valeur_comparaison(hauteur, kicker):
    # GIVEN: Une combinaison avec hauteur et kicker
    c = CombinaisonTest(hauteur, kicker)

    # WHEN: On calcule la valeur de comparaison
    force, hauteur_vals, kicker_vals = c._valeur_comparaison()

    # THEN: FORCE doit être un int
    assert isinstance(force, int)
    # THEN: Hauteur et kicker doivent être des tuples d'int
    assert all(isinstance(v, int) for v in hauteur_vals)
    assert all(isinstance(k, int) for k in kicker_vals)


# ===========================================
# Test comparateurs
# ===========================================
def test_combinaison_comparaison():
    # GIVEN: Plusieurs combinaisons
    c1 = CombinaisonTest("As", "Roi")
    c2 = CombinaisonTest("As", "Dame")
    c3 = CombinaisonTest("As", "Roi")
    c4 = CombinaisonTest("Roi", None)

    # WHEN / THEN: Comparaisons selon _valeur_comparaison
    assert c1 > c2  # kicker "Roi" > "Dame"
    assert c2 < c1
    assert c1 == c3
    assert c1 != c2
    # Comme toutes les forces =1, on ne teste pas c2 < c4
    assert c2 != c4


# ===========================================
# Test __str__ et __repr__
# ===========================================
@pytest.mark.parametrize(
    "hauteur,kicker",
    [
        ("As", None),
        ("Roi", "Dame"),
        (["10", "9"], ["8"]),
    ],
)
def test_combinaison_repr_str(hauteur, kicker):
    # GIVEN
    c = CombinaisonTest(hauteur, kicker)

    # WHEN
    s = str(c)
    r = repr(c)

    # THEN
    # Hauteur apparaît dans str
    if isinstance(hauteur, (list, tuple)) and len(hauteur) > 1:
        for h in hauteur:
            assert h in s or " et " in s
    else:
        if hauteur == "As":
            assert "d'As" in s
        else:
            assert hauteur in s

    # kicker apparaît dans repr si présent
    if kicker is not None:
        if isinstance(kicker, (list, tuple)):
            for k in kicker:
                assert k in r
        else:
            assert kicker in r
    else:
        assert "kicker" not in r


# ===========================================
# Test verifier_min_cartes
# ===========================================
def test_combinaison_verifier_min_cartes():
    # GIVEN / WHEN: Liste de cartes suffisante
    CombinaisonTest.verifier_min_cartes([1, 2, 3, 4, 5])
    CombinaisonTest.verifier_min_cartes([1, 2, 3, 4, 5, 6], n=5)

    # THEN: Erreur si moins de cartes
    with pytest.raises(ValueError):
        CombinaisonTest.verifier_min_cartes([1, 2, 3], n=5)
