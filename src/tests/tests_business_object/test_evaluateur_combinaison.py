import pytest

from business_object.combinaison.brelan import Brelan
from business_object.combinaison.carre import Carre
from business_object.combinaison.couleur import Couleur
from business_object.combinaison.double_paire import DoublePaire
from business_object.combinaison.full import Full
from business_object.combinaison.paire import Paire
from business_object.combinaison.quinte import Quinte
from business_object.combinaison.quinte_flush import QuinteFlush
from business_object.combinaison.simple import Simple
from business_object.evaluateur_combinaison import EvaluateurCombinaison


# --- Fixtures pour mains complètes ---
@pytest.fixture
def main_simple():
    return [
        pytest.deux_coeur,
        pytest.cinq_pique,
        pytest.sept_trefle,
        pytest.neuf_carreau,
        pytest.as_pique,
    ]


@pytest.fixture
def main_paire():
    return [
        pytest.dame_coeur,
        pytest.dame_trefle,
        pytest.sept_trefle,
        pytest.neuf_carreau,
        pytest.as_pique,
    ]


@pytest.fixture
def main_double_paire():
    return [
        pytest.roi_coeur,
        pytest.roi_trefle,
        pytest.dame_carreau,
        pytest.dame_pique,
        pytest.as_coeur,
    ]


@pytest.fixture
def main_brelan():
    return [
        pytest.roi_coeur,
        pytest.roi_trefle,
        pytest.roi_pique,
        pytest.neuf_carreau,
        pytest.as_pique,
    ]


@pytest.fixture
def main_quinte():
    return [
        pytest.six_coeur,
        pytest.sept_pique,
        pytest.huit_trefle,
        pytest.neuf_carreau,
        pytest.dix_coeur,
    ]


@pytest.fixture
def main_couleur():
    return [
        pytest.as_coeur,
        pytest.roi_coeur,
        pytest.dame_coeur,
        pytest.valet_coeur,
        pytest.neuf_coeur,
    ]


@pytest.fixture
def main_full():
    return [
        pytest.roi_coeur,
        pytest.roi_trefle,
        pytest.roi_pique,
        pytest.dame_coeur,
        pytest.dame_pique,
    ]


@pytest.fixture
def main_carre():
    return [
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.dame_trefle,
        pytest.dame_carreau,
        pytest.huit_coeur,
    ]


@pytest.fixture
def main_quinte_flush():
    return [
        pytest.six_coeur,
        pytest.sept_coeur,
        pytest.huit_coeur,
        pytest.neuf_coeur,
        pytest.dix_coeur,
    ]


# --- Test paramétré ---
@pytest.mark.parametrize(
    "fixture_name, classe_attendue, hauteur_attendue",
    [
        ("main_simple", Simple, "As"),
        ("main_paire", Paire, "Dame"),
        ("main_double_paire", DoublePaire, "Roi"),
        ("main_brelan", Brelan, "Roi"),
        ("main_quinte", Quinte, "10"),
        ("main_couleur", Couleur, "As"),
        ("main_full", Full, "Roi"),
        ("main_carre", Carre, "Dame"),
        ("main_quinte_flush", QuinteFlush, "10"),
    ],
)
def test_eval_combinaisons(fixture_name, classe_attendue, hauteur_attendue, request):
    cartes = request.getfixturevalue(fixture_name)
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, classe_attendue)
    assert combi.hauteur == hauteur_attendue
