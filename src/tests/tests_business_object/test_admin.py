"""Implémentation des tests pour la classe Admin"""

import unittest

from src.business_object.admin import Admin


class Joueur:
    """Classe minimale pour simuler un joueur."""

    def __init__(self, nom: str, credits: int = 0):
        self.nom = nom
        self.credits = credits


class TestAdmin(unittest.TestCase):
    """Tests unitaires pour la classe Admin."""

    def setUp(self):
        """Initialisation avant chaque test."""
        self.admin = Admin(1)
        self.joueur = Joueur("Alice", 100)

    # --- Tests de la propriété id_admin ---
    def test_get_id_admin(self):
        self.assertEqual(self.admin.id_admin, 1)

    def test_set_id_admin_valide(self):
        self.admin.id_admin = 42
        self.assertEqual(self.admin.id_admin, 42)

    def test_set_id_admin_invalide(self):
        with self.assertRaises(TypeError):
            self.admin.id_admin = "abc"

    # --- Tests de crediter() ---
    def test_crediter_positif(self):
        self.admin.crediter(self.joueur, 50)
        self.assertEqual(self.joueur.credits, 150)

    def test_crediter_zero_ou_negatif(self):
        with self.assertRaises(ValueError):
            self.admin.crediter(self.joueur, 0)
        with self.assertRaises(ValueError):
            self.admin.crediter(self.joueur, -10)

    # --- Tests de debiter() ---
    def test_debiter_positif(self):
        self.admin.debiter(self.joueur, 30)
        self.assertEqual(self.joueur.credits, 70)

    def test_debiter_trop(self):
        with self.assertRaises(ValueError):
            self.admin.debiter(self.joueur, 200)

    def test_debiter_zero_ou_negatif(self):
        with self.assertRaises(ValueError):
            self.admin.debiter(self.joueur, 0)
        with self.assertRaises(ValueError):
            self.admin.debiter(self.joueur, -5)


if __name__ == "__main__":
    unittest.main()
