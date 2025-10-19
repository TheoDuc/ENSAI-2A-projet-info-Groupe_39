import pytest

from business_object.combinaison.quinte_flush import QuinteFlush


class Test_QuinteFlush:
    """Tests unitaires QuinteFlush avec GIVEN / WHEN / THEN"""

    def test_creation_quinte_flush(self):
        # GIVEN : cartes formant une Quinte Flush
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
        ]

        # WHEN : création
        q = QuinteFlush.from_cartes(cartes)

        # THEN
        assert q.hauteur == "As"
        assert q.kicker == ()
        assert QuinteFlush.FORCE() == 8

    def test_est_present(self):
        # GIVEN : cartes avec quinte flush
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
        ]

        # WHEN / THEN
        assert QuinteFlush.est_present(cartes)

    def test_est_present_faux(self):
        # GIVEN : cartes sans quinte flush
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_carreau,
        ]

        # WHEN / THEN
        assert not QuinteFlush.est_present(cartes)

    def test_str_repr_quinte_flush(self):
        # GIVEN : une Quinte Flush
        q = QuinteFlush("As")

        # WHEN : récupération des chaînes
        texte_str = str(q)
        texte_repr = repr(q)

        # THEN : vérifications
        assert "Quinte Flush" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
