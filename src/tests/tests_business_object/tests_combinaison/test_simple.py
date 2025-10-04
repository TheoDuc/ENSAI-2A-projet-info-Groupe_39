"""Implémentation des tests pour la classe Simple"""

import pytest

from business_object.combinaison.simple import Simple


# ---------- Fixtures ----------
@pytest.fixture
def simple():
    """Fixture qui fournit une simple carte de test"""
    return Simple("As", ("Roi", "Dame", "10", "9"))


@pytest.fixture
def autre_simple():
    """Fixture pour comparaison"""
    return Simple("Roi", ("Dame", "10", "9", "8"))


# ---------- Tests ----------
def test_creation_simple(simple):
    assert simple.hauteur == "As"
    assert simple.kicker == ("Roi", "Dame", "10", "9")
    assert Simple.FORCE() == 0


def test_comparaison_simple(simple, autre_simple):
    assert simple > autre_simple
    assert not (autre_simple > simple)
    assert simple == Simple("As", ("Roi", "Dame", "10", "9"))


def test_egalite_et_non_egalite(simple, autre_simple):
    assert simple == Simple("As", ("Roi", "Dame", "10", "9"))
    assert simple != autre_simple


def test_creation_simple_invalide():
    # Hauteur non valide
    with pytest.raises(ValueError):
        Simple(12, ("Roi", "Dame", "10", "9"))


def test_str_simple(simple):
    texte = str(simple)
    assert "Simple" in texte
    assert "As" in texte
