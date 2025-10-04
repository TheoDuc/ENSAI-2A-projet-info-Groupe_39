"""Implémentation des tests pour la classe Couleur"""

import pytest

from business_object.combinaison.couleur import Couleur


# ---------- Fixtures ----------
@pytest.fixture
def couleur():
    """Fixture qui fournit une couleur de test"""
    return Couleur("As")  # kicker optionnel pour Couleur


@pytest.fixture
def autre_couleur():
    """Fixture pour comparaison"""
    return Couleur("Roi")


# ---------- Tests ----------
def test_creation_couleur(couleur):
    assert couleur.hauteur == "As"
    assert couleur.kicker == ()  # pas de kicker fourni
    assert Couleur.FORCE() == 5


def test_comparaison_couleur(couleur, autre_couleur):
    assert couleur > autre_couleur
    assert not (autre_couleur > couleur)
    assert couleur == Couleur("As")


def test_egalite_et_non_egalite(couleur, autre_couleur):
    assert couleur == Couleur("As")
    assert couleur != autre_couleur


def test_creation_couleur_invalide():
    with pytest.raises(ValueError):
        Couleur(12)  # hauteur non valide


def test_str_couleur(couleur):
    texte = str(couleur)
    assert "Couleur" in texte
    assert "As" in texte
