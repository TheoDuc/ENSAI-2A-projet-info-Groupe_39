"""Implémentation des tests pour la classe Carre"""

import pytest

from business_object.combinaison.carre import Carre


# ---------- Fixtures ----------
@pytest.fixture
def carre():
    """Fixture qui fournit un carré de test"""
    return Carre("Dame", ("10", "8", "7"))


@pytest.fixture
def autre_carre():
    """Fixture pour comparaison"""
    return Carre("Valet", ("Roi", "9", "6"))


# ---------- Tests ----------
def test_creation_carre(carre):
    assert carre.hauteur == "Dame"
    assert carre.kicker == ("10", "8", "7")
    assert Carre.FORCE() == 7  # appel correct de la méthode


def test_comparaison_carre(carre, autre_carre):
    assert carre > autre_carre
    assert not (autre_carre > carre)
    assert carre == Carre("Dame", ("10", "8", "7"))


def test_egalite_et_non_egalite(carre, autre_carre):
    assert carre == Carre("Dame", ("10", "8", "7"))
    assert carre != autre_carre


def test_creation_carre_invalide():
    # hauteur non valide
    with pytest.raises(ValueError):
        Carre(12, ("10", "8", "7"))


def test_str_carre(carre):
    texte = str(carre)
    assert "Carre" in texte
    assert "Dame" in texte
