"""Implémentation des tests pour la classe DoublePaire"""

import pytest

from business_object.combinaison.double_paire import DoublePaire


# ---------- Fixtures ----------
@pytest.fixture
def doublepaire():
    """Fixture qui fournit une double paire de test"""
    return DoublePaire("Dame", ("Roi", "10"))


@pytest.fixture
def autre_doublepaire():
    """Fixture pour comparaison"""
    return DoublePaire("Valet", ("As", "9"))


# ---------- Tests ----------
def test_creation_doublepaire(doublepaire):
    assert doublepaire.hauteur == "Dame"
    assert doublepaire.kicker == ("Roi", "10")
    assert DoublePaire.FORCE() == 2


def test_comparaison_doublepaire(doublepaire, autre_doublepaire):
    assert doublepaire > autre_doublepaire
    assert not (autre_doublepaire > doublepaire)
    assert doublepaire == DoublePaire("Dame", ("Roi", "10"))


def test_egalite_et_non_egalite(doublepaire, autre_doublepaire):
    assert doublepaire == DoublePaire("Dame", ("Roi", "10"))
    assert doublepaire != autre_doublepaire


def test_creation_doublepaire_invalide():
    with pytest.raises(ValueError):
        DoublePaire(12, ("Roi", "10"))  # hauteur non valide


def test_str_doublepaire(doublepaire):
    texte = str(doublepaire)
    assert "DoublePaire" in texte
    assert "Dame" in texte
