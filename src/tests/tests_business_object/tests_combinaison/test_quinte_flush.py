"""Implémentation des tests pour la classe QuinteFlush"""

import pytest

from business_object.combinaison.quinte_flush import QuinteFlush


# ---------- Fixtures ----------
@pytest.fixture
def quinte_flush():
    """Fixture qui fournit une quinte flush de test"""
    # kicker = None car QuinteFlush n'a pas de kicker
    return QuinteFlush("As")


@pytest.fixture
def autre_quinte_flush():
    """Fixture pour comparaison"""
    return QuinteFlush("Roi")


# ---------- Tests ----------
def test_creation_quinte_flush(quinte_flush):
    assert quinte_flush.hauteur == "As"
    assert quinte_flush.kicker == ()
    assert QuinteFlush.FORCE() == 8


def test_comparaison_quinte_flush(quinte_flush, autre_quinte_flush):
    assert quinte_flush > autre_quinte_flush
    assert not (autre_quinte_flush > quinte_flush)
    assert quinte_flush == QuinteFlush("As")


def test_egalite_et_non_egalite(quinte_flush, autre_quinte_flush):
    assert quinte_flush == QuinteFlush("As")
    assert quinte_flush != autre_quinte_flush


def test_creation_quinte_flush_invalide():
    # Hauteur non valide
    with pytest.raises(ValueError):
        QuinteFlush(12)


def test_str_quinte_flush(quinte_flush):
    texte = str(quinte_flush)
    assert "QuinteFlush" in texte
    assert "As" in texte
