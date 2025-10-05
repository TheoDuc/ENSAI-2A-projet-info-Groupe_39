"""Implémentation des tests pour la classe Full"""

import pytest

from business_object.combinaison.full import Full

"""Tests unitaires pour la combinaison Full"""


# ---------- Fixtures ----------
@pytest.fixture
def full():
    """Fixture qui fournit un Full de test"""
    return Full("Dame", ("Roi", "10"))


@pytest.fixture
def autre_full():
    """Fixture pour comparaison"""
    return Full("Valet", ("As", "9"))


# ---------- Classe de tests ----------
class Test_Full:
    def test_creation_full(self, full):
        # GIVEN
        hauteur = "Dame"
        kicker = ("Roi", "10")

        # WHEN
        f = full

        # THEN
        assert f.hauteur == "Dame"
        assert f.kicker == ("Roi", "10")
        assert Full.FORCE() == 6

    def test_comparaison_full(self, full, autre_full):
        # GIVEN
        f_dame = full
        f_valet = autre_full

        # WHEN
        resultat_sup = f_dame > f_valet
        resultat_inf = f_valet > f_dame
        resultat_egal = f_dame == Full("Dame", ("Roi", "10"))

        # THEN
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self, full, autre_full):
        # GIVEN
        f_dame = full
        f_valet = autre_full

        # THEN
        assert f_valet < f_dame

    def test_egalite_et_non_egalite(self, full, autre_full):
        # GIVEN
        f_dame = full
        f_valet = autre_full

        # WHEN / THEN
        assert f_dame == Full("Dame", ("Roi", "10"))
        assert f_dame != f_valet

    def test_creation_full_invalide(self):
        # GIVEN
        hauteur_invalide = 12
        kicker = ("Roi", "10")

        # WHEN / THEN
        with pytest.raises(ValueError):
            Full(hauteur_invalide, kicker)

    def test_str_repr_full(self, full):
        # GIVEN
        f = full

        # WHEN
        texte_str = str(f)
        texte_repr = repr(f)

        # THEN
        assert "Full" in texte_str
        assert "Dame" in texte_str
        assert texte_repr == texte_str
