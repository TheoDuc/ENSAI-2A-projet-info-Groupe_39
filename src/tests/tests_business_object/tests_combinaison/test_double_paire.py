import pytest

from business_object.carte import Carte
from business_object.combinaison.double_paire import DoublePaire


class Test_DoublePaire:
    """Tests unitaires pour la combinaison DoublePaire avec structure GIVEN / WHEN / THEN"""

    def test_double_paire_init_succes(self):
        # GIVEN : cartes formant une Double Paire
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.valet_coeur,
        ]

        # WHEN : création de la Double Paire
        double_paire = DoublePaire.from_cartes(cartes)

        # THEN : vérifications
        assert double_paire.hauteur == "Roi"  # la paire la plus haute
        assert double_paire.kicker[0] == "Dame"  # la deuxième paire
        assert all(k in Carte.VALEURS() for k in double_paire.kicker)

    def test_double_paire_init_invalide(self):
        # GIVEN : cartes sans Double Paire
        cartes = [pytest.dame_coeur, pytest.dame_pique, pytest.valet_coeur]

        # WHEN / THEN : création échoue
        with pytest.raises(ValueError):
            DoublePaire.from_cartes(cartes)

    def test_double_paire_est_present(self):
        # GIVEN : cartes contenant une Double Paire
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.valet_coeur,
        ]

        # WHEN / THEN : méthode est_present retourne True
        assert DoublePaire.est_present(cartes)

    def test_double_paire_est_present_faux(self):
        # GIVEN : cartes sans Double Paire
        cartes = [pytest.dame_coeur, pytest.dame_pique, pytest.valet_coeur]

        # WHEN / THEN : méthode est_present retourne False
        assert not DoublePaire.est_present(cartes)

    def test_double_paire_str_repr(self):
        # GIVEN : cartes formant une Double Paire
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.valet_coeur,
        ]

        # WHEN : création de la Double Paire
        double_paire = DoublePaire.from_cartes(cartes)

        # THEN : vérification des représentations
        assert str(double_paire) == "Double Paire Roi et Dame"
        assert (
            repr(double_paire)
            == f"DoublePaire(hauteur=Roi, kicker=({double_paire.kicker[0]}, {double_paire.kicker[1]}))"
        )
