import pytest

from business_object.combinaison.simple import Simple


class Test_Simple:
    """Tests unitaires pour la combinaison Simple avec GIVEN / WHEN / THEN"""

    def test_creation_simple(self):
        # GIVEN : un jeu de cartes quelconques
        cartes = [
            pytest.as_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.valet_pique,
            pytest.dix_carreau,
        ]

        # WHEN : création de la Simple
        simple = Simple.from_cartes(cartes)

        # THEN : vérifications
        assert simple.hauteur == "As"  # la carte la plus haute
        assert simple.kicker == ("Roi", "Dame", "Valet", "10")
        assert Simple.FORCE() == 0

    def test_est_present(self):
        # GIVEN : des cartes non vides
        cartes = [pytest.as_coeur, pytest.roi_carreau]

        # WHEN / THEN
        assert Simple.est_present(cartes)

    def test_est_present_faux(self):
        # GIVEN : aucune carte
        cartes = []

        # WHEN / THEN
        assert not Simple.est_present(cartes)

    def test_str_repr_simple(self):
        # GIVEN : création d'une Simple
        cartes = [
            pytest.as_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
        ]
        simple = Simple.from_cartes(cartes)

        # WHEN
        texte_str = str(simple)
        texte_repr = repr(simple)

        # THEN : vérifications
        assert "Simple" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
