"""Implémentation des tests pour la classe Full"""

import pytest

from business_object.combinaison.full import Full


# ---------- Fixtures ----------
@pytest.fixture
def full():
    """Fixture qui fournit un full de test"""
    return Full("Dame", ("Roi", "10"))


@pytest.fixture
def autre_full():
    """Fixture pour comparaison"""
    return Full("Valet", ("As", "9"))


# ---------- Tests ----------
def test_creation_full(full):
    assert full.hauteur == "Dame"
    assert full.kicker == ("Roi", "10")
    assert Full.FORCE() == 6


def test_comparaison_full(full, autre_full):
    assert full > autre_full
    assert not (autre_full > full)
    assert full == Full("Dame", ("Roi", "10"))


def test_egalite_et_non_egalite(full, autre_full):
    assert full == Full("Dame", ("Roi", "10"))
    assert full != autre_full


def test_creation_full_invalide():
    # Hauteur non valide
    with pytest.raises(ValueError):
        Full(12, ("Roi", "10"))


def test_str_full(full):
    texte = str(full)
    assert "Full" in texte
    assert "Dame" in texte
