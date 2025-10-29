import pytest

from business_object.combinaison.quinte_flush import QuinteFlush


class Test_QuinteFlush:
    def test_quinte_flush_creation(self):
        # GIVEN : 7 cartes formant une Quinte Flush As haut
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
            pytest.neuf_coeur,
            pytest.huit_coeur,
        ]

        # WHEN : création via from_cartes
        q = QuinteFlush.from_cartes(cartes)

        # THEN
        assert q.hauteur == "As"
        assert q.kicker is None
        assert QuinteFlush.FORCE() == 8

    def test_quinte_flush_est_present(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
            pytest.neuf_coeur,
            pytest.huit_coeur,
        ]
        assert QuinteFlush.est_present(cartes)

    def test_quinte_flush_est_present_faux(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_carreau,
            pytest.huit_coeur,
            pytest.sept_coeur,
        ]
        assert not QuinteFlush.est_present(cartes)

    def test_quinte_flush_str_repr(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
        ]
        q = QuinteFlush.from_cartes(cartes)

        texte_str = str(q)
        texte_repr = repr(q)

        assert texte_str == "Quinte Flush Royale"
        assert texte_repr == "Quinte Flush(hauteur='As')"

        # GIVEN : Quinte Flush autre que As
        cartes2 = [
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
            pytest.neuf_coeur,
        ]
        q2 = QuinteFlush.from_cartes(cartes2)

        texte_str2 = str(q2)
        texte_repr2 = repr(q2)

        assert texte_str2 == "Quinte Flush"
        assert texte_repr2 == "Quinte Flush(hauteur='Roi')"

    def test_quinte_flush_creation_invalide(self):
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_carreau,
            pytest.huit_coeur,
            pytest.sept_coeur,
        ]
        # Pas de quinte flush complète
        with pytest.raises(ValueError):
            QuinteFlush.from_cartes(cartes)
