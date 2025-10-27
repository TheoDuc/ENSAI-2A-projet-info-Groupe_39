import pytest

from business_object.combinaison.quinte_flush import QuinteFlush


class Test_QuinteFlush:
    """Tests unitaires QuinteFlush avec GIVEN / WHEN / THEN"""

    def test_quinte_flush_creation(self):
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

    def test_quinte_flush_est_present(self):
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

    def test_quinte_flush_est_present_faux(self):
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

    def test_quinte_flush_str_repr(self):
        # GIVEN : une Quinte Flush As
        q = QuinteFlush("As")

        # WHEN : récupération des chaînes
        texte_str = str(q)
        texte_repr = repr(q)

        # THEN : vérifications
        assert texte_str == "Quinte Flush Royale"  # str lisible pour joueur
        assert texte_repr == "QuinteFlush(hauteur='As')"  # repr technique

        # GIVEN : une Quinte Flush autre que As
        q2 = QuinteFlush("Roi")

        # WHEN
        texte_str2 = str(q2)
        texte_repr2 = repr(q2)

        # THEN
        assert texte_str2 == "Quinte Flush"
        assert texte_repr2 == "QuinteFlush(hauteur='Roi')"
