"""Tests pour la classe MancheDAO."""

import os
import json
import pytest

from business_object.manche import Manche
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from dao.manche_dao import MancheDAO


@pytest.fixture(autouse=True)
def cleanup_json():
    """Supprime le fichier JSON avant et après chaque test."""
    if os.path.exists(MancheDAO.FILE_PATH):
        os.remove(MancheDAO.FILE_PATH)
    yield
    if os.path.exists(MancheDAO.FILE_PATH):
        os.remove(MancheDAO.FILE_PATH)


def test_creer_et_lire_manche():
    """Vérifie la création et la lecture d'une manche."""
    # GIVEN : création d'une manche avec des joueurs valides
    joueurs = [
        Joueur(1, "Alice", credit=1000, actif=True, pays="FR", age=30),
        Joueur(2, "Bob", credit=1200, actif=True, pays="CA", age=28),
    ]
    # 🩵 Correction clé : appel explicite en mot-clé
    info = InfoManche(joueurs=joueurs)

    manche = Manche(info, grosse_blind=100)
    manche.ajouter_au_pot(250)

    # WHEN : sauvegarde de la manche
    id_manche = MancheDAO.creer_manche(manche)

    # THEN : vérification du fichier et de la lecture
    assert isinstance(id_manche, int)
    assert os.path.exists(MancheDAO.FILE_PATH)

    with open(MancheDAO.FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert str(id_manche) in data

    manche_lue = MancheDAO.lire_manche(id_manche)
    assert isinstance(manche_lue, Manche)
    assert manche_lue.grosse_blind == 100
    assert manche_lue.pot == 250
    assert manche_lue.tour == 0


def test_lire_manche_inexistante():
    """Vérifie qu'une manche inexistante retourne None."""
    # GIVEN / WHEN
    manche = MancheDAO.lire_manche(999)

    # THEN
    assert manche is None
