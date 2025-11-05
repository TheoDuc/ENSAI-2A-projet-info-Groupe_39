import unittest
from unittest.mock import patch

from business_object.joueur import Joueur
from service.joueur_service import JoueurService


class TestJoueurService(unittest.TestCase):
    def setUp(self):
        self.service = JoueurService()

    @patch("dao.joueur_dao.JoueurDao.creer")
    def test_creer_joueur_reussi(self, mock_creer):
        mock_creer.return_value = True
        joueur = self.service.creer("Alice", credit=1000, pays="France")
        self.assertIsNotNone(joueur)
        self.assertEqual(joueur.pseudo, "Alice")
        mock_creer.assert_called_once()

    @patch("dao.joueur_dao.JoueurDao.lister_tous")
    def test_lister_tous(self, mock_lister):
        mock_lister.return_value = [
            Joueur(1, "Alice", 1000, "France"),
            Joueur(2, "Bob", 500, "USA"),
        ]
        joueurs = self.service.lister_tous()
        self.assertEqual(len(joueurs), 2)
        self.assertEqual(joueurs[0].pseudo, "Alice")
