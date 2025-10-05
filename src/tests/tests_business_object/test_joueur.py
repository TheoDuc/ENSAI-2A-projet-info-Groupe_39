"""Implémentation des tests pour la classe Joueur"""

import unittest
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


class TestJoueur(unittest.TestCase):
    """Tests unitaires de la classe Joueur"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.joueur = Joueur(1, "Pikachu", 100, True, "France", 20)
        self.table = TableMock()

    def test_initialisation(self):
        """Vérifie l'initialisation correcte"""
        self.assertEqual(self.joueur.pseudo, "Pikachu")
        self.assertEqual(self.joueur.credit, 100)
        self.assertTrue(self.joueur.actif)
        self.assertEqual(self.joueur.pays, "France")

    def test_changer_pseudo(self):
        """Test du changement de pseudo"""
        self.joueur.changer_pseudo("Raichu")
        self.assertEqual(self.joueur.pseudo, "Raichu")

    def test_changer_pays(self):
        """Test du changement de pays"""
        self.joueur.changer_pays("Japon")
        self.assertEqual(self.joueur.pays, "Japon")

    def test_ajouter_credits(self):
        """Test de l'ajout de crédits"""
        self.joueur.ajouter_credits(50)
        self.assertEqual(self.joueur.credit, 150)

    def test_retirer_credits(self):
        """Test du retrait de crédits"""
        nouveau_solde = self.joueur.retirer_credits(30)
        self.assertEqual(nouveau_solde, 70)
        self.assertEqual(self.joueur.credit, 70)

    def test_retirer_credits_trop(self):
        """Test du retrait de crédits excessif"""
        with self.assertRaises(ValueError):
            self.joueur.retirer_credits(999)

    def test_changer_statut(self):
        """Test de l'inversion du statut"""
        self.joueur.changer_statut()
        self.assertFalse(self.joueur.actif)
        self.joueur.changer_statut()
        self.assertTrue(self.joueur.actif)

    def test_rejoindre_table(self):
        """Test que le joueur peut rejoindre une table"""
        self.joueur.rejoindre_table(self.table)
        self.assertIn(self.joueur, self.table.joueurs)
        self.assertEqual(self.joueur.table, self.table)

    def test_rejoindre_table_deja(self):
        """Test que le joueur ne peut pas rejoindre deux tables"""
        self.joueur.rejoindre_table(self.table)
        with self.assertRaises(ValueError):
            self.joueur.rejoindre_table(self.table)

    def test_quitter_table(self):
        """Test du départ d'une table"""
        self.joueur.rejoindre_table(self.table)
        self.joueur.quitter_table()
        self.assertNotIn(self.joueur, self.table.joueurs)
        self.assertIsNone(self.joueur.table)

    def test_as_list(self):
        """Test du retour sous forme de liste"""
        result = self.joueur.as_list()
        self.assertIn(self.joueur.pseudo, result)
        self.assertIn(self.joueur.pays, result)


if __name__ == "__main__":
    unittest.main()
