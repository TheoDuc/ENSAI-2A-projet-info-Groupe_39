import pytest

from business_object.combinaison.quinte import Quinte


class Test_Quinte:
    """Tests unitaires pour la combinaison Quinte avec GIVEN / WHEN / THEN"""

    def test_creation_quinte(self):
        # GIVEN : cartes formant une Quinte (via fixture ou exemple)
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.dix_coeur,
        ]

        # WHEN : création
        q = Quinte.from_cartes(cartes)

        # THEN : vérifications
        assert q.hauteur == "As"
        assert q.kicker == ()
        assert Quinte.FORCE() == 4

    def test_est_present(self):
        # GIVEN : cartes contenant une quinte
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.dix_coeur,
        ]

        # WHEN / THEN : méthode retourne True
        assert Quinte.est_present(cartes)

    def test_est_present_faux(self):
        # GIVEN : cartes ne formant pas une quinte
        cartes = [
            pytest.as_coeur,
            pytest.roi_pique,
            pytest.dame_carreau,
            pytest.valet_trefle,
            pytest.neuf_carreau,
        ]

        # WHEN / THEN : méthode retourne False
        assert not Quinte.est_present(cartes)

    def test_comparaison_quinte(self):
        # GIVEN : deux Quintes différentes
        q_as = Quinte("As")
        q_roi = Quinte("Roi")

        # WHEN : comparaisons
        resultat_sup = q_as > q_roi
        resultat_inf = q_roi > q_as
        resultat_egal = q_as == Quinte("As")

        # THEN : vérifications
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_comparaison_inverse(self):
        # GIVEN : deux Quintes différentes
        q_as = Quinte("As")
        q_roi = Quinte("Roi")

        # THEN : comparaison inverse
        assert q_roi < q_as

    def test_egalite_et_non_egalite(self):
        # GIVEN : deux Quintes différentes
        q_as = Quinte("As")
        q_roi = Quinte("Roi")

        # WHEN / THEN : égalité et différence
        assert q_as == Quinte("As")
        assert q_as != q_roi

    def test_creation_quinte_invalide(self):
        # GIVEN : valeur invalide
        hauteur_invalide = 12

        # WHEN / THEN : création échoue
        with pytest.raises(ValueError):
            Quinte(hauteur_invalide)

    def test_str_repr_quinte(self):
        # GIVEN : Quinte As
        q = Quinte("As")

        # WHEN : récupération des chaînes
        texte_str = str(q)
        texte_repr = repr(q)

        # THEN : vérifications
        assert "Quinte" in texte_str
        assert "As" in texte_str
        assert texte_repr == texte_str
