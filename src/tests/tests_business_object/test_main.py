"""Implémentation des tests pour la classe Main"""

import pytest

from business_object.main import Main
from tests.tests_business_object.test_liste_cartes import AbstractListeCartesTest


class TestMain(AbstractListeCartesTest):
    @pytest.fixture
    def liste_cartes(self):
        return Main([pytest.as_pique, pytest.dix_coeur])

    @pytest.fixture
    def cls(self):
        return Main

    def test_main_init_defaut(self):
        # GIVEN
        resultat = []

        # WHEN
        main = Main()

        # THEN
        assert main.cartes == resultat

    def test_main_init_trop_grand(self):
        # GIVEN
        cartes = [pytest.as_pique, pytest.dix_coeur, pytest.as_pique]
        message_attendu = f"Le nombre de cartes dans la main est trop grand : {len(cartes)}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Main(cartes)

    def test_main_intervertir_cartes_(self):
        # GIVEN
        main = Main([pytest.roi_carreau, pytest.roi_coeur])
        resultat = [pytest.roi_coeur, pytest.roi_carreau]

        # WHEN
        main.intervertir_cartes()

        # THEN
        assert main.cartes == resultat

    def test_main_ajouter_carte_succes(self):
        # GIVEN
        carte = pytest.cinq_trefle
        main = Main([pytest.as_pique])
        resultat = [pytest.as_pique, pytest.cinq_trefle]

        # WHEN
        main.ajouter_carte(carte)

        # THEN
        assert main.cartes == resultat

    def test_main_ajouter_cartes_echec(self):
        # GIVEN
        main = Main([pytest.as_pique, pytest.dix_coeur])
        carte = pytest.as_coeur
        message_attendu = f"Le nombre de cartes dans la main est trop grand : {len(main.cartes)+1}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            main.ajouter_carte(carte)
