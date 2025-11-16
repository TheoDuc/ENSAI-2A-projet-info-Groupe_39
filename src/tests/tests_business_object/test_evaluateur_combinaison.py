import pytest

from business_object.combinaison.full import Full
from business_object.combinaison.paire import Paire
from business_object.combinaison.simple import Simple
from business_object.evaluateur_combinaison import EvaluateurCombinaison


def get_kicker_valeurs(kicker):
    """Retourne toujours une liste de valeurs de cartes même si kicker est string ou tuple/list"""
    if kicker is None:
        return []
    if isinstance(kicker, (list, tuple)):
        return list(kicker)
    return [kicker]


def test_eval_full():
    # GIVEN: une liste de cartes formant un Full
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.roi_carreau,
        pytest.dame_trefle,
        pytest.dame_coeur,
    ]

    # WHEN: on évalue la combinaison
    combi = EvaluateurCombinaison.eval(cartes)

    # THEN
    assert isinstance(combi, Full)
    assert combi.hauteur == ["Roi", "Dame"]
    assert combi.kicker is None


def test_eval_paire():
    # GIVEN: une liste de cartes formant une Paire
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.dame_carreau,
        pytest.dix_trefle,
        pytest.neuf_coeur,
    ]

    # WHEN: on évalue la combinaison
    combi = EvaluateurCombinaison.eval(cartes)

    # THEN:
    assert isinstance(combi, Paire)
    assert combi.hauteur == "Roi"
    assert get_kicker_valeurs(combi.kicker) == ["Dame", "10", "9"]


def test_eval_simple():
    # GIVEN:
    cartes = [
        pytest.as_coeur,
        pytest.roi_pique,
        pytest.dame_carreau,
        pytest.dix_trefle,
        pytest.neuf_coeur,
    ]

    # WHEN: on évalue la combinaison
    combi = EvaluateurCombinaison.eval(cartes)

    # THEN
    assert isinstance(combi, Simple)
    assert combi.hauteur == "As"
    assert get_kicker_valeurs(combi.kicker) == ["Roi", "Dame", "10", "9"]
