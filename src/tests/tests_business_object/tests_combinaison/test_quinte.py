"""Implémentation des tests pour la classe Quinte"""

import pytest

from business_object.combinaison.quinte import Quinte


# ---------- Fixtures ----------
@pytest.fixture
def quinte():
    """Fixture qui fournit une quinte de test"""
    # kicker = None car Quinte n'a pas de kicker
    return Quinte("As")


@pytest.fixture
def autre_quinte():
    """Fixture pour comparaison"""
    return Quinte("Roi")


# ---------- Tests ----------
def test_creation_quinte(quinte):
    assert quinte.hauteur == "As"
    assert quinte.kicker == ()
    assert Quinte.FORCE() == 4


def test_comparaison_quinte(quinte, autre_quinte):
    assert quinte > autre_quinte
    assert not (autre_quinte > quinte)
    assert quinte == Quinte("As")


def test_egalite_et_non_egalite(quinte, autre_quinte):
    assert quinte == Quinte("As")
    assert quinte != autre_quinte


def test_creation_quinte_invalide():
    # Hauteur non valide
    with pytest.raises(ValueError):
        Quinte(12)


def test_str_quinte(quinte):
    texte = str(quinte)
    assert "Quinte" in texte
    assert "As" in texte
