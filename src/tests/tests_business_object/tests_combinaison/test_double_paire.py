"""Tests unitaires pour la classe DoublePaire"""

import pytest

from business_object.combinaison.double_paire import DoublePaire


class Test_Double_Paire:
    """Tests unitaires pour la combinaison Double Paire"""

    def test_creation_doublepaire(self):
        # GIVEN
        hauteur = "Dame"
        kicker = ("Roi", "10")

        # WHEN
        dp = DoublePaire(hauteur, kicker)

        # THEN
        assert dp.hauteur == "Dame"
        assert dp.kicker == ("Roi", "10")
        assert DoublePaire.FORCE() == 2

    def test_comparaison_doublepaire(self):
        # GIVEN
        dp_dame = DoublePaire("Dame", ("Roi", "10"))
        dp_valet = DoublePaire("Valet", ("As", "9"))

        # WHEN
        resultat_sup = dp_dame > dp_valet
        resultat_inf = dp_valet > dp_dame
        resultat_egal = dp_dame == DoublePaire("Dame", ("Roi", "10"))

        # THEN
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self):
        # GIVEN
        dp_dame = DoublePaire("Dame", ("Roi", "10"))
        dp_valet = DoublePaire("Valet", ("As", "9"))

        # THEN
        assert dp_valet < dp_dame

    def test_egalite_et_non_egalite(self):
        # GIVEN
        dp_dame = DoublePaire("Dame", ("Roi", "10"))
        dp_valet = DoublePaire("Valet", ("As", "9"))

        # WHEN / THEN
        assert dp_dame == DoublePaire("Dame", ("Roi", "10"))
        assert dp_dame != dp_valet

    def test_creation_doublepaire_invalide(self):
        # GIVEN
        hauteur_invalide = 12
        kicker = ("Roi", "10")

        # WHEN / THEN
        with pytest.raises(ValueError):
            DoublePaire(hauteur_invalide, kicker)

    def test_str_repr_doublepaire(self):
        # GIVEN
        dp = DoublePaire("Dame", ("Roi", "10"))

        # WHEN
        texte_str = str(dp)
        texte_repr = repr(dp)

        # THEN
        assert "DoublePaire" in texte_str
        assert "Dame" in texte_str
        assert texte_repr == texte_str
