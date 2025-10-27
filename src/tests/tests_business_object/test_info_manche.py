"""Implémentation des tests pour la classe InfoManche"""

import pytest

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main


class TestInfoManche:
    @pytest.fixture
    def joueurs(self):
        return [
            Joueur(1, "Alice", 500, True, "France", 25),
            Joueur(2, "Bob", 300, True, "Canada", 30),
        ]

    @pytest.fixture
    def mains(self):
        return [
            Main([pytest.as_pique, pytest.roi_coeur]),
            Main([pytest.dix_carreau, pytest.dix_trefle]),
        ]

    # ---------------------------------------------------------------------- #
    # Tests d’initialisation
    # ---------------------------------------------------------------------- #
    def test_infomanche_init_ok(self, joueurs):
        # GIVEN / WHEN
        manche = InfoManche(joueurs)

        # THEN
        assert manche.joueurs == joueurs
        assert len(manche.mains) == len(joueurs)
        assert all(m is None for m in manche.mains)
        assert manche.mises == [0, 0]
        assert manche.tour_couche == [None, None]

    def test_infomanche_init_type_error(self):
        # GIVEN
        mauvais_param = "pas une liste"
        message_attendu = "Le paramètre 'joueurs' doit être une liste"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
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
        # GIVEN
        joueurs = []

        # WHEN / THEN
        with pytest.raises(
            ValueError, match=f"Au moins deux joueurs doivent être présents : {len(joueurs)}"
        ):
            InfoManche(joueurs)

    # ---------------------------------------------------------------------- #
    # Tests assignation_mains
    # ---------------------------------------------------------------------- #
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

    # ---------------------------------------------------------------------- #
    # Tests miser
    # ---------------------------------------------------------------------- #
    def test_miser_ok(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        indice = 0
        montant = 100

        # WHEN
        manche.miser(indice, montant)

        # THEN
        assert manche.mises[indice] == montant

    def test_miser_type_indice(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        message_attendu = "indice_joueur doit être un entier"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            manche.miser("0", 100)

    def test_miser_montant_negatif(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        message_attendu = "Le montant doit être un entier strictement positif"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            manche.miser(0, -50)

    # ---------------------------------------------------------------------- #
    # Tests coucher_joueur
    # ---------------------------------------------------------------------- #
    def test_coucher_joueur_ok(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        indice = 1

        # WHEN
        manche.coucher_joueur(indice)

        # THEN
        assert manche.tour_couche[indice] is True
        assert manche.tour_couche[0] is None

    # ---------------------------------------------------------------------- #
    # Tests __str__
    # ---------------------------------------------------------------------- #
    def test_str_contenu(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        texte = str(manche)

        # THEN
        assert "InfoManche(" in texte
        assert "joueurs=" in texte
        assert "mains=" in texte
        assert "mises=" in texte
