import pytest

from business_object.combinaison.brelan import Brelan


class Test_Brelan:
    """Tests unitaires pour la classe Brelan avec GIVEN / WHEN / THEN"""

    def test_brelan_init_succes(self):
        # GIVEN : cartes formant un Brelan
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,  # le Brelan
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.neuf_carreau,
        ]

        # WHEN : création du Brelan
        brelan = Brelan.from_cartes(cartes)

        # THEN : vérifier hauteur et kickers
        assert brelan.hauteur == "Dame"
        assert brelan.kicker == ("As", "Roi")
        assert Brelan.FORCE() == 4

    def test_brelan_init_erreur(self):
        # GIVEN : cartes sans Brelan
        cartes = [
            pytest.deux_coeur,
            pytest.trois_coeur,
            pytest.quatre_trefle,
            pytest.cinq_coeur,
            pytest.sept_trefle,
        ]

        # WHEN / THEN : création échoue
        with pytest.raises(ValueError, match="Aucun brelan présent"):
            Brelan.from_cartes(cartes)

    def test_brelan_comparaison(self):
        # GIVEN : deux Brelans différents
        brelan_dame = Brelan.from_cartes(
            [
                pytest.dame_coeur,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.as_pique,
                pytest.roi_coeur,
            ]
        )
        brelan_roi = Brelan.from_cartes(
            [
                pytest.roi_coeur,
                pytest.roi_trefle,
                pytest.roi_carreau,
                pytest.as_coeur,
                pytest.valet_pique,
            ]
        )

        # THEN : comparaison fonctionne
        assert brelan_roi > brelan_dame
        assert not brelan_dame > brelan_roi
        assert brelan_dame == Brelan.from_cartes(
            [
                pytest.dame_coeur,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.as_pique,
                pytest.roi_coeur,
            ]
        )

    def test_brelan_str_repr(self):
        # GIVEN : Brelan de Dame
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
        ]
        brelan = Brelan.from_cartes(cartes)

        # THEN : __str__ et __repr__
        assert str(brelan) == "Brelan de Dame"
        kicker = ("As", "Roi")
        assert repr(brelan) == f"Brelan(hauteur={brelan.hauteur}, kickers={kicker})"

    def test_brelan_est_present(self):
        # GIVEN : cartes avec et sans Brelan
        cartes_ok = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
        ]
        cartes_non = [
            pytest.deux_coeur,
            pytest.trois_trefle,
            pytest.quatre_carreau,
            pytest.cinq_coeur,
            pytest.sept_trefle,
        ]

        # THEN : est_present correct
        assert Brelan.est_present(cartes_ok)
        assert not Brelan.est_present(cartes_non)
