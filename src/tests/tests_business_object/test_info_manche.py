"""Implémentation des tests pour la classe InfoManche"""

import pytest

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main


class TestInfoManche:
    @pytest.fixture
    def joueurs(self):
        return [
            Joueur(1, "Alice", 500, "France"),
            Joueur(2, "Bob", 300, "Canada"),
        ]

    @pytest.fixture
    def mains(self):
        return [
            Main([pytest.as_pique, pytest.roi_coeur]),
            Main([pytest.dix_carreau, pytest.dix_trefle]),
        ]

    # Tests d’initialisation

    def test_infomanche_init_ok(self, joueurs):
        # GIVEN / WHEN
        manche = InfoManche(joueurs)

        # THEN
        assert manche.joueurs == joueurs
        assert manche.statuts == [0, 0]
        assert len(manche.mains) == len(joueurs)
        assert all(m is None for m in manche.mains)
        assert manche.mises == [0, 0]
        assert manche.tour_couche == [10, 10]

    def test_infomanche_init_type_error(self):
        # GIVEN
        mauvais_param = "pas une liste"

        # WHEN / THEN
        with pytest.raises(TypeError, match="Le paramètre 'joueurs' doit être une liste"):
            InfoManche(mauvais_param)

    def test_infomanche_init_joueur_non_instance(self):
        # GIVEN
        mauvais_joueurs = ["Alice", "Bob"]

        # WHEN / THEN
        with pytest.raises(
            TypeError, match="Tous les éléments de 'joueurs' doivent être des instances de Joueur."
        ):
            InfoManche(mauvais_joueurs)

    def test_infomanche_init_vide(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(ValueError, match="0 présents"):
            InfoManche([])

    # Tests assignation_mains

    def test_assignation_mains_ok(self, joueurs, mains):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        manche.assignation_mains(mains)

        # THEN
        assert manche.mains == mains

    def test_assignation_mains_type_error(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        mauvaises_mains = ["pas une main"]

        # WHEN / THEN
        with pytest.raises(TypeError, match="Le paramètre 'mains' doit être une liste de Main."):
            manche.assignation_mains(mauvaises_mains)

    def test_assignation_mains_nombre_incorrect(self, joueurs, mains):
        # GIVEN
        manche = InfoManche(joueurs)
        mauvaises_mains = [mains[0]]  # seulement une main

        # WHEN / THEN
        with pytest.raises(
            ValueError, match="Le nombre de mains doit correspondre au nombre de joueurs."
        ):
            manche.assignation_mains(mauvaises_mains)

    # Tests coucher_joueur

    def test_coucher_joueur_ok(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        indice = 1
        tour = 1

        # WHEN
        manche.coucher_joueur(indice, tour)

        # THEN
        assert manche.tour_couche[indice] == tour
        assert manche.statuts[1] == 3

    # Tests __str__

    def test_str_contenu(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        texte = str(manche)

        # THEN
        assert "InfoManche(" in texte
        assert "joueurs=" in texte
        assert "statuts=" in texte
        assert "mains=" in texte
        assert "mises=" in texte
