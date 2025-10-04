"""Implémentation des tests pour la classe Paire"""

import pytest

from business_object.combinaison.paire import Paire


# ---------- Fixtures ----------
@pytest.fixture
def paire():
    """Fixture qui fournit une paire de test"""
    return Paire("Dame", ("Roi", "10", "8"))


@pytest.fixture
def autre_paire():
    """Fixture pour comparaison"""
    return Paire("Valet", ("As", "9", "7"))


# ---------- Tests ----------
def test_creation_paire(paire):
    assert paire.hauteur == "Dame"
    assert paire.kicker == ("Roi", "10", "8")
    assert Paire.FORCE() == 1


def test_comparaison_paire(paire, autre_paire):
    assert paire > autre_paire
    assert not (autre_paire > paire)
    assert paire == Paire("Dame", ("Roi", "10", "8"))


def test_egalite_et_non_egalite(paire, autre_paire):
    assert paire == Paire("Dame", ("Roi", "10", "8"))
    assert paire != autre_paire


def test_creation_paire_invalide():
    # Hauteur non valide
    with pytest.raises(ValueError):
        Paire(12, ("Roi", "10", "8"))


def test_str_paire(paire):
    texte = str(paire)
    assert "Paire" in texte
    assert "Dame" in texte
