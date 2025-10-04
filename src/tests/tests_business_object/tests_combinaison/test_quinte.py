"""Implémentation des tests pour la classe Quinte"""

import pytest

from business_object.combinaison.quinte import Quinte

"""Tests unitaires pour la combinaison Quinte"""


# ---------- Fixtures ----------
@pytest.fixture
def quinte():
    """Fixture qui fournit une Quinte de test"""
    return Quinte("As")  # kicker = None pour Quinte


@pytest.fixture
def autre_quinte():
    """Fixture pour comparaison"""
    return Quinte("Roi")


# ---------- Classe de tests ----------
class Test_Quinte:
    """Tests unitaires pour la combinaison Quinte"""

    def test_creation_quinte(self, quinte):
        # GIVEN
        hauteur = "As"

        # WHEN
        q = quinte

        # THEN
        assert q.hauteur == "As"
        assert q.kicker == ()
        assert Quinte.FORCE() == 4

    def test_comparaison_quinte(self, quinte, autre_quinte):
        # GIVEN
        q_as = quinte
        q_roi = autre_quinte

        # WHEN
        resultat_sup = q_as > q_roi
        resultat_inf = q_roi > q_as
        resultat_egal = q_as == Quinte("As")

        # THEN
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self, quinte, autre_quinte):
        # GIVEN
        q_as = quinte
        q_roi = autre_quinte

        # THEN
        assert q_roi < q_as

    def test_egalite_et_non_egalite(self, quinte, autre_quinte):
        # GIVEN
        q_as = quinte
        q_roi = autre_quinte

        # WHEN / THEN
        assert q_as == Quinte("As")
        assert q_as != q_roi

    def test_creation_quinte_invalide(self):
        # GIVEN
        hauteur_invalide = 12

        # WHEN / THEN
        with pytest.raises(ValueError):
            Quinte(hauteur_invalide)

    def test_str_repr_quinte(self, quinte):
        # GIVEN
        q = quinte

        # WHEN
        texte_str = str(q)
        texte_repr = repr(q)

        # THEN
        assert "Quinte" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
