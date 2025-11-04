import pytest

from business_object.combinaison.full import Full


class Test_Full:
    """Tests unitaires complets pour la combinaison Full avec 7 cartes."""

    def test_full_init_succes(self):
        # GIVEN : 7 cartes formant un Full (brelan + paire)
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,  # brelan
            pytest.roi_coeur,
            pytest.roi_carreau,  # paire
            pytest.as_coeur,
            pytest.valet_coeur,  # cartes restantes
        ]

        # WHEN : création de la combinaison
        full = Full.from_cartes(cartes)

        # THEN : vérification de la hauteur et kicker
        assert full.hauteur == ["Dame", "Roi"]
        assert full.kicker is None
        assert Full.FORCE() == 6

    def test_full_init_invalide(self):
        # GIVEN : cartes ne formant pas un Full
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.roi_coeur,
            pytest.as_coeur,
        ]

        # WHEN / THEN : doit lever ValueError
        with pytest.raises(ValueError):
            Full.from_cartes(cartes)

    def test_full_est_present(self):
        # GIVEN : cartes contenant un Full
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,  # brelan
            pytest.roi_coeur,
            pytest.roi_carreau,  # paire
        ]
        assert Full.est_present(cartes)

    def test_full_est_present_faux(self):
        # GIVEN : cartes sans Full
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.roi_coeur,
            pytest.as_coeur,
        ]
        assert not Full.est_present(cartes)

    def test_full_comparaison(self):
        # GIVEN : deux Full différents
        cartes_1 = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,
            pytest.roi_coeur,
            pytest.roi_carreau,
        ]
        cartes_2 = [
            pytest.valet_coeur,
            pytest.valet_pique,
            pytest.valet_trefle,
            pytest.as_coeur,
            pytest.as_pique,
        ]

        full1 = Full.from_cartes(cartes_1)  # Full Dame-Roi
        full2 = Full.from_cartes(cartes_2)  # Full Valet-As

        # THEN : comparaison par brelan puis paire
        assert full1 > full2
        assert full2 < full1
        assert full1 == Full.from_cartes(cartes_1)

    def test_full_str_repr(self):
        # GIVEN : 7 cartes formant un Full
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,
            pytest.roi_coeur,
            pytest.roi_carreau,
        ]

        full = Full.from_cartes(cartes)

        # THEN : vérification des représentations
        assert str(full) == "Full Dame Roi"
        assert repr(full) == "Full(hauteur=['Dame', 'Roi'], kicker=None)"
