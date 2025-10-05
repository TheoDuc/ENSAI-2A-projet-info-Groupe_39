"""Implémentation des tests pour la classe Simple"""

import pytest

from business_object.combinaison.simple import Simple


# ---------- Fixtures ----------
@pytest.fixture
def simple():
    """Fixture qui fournit une carte Simple de test"""
    return Simple("As", ("Roi", "Dame", "10", "9"))


@pytest.fixture
def autre_simple():
    """Fixture pour comparaison"""
    return Simple("Roi", ("Dame", "10", "9", "8"))


# ---------- Classe de tests ----------
class Test_Simple:
    """Tests unitaires pour la combinaison Simple"""

    def test_creation_simple(self, simple):
        # GIVEN
        hauteur = "As"
        kicker = ("Roi", "Dame", "10", "9")

        # WHEN
        s = simple

        # THEN
        assert s.hauteur == "As"
        assert s.kicker == ("Roi", "Dame", "10", "9")
        assert Simple.FORCE() == 0

    def test_comparaison_simple(self, simple, autre_simple):
        # GIVEN
        s_as = simple
        s_roi = autre_simple

        # WHEN
        resultat_sup = s_as > s_roi
        resultat_inf = s_roi > s_as
        resultat_egal = s_as == Simple("As", ("Roi", "Dame", "10", "9"))

        # THEN
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self, simple, autre_simple):
        # GIVEN
        s_as = simple
        s_roi = autre_simple

        # THEN
        assert s_roi < s_as

    def test_egalite_et_non_egalite(self, simple, autre_simple):
        # GIVEN
        s_as = simple
        s_roi = autre_simple

        # WHEN / THEN
        assert s_as == Simple("As", ("Roi", "Dame", "10", "9"))
        assert s_as != s_roi

    def test_creation_simple_invalide(self):
        # GIVEN
        hauteur_invalide = 12
        kicker = ("Roi", "Dame", "10", "9")

        # WHEN / THEN
        with pytest.raises(ValueError):
            Simple(hauteur_invalide, kicker)

    def test_str_repr_simple(self, simple):
        # GIVEN
        s = simple

        # WHEN
        texte_str = str(s)
        texte_repr = repr(s)

        # THEN
        assert "Simple" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
