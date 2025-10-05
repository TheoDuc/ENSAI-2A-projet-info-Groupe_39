"""Implémentation des tests pour la classe Paire"""

import pytest

from business_object.combinaison.paire import Paire

"""Tests unitaires pour la combinaison Paire"""


# ---------- Fixtures ----------
@pytest.fixture
def paire():
    """Fixture qui fournit une Paire de test"""
    return Paire("Dame", ("Roi", "10", "8"))


@pytest.fixture
def autre_paire():
    """Fixture pour comparaison"""
    return Paire("Valet", ("As", "9", "7"))


# ---------- Classe de tests ----------
class Test_Paire:
    def test_creation_paire(self, paire):
        # GIVEN
        hauteur = "Dame"
        kicker = ("Roi", "10", "8")

        # WHEN
        p = paire

        # THEN
        assert p.hauteur == "Dame"
        assert p.kicker == ("Roi", "10", "8")
        assert Paire.FORCE() == 1

    def test_comparaison_paire(self, paire, autre_paire):
        # GIVEN
        p_dame = paire
        p_valet = autre_paire

        # WHEN
        resultat_sup = p_dame > p_valet
        resultat_inf = p_valet > p_dame
        resultat_egal = p_dame == Paire("Dame", ("Roi", "10", "8"))

        # THEN
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self, paire, autre_paire):
        # GIVEN
        p_dame = paire
        p_valet = autre_paire

        # THEN
        assert p_valet < p_dame

    def test_egalite_et_non_egalite(self, paire, autre_paire):
        # GIVEN
        p_dame = paire
        p_valet = autre_paire

        # WHEN / THEN
        assert p_dame == Paire("Dame", ("Roi", "10", "8"))
        assert p_dame != p_valet

    def test_creation_paire_invalide(self):
        # GIVEN
        hauteur_invalide = 12
        kicker = ("Roi", "10", "8")

        # WHEN / THEN
        with pytest.raises(ValueError):
            Paire(hauteur_invalide, kicker)

    def test_str_repr_paire(self, paire):
        # GIVEN
        p = paire

        # WHEN
        texte_str = str(p)
        texte_repr = repr(p)

        # THEN
        assert "Paire" in texte_str
        assert "Dame" in texte_str
        assert texte_repr == texte_str
