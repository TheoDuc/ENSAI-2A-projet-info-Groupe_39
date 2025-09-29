"""Implémentation des tests pour la classe Carte"""

import pytest

from business_object.carte import Carte


@pytest.mark.parametrize(
    "valeur, couleur, message_attendu",
    [
        ("1", "Carreau", "Valeur de la carte incorrecte."),
        ("Dame", "Rouge", "Couleur de la carte incorrecte."),
        ("12", "Coeur", "Valeur de la carte incorrecte."),
        (("Trois"), "Trêfle", "Valeur de la carte incorrecte."),
        ("Trêfle", "10", "Valeur de la carte incorrecte."),
        (2, "Coeur", "Valeur de la carte incorrecte."),
    ],
)
def test_carte_init_echec(valeur, couleur, message_attendu):
    with pytest.raises(ValueError, match=message_attendu):
        Carte(valeur, couleur)


@pytest.mark.parametrize(
    "valeur, couleur, resultat_attendu",
    [
        ("2", "Carreau", pytest.deux_carreau),
        ("Valet", "Pique", pytest.valet_pique),
        ("10", "Coeur", pytest.dix_coeur),
        ("Roi", "Trêfle", pytest.roi_trefle),
    ],
)
def test_carte_init_succes(valeur, couleur, resultat_attendu):
    assert Carte(valeur, couleur) == resultat_attendu


@pytest.mark.parametrize(
    "carte, resultat_attendu",
    [
        (pytest.as_carreau, "As de carreau"),
        (pytest.valet_pique, "Valet de pique"),
        (pytest.cinq_coeur, "5 de coeur"),
        (pytest.neuf_trefle, "9 de trêfle"),
    ],
)
def test_carte_str(carte, resultat_attendu):
    assert str(carte) == resultat_attendu


@pytest.mark.parametrize(
    "carte, resultat_attendu",
    [
        (pytest.as_carreau, "Carte(As, Carreau)"),
        (pytest.valet_pique, "Carte(Valet, Pique)"),
        (pytest.cinq_coeur, "Carte(5, Coeur)"),
        (pytest.neuf_trefle, "Carte(9, Trêfle)"),
    ],
)
def test_carte_repr(carte, resultat_attendu):
    assert repr(carte) == resultat_attendu


@pytest.mark.parametrize(
    "carte, other, resultat_attendu",
    [
        (pytest.huit_carreau, pytest.huit_carreau, True),
        (pytest.neuf_trefle, pytest.six_carreau, False),
        (pytest.valet_pique, pytest.valet_coeur, False),
        (pytest.cinq_coeur, pytest.quatre_coeur, False),
        (pytest.as_carreau, "Carte(As de carreau)", False),
        (pytest.valet_pique, "Valet de Pique", False),
        (pytest.cinq_coeur, 5, False),
        (pytest.neuf_trefle, "Trêfle", False),
    ],
)
def test_carte_eq_et_hash(carte, other, resultat_attendu):
    """Vérifie que l'égalité des objets et leur hash sont cohérents"""
    assert (carte == other) is resultat_attendu
    assert (hash(carte) == hash(other)) is resultat_attendu
