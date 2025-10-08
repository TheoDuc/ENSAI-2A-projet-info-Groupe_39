"""Tests Pytest pour la classe Joueur"""

import pytest
from src.business_object.joueur import Joueur


# Classe factice pour simuler une table
class TableMock:
    """Classe de simulation d'une table pour les tests"""

    def __init__(self):
        self.joueurs = []

    def ajouter_joueur(self, joueur: Joueur):
        self.joueurs.append(joueur)

    def retirer_joueur(self, joueur_ou_indice):
        if isinstance(joueur_ou_indice, Joueur):
            self.joueurs.remove(joueur_ou_indice)
        elif isinstance(joueur_ou_indice, int):
            self.joueurs.pop(joueur_ou_indice)


@pytest.fixture
def joueur():
    """Fixture pour un joueur initialisé."""
    return Joueur(1, "Pikachu", 100, True, "France", 20)


@pytest.fixture
def table():
    """Fixture pour une table simulée."""
    return TableMock()


# --- Tests d'initialisation ---
def test_initialisation(joueur):
    """Vérifie l'initialisation correcte"""
    assert joueur.pseudo == "Pikachu"
    assert joueur.credit == 100
    assert joueur.actif is True
    assert joueur.pays == "France"


# --- Tests des changements d’attributs ---
def test_changer_pseudo(joueur):
    """Test du changement de pseudo"""
    joueur.changer_pseudo("Raichu")
    assert joueur.pseudo == "Raichu"


def test_changer_pays(joueur):
    """Test du changement de pays"""
    joueur.changer_pays("Japon")
    assert joueur.pays == "Japon"


# --- Tests de gestion des crédits ---
def test_ajouter_credits(joueur):
    """Test de l'ajout de crédits"""
    joueur.ajouter_credits(50)
    assert joueur.credit == 150


def test_retirer_credits(joueur):
    """Test du retrait de crédits"""
    nouveau_solde = joueur.retirer_credits(30)
    assert nouveau_solde == 70
    assert joueur.credit == 70


def test_retirer_credits_trop(joueur):
    """Test du retrait de crédits excessif"""
    with pytest.raises(ValueError):
        joueur.retirer_credits(999)


# --- Tests du statut ---
def test_changer_statut(joueur):
    """Test de l'inversion du statut"""
    joueur.changer_statut()
    assert joueur.actif is False
    joueur.changer_statut()
    assert joueur.actif is True


# --- Tests de gestion des tables ---
def test_rejoindre_table(joueur, table):
    """Test que le joueur peut rejoindre une table"""
    joueur.rejoindre_table(table)
    assert joueur in table.joueurs
    assert joueur.table == table


def test_rejoindre_table_deja(joueur, table):
    """Test que le joueur ne peut pas rejoindre deux tables"""
    joueur.rejoindre_table(table)
    with pytest.raises(ValueError):
        joueur.rejoindre_table(table)


def test_quitter_table(joueur, table):
    """Test du départ d'une table"""
    joueur.rejoindre_table(table)
    joueur.quitter_table()
    assert joueur not in table.joueurs
    assert joueur.table is None


# --- Test de conversion en liste ---
def test_as_list(joueur):
    """Test du retour sous forme de liste"""
    result = joueur.as_list()
    assert joueur.pseudo in result
    assert joueur.pays in result
