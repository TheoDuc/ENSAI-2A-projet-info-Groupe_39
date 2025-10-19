import pytest

from business_object.carte import Carte
from business_object.combinaison.carre import Carre


class Test_Carre:
    """Tests unitaires pour la combinaison 'Carré' avec structure Given / When / Then"""

    def test_carre_init_succes(self):
        # GIVEN : 4 cartes identiques pour former un Carré
        cartes = [pytest.dame_coeur, pytest.dame_pique, pytest.dame_trefle, pytest.dame_carreau]

        # WHEN : création du Carré à partir des cartes
        carre = Carre.from_cartes(cartes)

        # THEN : vérifier la hauteur, la force et les kickers
        assert carre.hauteur == "Dame"
        assert all(k in Carte.VALEURS() for k in carre.kicker)
        assert Carre.FORCE() == 7

    def test_carre_init_hauteur_invalide(self):
        # GIVEN : cartes ne formant pas un Carré
        cartes = [pytest.dame_coeur, pytest.dame_pique, pytest.valet_coeur]

        # WHEN / THEN : la création doit lever une erreur
        with pytest.raises(ValueError):
            Carre.from_cartes(cartes)

    def test_carre_comparaison_gt_lt_eq(self):
        # GIVEN : deux Carrés différents
        carre_dame = Carre.from_cartes(
            [pytest.dame_coeur, pytest.dame_pique, pytest.dame_trefle, pytest.dame_carreau]
        )
        carre_roi = Carre.from_cartes(
            [pytest.roi_coeur, pytest.roi_pique, pytest.roi_trefle, pytest.roi_carreau]
        )

        # WHEN / THEN : comparer les Carrés
        assert carre_roi > carre_dame
        assert not carre_dame > carre_roi
        assert carre_dame == Carre.from_cartes(
            [pytest.dame_coeur, pytest.dame_pique, pytest.dame_trefle, pytest.dame_carreau]
        )

    def test_carre_str(self):
        # GIVEN : Carré de Dames
        carre = Carre.from_cartes(
            [pytest.dame_coeur, pytest.dame_pique, pytest.dame_trefle, pytest.dame_carreau]
        )

        # WHEN / THEN : vérifier la représentation __str__
        assert str(carre) == "Carre de Dame"

    def test_carre_repr(self):
        # GIVEN : Carré de Dames
        carre = Carre.from_cartes(
            [pytest.dame_coeur, pytest.dame_pique, pytest.dame_trefle, pytest.dame_carreau]
        )

        # WHEN / THEN : vérifier la représentation __repr__
        attendu = "Carre([Dame de Coeur, Dame de Pique, Dame de Trêfle, Dame de Carreau])"
        assert repr(carre) == attendu

    def test_carre_est_present(self):
        # GIVEN : une main contenant un Carré
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.huit_coeur,
        ]

        # WHEN / THEN : est_present doit retourner True
        assert Carre.est_present(cartes)

    def test_carre_est_present_faux(self):
        # GIVEN : une main sans Carré
        cartes = [pytest.dame_coeur, pytest.dame_pique, pytest.valet_coeur, pytest.huit_coeur]

        # WHEN / THEN : est_present doit retourner False
        assert not Carre.est_present(cartes)
