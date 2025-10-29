import pytest

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan


class Test_Brelan:
    """Tests unitaires complets pour la classe Brelan avec GIVEN / WHEN / THEN."""

    def test_brelan_init_succes(self):
        # GIVEN : 7 cartes formant un brelan
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
        assert isinstance(brelan.hauteur, str)
        assert brelan.hauteur == "Dame"
        assert isinstance(brelan.kicker, tuple)
        assert brelan.kicker == ("As", "Roi")

    def test_brelan_init_invalide(self):
        # GIVEN : 7 cartes sans brelan
        cartes = [
            pytest.deux_pique,
            pytest.trois_coeur,
            pytest.quatre_trefle,
            pytest.cinq_coeur,
            pytest.sept_trefle,
            pytest.huit_pique,
            pytest.neuf_coeur,
        ]

        # WHEN / THEN : la création échoue avec ValueError
        with pytest.raises(ValueError, match="Aucun brelan présent"):
            Brelan.from_cartes(cartes)

    def test_brelan_comparaison(self):
        # GIVEN : deux brelans sur 7 cartes
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

        # THEN : comparaisons cohérentes
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
        # GIVEN : brelan sur 7 cartes
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.dix_trefle,
            pytest.neuf_pique,
        ]

        # WHEN : création du brelan
        brelan = Brelan.from_cartes(cartes)

        # THEN : représentation lisible
        assert str(brelan) == "Brelan de Dame"

    def test_brelan_str_as(self):
        # GIVEN : brelan d'As sur 7 cartes
        cartes = [
            pytest.as_coeur,
            pytest.as_trefle,
            pytest.as_carreau,
            pytest.roi_pique,
            pytest.dame_coeur,
            pytest.dix_trefle,
            pytest.huit_pique,
        ]

        # WHEN
        brelan = Brelan.from_cartes(cartes)

        # THEN : représentation spéciale pour As
        assert str(brelan) == "Brelan d'As"

    def test_brelan_repr(self):
        # GIVEN : 7 cartes formant un brelan
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.dix_trefle,
            pytest.neuf_pique,
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

        # La hauteur peut être stockée en str ou tuple selon la version → on l’adapte :
        hauteur_fmt = brelan.hauteur if isinstance(brelan.hauteur, str) else brelan.hauteur[0]
        attendu = f"Brelan(hauteur={hauteur_fmt}, kickers={kicker})"
        assert repr(brelan) == attendu

    def test_brelan_repr_sans_kicker(self):
        # GIVEN : création manuelle sans kicker
        brelan = Brelan("Roi", ())

        # THEN : représentation minimale
        assert repr(brelan) == "Brelan(hauteur=Roi)"

    def test_brelan_force(self):
        # THEN : la force doit être correcte
        assert Brelan.FORCE() == 4
