import pytest

from business_object.carte import Carte
from business_object.combinaison.couleur import Couleur


class Test_Couleur:
    """Tests unitaires pour la combinaison Couleur avec GIVEN / WHEN / THEN et conftest.py"""

    def test_couleur_init_succes(self):
        # GIVEN : hauteur = As
        hauteur = "As"

        # WHEN : création d'une Couleur
        couleur = Couleur(hauteur)

        # THEN : vérifications
        assert couleur.hauteur == "As"
        assert all(k in Carte.VALEURS() for k in couleur.kicker)
        assert Couleur.FORCE() == 5

    def test_couleur_comparaison(self):
        # GIVEN : deux couleurs de hauteurs différentes
        as_couleur = Couleur("As")
        roi_couleur = Couleur("Roi")

        # THEN : comparaisons
        assert as_couleur > roi_couleur
        assert roi_couleur < as_couleur
        assert as_couleur == Couleur("As")

    def test_couleur_creation_invalide(self):
        # GIVEN / WHEN / THEN : création invalide doit lever ValueError
        with pytest.raises(ValueError):
            Couleur(12)

    def test_couleur_str_repr(self):
        # GIVEN : cartes formant une Couleur (utilisation de conftest.py)
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
        ]
        couleur = Couleur.from_cartes(cartes)

        # WHEN : récupération des chaînes
        texte_str = str(couleur)
        texte_repr = repr(couleur)

        # THEN : vérifications
        assert texte_str == "Nous avons des couleurs"
        assert texte_repr.startswith("Couleur(")

    def test_couleur_est_present(self):
        # GIVEN : 5 cartes de même couleur (conftest)
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
            pytest.huit_coeur,
        ]

        # THEN
        assert Couleur.est_present(cartes)

    def test_couleur_est_present_faux(self):
        # GIVEN : seulement 4 cartes de même couleur
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
        ]

        # THEN
        assert not Couleur.est_present(cartes)
