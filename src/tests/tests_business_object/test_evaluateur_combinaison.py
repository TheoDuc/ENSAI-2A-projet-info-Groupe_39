"""Implémentation des tests pour la classe EvaluateurCombinaison"""

import pytest

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan
from business_object.combinaison.paire import Paire
from business_object.combinaison.simple import Simple
from business_object.evaluateur_combinaison import EvaluateurCombinaison


# ---------- Fixtures ----------
@pytest.fixture
def cartes_simple():
    return [
        Carte("2", "Coeur"),
        Carte("5", "Pique"),
        Carte("7", "Trêfle"),
        Carte("9", "Carreau"),
        Carte("As", "Pique"),
    ]


@pytest.fixture
def cartes_paire():
    return [
        Carte("Dame", "Coeur"),
        Carte("Dame", "Trêfle"),
        Carte("7", "Trêfle"),
        Carte("9", "Carreau"),
        Carte("As", "Pique"),
    ]


@pytest.fixture
def cartes_brelan():
    return [
        Carte("Roi", "Coeur"),
        Carte("Roi", "Trêfle"),
        Carte("Roi", "Pique"),
        Carte("9", "Carreau"),
        Carte("As", "Pique"),
    ]


# ---------- Tests ----------
def test_eval_simple(cartes_simple):
    combi = EvaluateurCombinaison.eval(cartes_simple)
    assert isinstance(combi, Simple)
    assert combi.hauteur == "As"


def test_eval_paire(cartes_paire):
    combi = EvaluateurCombinaison.eval(cartes_paire)
    assert isinstance(combi, Paire)
    assert combi.hauteur == "Dame"


def test_eval_brelan(cartes_brelan):
    combi = EvaluateurCombinaison.eval(cartes_brelan)
    assert isinstance(combi, Brelan)
    assert combi.hauteur == "Roi"
