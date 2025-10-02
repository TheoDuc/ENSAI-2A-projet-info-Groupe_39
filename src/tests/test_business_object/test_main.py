"""Implémentation des tests pour la classe Main"""

import pytest

from business_object.main import Main
from tests.test_business_object.test_liste_cartes import AbstractListeCartesTest


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

    def test_main_intervertir_cartes_(self):
        # GIVEN
        main = Main([pytest.roi_carreau, pytest.roi_coeur])
        resultat = [pytest.roi_coeur, pytest.roi_carreau]

        # WHEN
        main.intervertir_cartes()

        # THEN
        assert main.cartes == resultat
