import pytest

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan


class Test_Brelan:
    """Tests unitaires pour la classe Brelan."""

    def test_brelan_init_succes(self):
        # GIVEN : cartes formant un brelan
        cartes = [pytest.dame_coeur, pytest.dame_trefle, pytest.dame_carreau]

        # WHEN : création du brelan
        brelan = Brelan.from_cartes(cartes)

        # THEN : vérifications
        assert brelan.hauteur == "Dame"
        # tous les kickers sont corrects (ici il n'y en a pas)
        assert brelan.kicker == ()

    def test_brelan_init_hauteur_invalide(self):
        # GIVEN : cartes ne formant pas de brelan
        cartes = [pytest.deux_pique, pytest.trois_coeur, pytest.quatre_trefle]

        # WHEN / THEN : création échoue avec ValueError
        with pytest.raises(ValueError, match="Aucun brelan présent dans les cartes"):
            Brelan.from_cartes(cartes)

    def test_brelan_comparaison(self):
        # GIVEN : deux brelans différents
        brelan_dame = Brelan.from_cartes(
            [pytest.dame_coeur, pytest.dame_trefle, pytest.dame_carreau]
        )
        brelan_roi = Brelan.from_cartes([pytest.roi_coeur, pytest.roi_trefle, pytest.roi_carreau])

        # THEN : vérifications des comparaisons
        assert brelan_roi > brelan_dame
        assert not brelan_dame > brelan_roi
        assert brelan_dame == Brelan.from_cartes(
            [pytest.dame_coeur, pytest.dame_trefle, pytest.dame_carreau]
        )

    def test_brelan_str(self):
        # GIVEN : un brelan
        brelan = Brelan.from_cartes([pytest.dame_coeur, pytest.dame_trefle, pytest.dame_carreau])

        # THEN : représentation lisible
        assert str(brelan) == "Brelan de Dame"

    def test_brelan_repr(self):
        # GIVEN : cartes formant un brelan
        cartes = [pytest.dame_coeur, pytest.dame_trefle, pytest.dame_carreau]
        brelan = Brelan.from_cartes(cartes)

        # THEN : représentation technique
        # construction des kickers (ici aucune carte restante donc tuple vide)
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != "Dame"],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )

        if kicker:
            attendu = f"Brelan(hauteur=Dame, kickers={kicker})"
        else:
            attendu = "Brelan(hauteur=Dame)"

        assert repr(brelan) == attendu
