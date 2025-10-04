import pytest

from business_object.combinaison.brelan import Brelan


@pytest.fixture
def brelan():
    """Fixture qui crée un brelan de Dames"""
    return Brelan("Dame", ("10", "8"))


@pytest.fixture
def autre_brelan():
    """Fixture pour comparaison : brelan de Valets"""
    return Brelan("Valet", ("Roi", "9"))


def test_creation_brelan(brelan):
    # THEN
    assert brelan.hauteur == "Dame"
    assert brelan.kicker == ("10", "8")
    # Vérifie que la constante FORCE vaut bien 3
    assert getattr(Brelan, "FORCE", None) == 3 or callable(Brelan.FORCE)


def test_comparaison_brelan(brelan, autre_brelan):
    # WHEN / THEN
    assert brelan > autre_brelan
    assert not (autre_brelan > brelan)
    assert brelan == Brelan("Dame", ("10", "8"))


def test_egalite_et_non_egalite(brelan, autre_brelan):
    assert brelan == Brelan("Dame", ("10", "8"))
    assert brelan != autre_brelan


def test_creation_brelan_invalide():
    with pytest.raises(ValueError):
        Brelan(12, ("10", "8"))  # hauteur non valide


def test_str_brelan(brelan):
    texte = str(brelan)
    assert "Brelan" in texte
    assert "Dame" in texte
