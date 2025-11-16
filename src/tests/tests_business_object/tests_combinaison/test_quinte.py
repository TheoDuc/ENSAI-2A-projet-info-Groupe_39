import pytest

from business_object.combinaison.quinte import Quinte


class Test_Quinte:
    """Tests unitaires pour la combinaison Quinte ."""

    def test_quinte_creation(self):
        # GIVEN :
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.dix_coeur,
            pytest.neuf_coeur,
            pytest.huit_carreau,
        ]

        # WHEN : création via from_cartes
        q = Quinte.from_cartes(cartes)

        # THEN : vérifications
        assert q.hauteur == "As"
        assert q.kicker is None
        assert Quinte.FORCE() == 4

    def test_quinte_est_present(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.dix_coeur,
            pytest.neuf_coeur,
            pytest.huit_carreau,
        ]
        assert Quinte.est_present(cartes)

    def test_quinte_est_present_faux(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.neuf_carreau,
            pytest.sept_coeur,
            pytest.six_coeur,
        ]
        assert not Quinte.est_present(cartes)

    def test_quinte_comparaison(self):
        cartes1 = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.dix_coeur,
        ]
        cartes2 = [
            pytest.roi_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.dix_trefle,
            pytest.neuf_coeur,
        ]
        q_as = Quinte.from_cartes(cartes1)
        q_roi = Quinte.from_cartes(cartes2)

        # Comparaisons
        assert q_as > q_roi
        assert q_roi < q_as
        assert q_as == Quinte.from_cartes(cartes1)
        assert q_as != q_roi

    def test_quinte_creation_invalide(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.neuf_coeur,
            pytest.huit_coeur,
            pytest.sept_coeur,
        ]
        # Il n’y a pas de quinte complète de 5 cartes consécutives
        with pytest.raises(ValueError):
            Quinte.from_cartes(cartes)

    def test_quinte_str_repr(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.dix_coeur,
        ]
        q = Quinte.from_cartes(cartes)

        texte_str = str(q)
        texte_repr = repr(q)

        assert texte_str == "Quinte"
        assert texte_repr == "Quinte(hauteur='As')"
