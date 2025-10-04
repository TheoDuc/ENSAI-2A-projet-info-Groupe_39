"""Tests unitaires pour la classe Couleur"""

import pytest

from business_object.combinaison.couleur import Couleur


class Test_Couleur:
    def test_creation_couleur(self):
        # GIVEN
        hauteur = "As"

        # WHEN
        c = Couleur(hauteur)

        # THEN
        assert c.hauteur == "As"
        assert c.kicker == ()
        assert Couleur.FORCE() == 5

    def test_comparaison_couleur(self):
        # GIVEN
        as_c = Couleur("As")
        roi_c = Couleur("Roi")

        # WHEN / THEN
        assert as_c > roi_c
        assert roi_c < as_c
        assert as_c == Couleur("As")

    def test_egalite_et_non_egalite(self):
        # GIVEN
        c1 = Couleur("As")
        c2 = Couleur("Roi")

        # WHEN / THEN
        assert c1 == Couleur("As")
        assert c1 != c2

    def test_creation_couleur_invalide(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(ValueError):
            Couleur(12)

    def test_str_repr_couleur(self):
        # GIVEN
        c = Couleur("As")

        # WHEN
        texte_str = str(c)
        texte_repr = repr(c)

        # THEN
        assert "Couleur" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
