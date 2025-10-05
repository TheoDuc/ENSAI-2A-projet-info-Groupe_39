"""Implémentation des tests pour la classe QuinteFlush"""

import pytest

from business_object.combinaison.quinte_flush import QuinteFlush


# ---------- Fixtures ----------
@pytest.fixture
def quinte_flush():
    """Fixture qui fournit une QuinteFlush avec hauteur 'As'"""
    return QuinteFlush("As")


@pytest.fixture
def autre_quinte_flush():
    """Fixture pour comparaison"""
    return QuinteFlush("Roi")


# ---------- Classe de tests ----------
class Test_Quinte_Flush:
    """Tests unitaires pour la classe QuinteFlush"""

    def test_creation_quinte_flush(self, quinte_flush):
        # GIVEN
        hauteur = "As"

        # WHEN
        quinte = quinte_flush

        # THEN
        assert quinte.hauteur == "As"
        assert quinte.kicker == ()
        assert QuinteFlush.FORCE() == 8

    def test_comparaison_quinte_flush(self, quinte_flush, autre_quinte_flush):
        # GIVEN
        q_as = quinte_flush
        q_roi = autre_quinte_flush

        # WHEN
        resultat_sup = q_as > q_roi
        resultat_inf = q_roi > q_as
        resultat_egal = q_as == QuinteFlush("As")

        # THEN
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self, quinte_flush, autre_quinte_flush):
        # GIVEN
        q_as = quinte_flush
        q_roi = autre_quinte_flush

        # THEN
        assert q_roi < q_as

    def test_egalite_et_non_egalite(self, quinte_flush, autre_quinte_flush):
        # GIVEN
        q_as = quinte_flush
        q_roi = autre_quinte_flush

        # WHEN / THEN
        assert q_as == QuinteFlush("As")
        assert q_as != q_roi

    def test_creation_quinte_flush_invalide(self):
        # GIVEN
        hauteur_invalide = 12

        # WHEN / THEN
        with pytest.raises(ValueError):
            QuinteFlush(hauteur_invalide)

    def test_str_repr_quinte_flush(self, quinte_flush):
        # GIVEN
        q = quinte_flush

        # WHEN
        texte_str = str(q)
        texte_repr = repr(q)

        # THEN
        assert "QuinteFlush" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
