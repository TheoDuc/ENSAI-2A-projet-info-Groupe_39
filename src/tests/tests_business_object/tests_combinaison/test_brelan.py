import pytest

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan


class Test_Brelan:
    """Tests unitaires pour la classe Brelan avec GIVEN / WHEN / THEN."""

    def test_brelan_init_succes(self):
        # GIVEN : cartes formant un brelan
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.neuf_carreau,
            pytest.deux_trefle,
        ]

        # WHEN : création du brelan
        brelan = Brelan.from_cartes(cartes)

        # THEN : vérifications
        assert brelan.hauteur == "Dame"
        assert brelan.kicker == ("As", "Roi")

    def test_brelan_init_invalide(self):
        # GIVEN : cartes sans brelan
        cartes = [
            pytest.deux_pique,
            pytest.trois_coeur,
            pytest.quatre_trefle,
            pytest.cinq_coeur,
            pytest.sept_trefle,
            pytest.huit_pique,
            pytest.neuf_coeur,
        ]

        # WHEN / THEN : création échoue avec ValueError
        with pytest.raises(ValueError, match="Aucun brelan présent"):
            Brelan.from_cartes(cartes)

    def test_brelan_comparaison(self):
        # GIVEN : deux brelans différents
        brelan_dame = Brelan.from_cartes(
            [
                pytest.dame_coeur,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.as_pique,
                pytest.roi_coeur,
                pytest.neuf_carreau,
                pytest.deux_trefle,
            ]
        )
        brelan_roi = Brelan.from_cartes(
            [
                pytest.roi_coeur,
                pytest.roi_trefle,
                pytest.roi_carreau,
                pytest.as_coeur,
                pytest.dame_pique,
                pytest.valet_carreau,
                pytest.huit_trefle,
            ]
        )

        # THEN : vérifications des comparaisons
        assert brelan_roi > brelan_dame
        assert not brelan_dame > brelan_roi
        assert brelan_dame == Brelan.from_cartes(
            [
                pytest.dame_coeur,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.as_pique,
                pytest.roi_coeur,
                pytest.neuf_carreau,
                pytest.deux_trefle,
            ]
        )

    def test_brelan_str(self):
        # GIVEN : un brelan
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
        ]

        # WHEN : création du brelan
        brelan = Brelan.from_cartes(cartes)

        # THEN : représentation lisible
        assert str(brelan) == "Brelan de Dame"

    def test_brelan_repr(self):
        # GIVEN : cartes formant un brelan
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
        ]

        # WHEN : création du brelan
        brelan = Brelan.from_cartes(cartes)

        # THEN : représentation technique
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != "Dame"],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )[:2]
        )
        attendu = f"Brelan(hauteur={brelan.hauteur}, kickers={kicker})"
        assert repr(brelan) == attendu
