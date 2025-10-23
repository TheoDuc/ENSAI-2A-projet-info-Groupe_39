"""Tests unitaires pour la combinaison Full avec structure GIVEN / WHEN / THEN"""

import pytest

from business_object.combinaison.full import Full


class Test_Full:
    def test_full_init_succes(self):
        # GIVEN : cartes formant un Full (brelan + paire)
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,
            pytest.roi_coeur,
            pytest.roi_carreau,
        ]

        # WHEN : création du Full
        full = Full.from_cartes(cartes)

        # THEN : vérifications
        assert full.hauteur == "Dame"  # brelan
        assert full.paire == "Roi"  # paire
        assert Full.FORCE() == 6

    def test_full_init_invalide(self):
        # GIVEN : cartes ne formant pas un Full
        cartes = [pytest.dame_coeur, pytest.dame_pique, pytest.roi_coeur, pytest.valet_coeur]

        # WHEN / THEN : création échoue
        with pytest.raises(ValueError):
            Full.from_cartes(cartes)

    def test_full_est_present(self):
        # GIVEN : cartes contenant un Full
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,
            pytest.roi_coeur,
            pytest.roi_carreau,
        ]

        # WHEN / THEN : méthode est_present retourne True
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

        # WHEN / THEN : méthode est_present retourne False
        assert not Full.est_present(cartes)

    def test_full_comparaison(self):
        # GIVEN : deux Full de hauteurs différentes
        full_dame = Full("Dame", None)
        full_dame._paire = "Roi"

        full_valet = Full("Valet", None)
        full_valet._paire = "As"

        # GIVEN pour comparaison d’égalité
        full_dame2 = Full("Dame", None)
        full_dame2._paire = "Roi"

        # WHEN
        resultat_sup = full_dame > full_valet
        resultat_inf = full_valet > full_dame
        resultat_egal = full_dame == full_dame2

        # THEN : vérifications
        assert resultat_sup
        assert not resultat_inf
        assert resultat_egal

    def test_full_str_repr(self):
        # GIVEN : Full
        full = Full("Dame", None)
        full._paire = "Roi"

        # WHEN
        texte_str = str(full)
        texte_repr = repr(full)

        # THEN : vérifications
        assert "Full" in texte_str
        assert "Dame" in texte_str
        assert "Roi" in texte_str
        assert texte_repr == texte_str
