"""Implémentation des tests pour la classe Admin"""

import pytest

from src.business_object.admin import Admin


class Joueur:
    """Classe minimale pour simuler un joueur."""

    def __init__(self, nom: str, credits: int = 0):
        self.nom = nom
        self.credits = credits


@pytest.fixture
def admin():
    """Fixture pour un admin initialisé."""
    return Admin(1)


@pytest.fixture
def joueur():
    """Fixture pour un joueur initialisé."""
    return Joueur("Alice", 100)


# --- Tests de la propriété id_admin ---
def test_get_id_admin(admin):
    assert admin.id_admin == 1


def test_set_id_admin_valide(admin):
    admin.id_admin = 42
    assert admin.id_admin == 42


def test_set_id_admin_invalide(admin):
    with pytest.raises(TypeError):
        admin.id_admin = "abc"


# --- Tests de crediter() ---
def test_crediter_positif(admin, joueur):
    admin.crediter(joueur, 50)
    assert joueur.credits == 150


def test_crediter_zero_ou_negatif(admin, joueur):
    with pytest.raises(ValueError):
        admin.crediter(joueur, 0)
    with pytest.raises(ValueError):
        admin.crediter(joueur, -10)


# --- Tests de debiter() ---
def test_debiter_positif(admin, joueur):
    admin.debiter(joueur, 30)
    assert joueur.credits == 70


def test_debiter_trop(admin, joueur):
    with pytest.raises(ValueError):
        admin.debiter(joueur, 200)


def test_debiter_zero_ou_negatif(admin, joueur):
    with pytest.raises(ValueError):
        admin.debiter(joueur, 0)
    with pytest.raises(ValueError):
        admin.debiter(joueur, -5)
