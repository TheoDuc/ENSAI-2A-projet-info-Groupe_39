"""Tests unitaires pour la classe MancheJoueurDAO"""

import unittest
from unittest.mock import MagicMock, patch
from dao.manche_joueur_dao import MancheJoueurDAO
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur


class TestMancheJoueurDAO(unittest.TestCase):
    """Classe de tests unitaires pour MancheJoueurDAO"""

    def setUp(self):
        self.dao = MancheJoueurDAO()

        # Création de joueurs factices
        self.j1 = Joueur(id_joueur=1, pseudo="Alice", credit=1000, pays="France")
        self.j2 = Joueur(id_joueur=2, pseudo="Bob", credit=800, pays="Belgique")

        # Création d’un objet InfoManche cohérent avec ta classe actuelle
        self.info_manche = InfoManche([self.j1, self.j2])

        # Simule un état de manche : Alice mise, Bob se couche
        self.info_manche.modifier_mise(0, 100)          # Alice mise 100
        self.info_manche.coucher_joueur(1, tour=2)      # Bob s’est couché au tour 2

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_creer_manche_joueur_succes(self, mock_db):
        """Test de la création réussie de participations"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.creer_manche_joueur(1, self.info_manche)

        self.assertTrue(result)
        self.assertEqual(mock_cursor.execute.call_count, 2)

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_creer_manche_joueur_exception(self, mock_db):
        """Test en cas d’exception SQL"""
        mock_db.return_value.connection.__enter__.side_effect = Exception("DB error")

        result = self.dao.creer_manche_joueur(1, self.info_manche)
        self.assertFalse(result)

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_trouver_par_ids(self, mock_db):
        """Test de la récupération des participations"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "id_manche": 1,
                "id_joueur": 1,
                "carte_main_1": "As de pique",
                "carte_main_2": "Roi de coeur",
                "gain": 200,
                "mise": 100,
                "tour_couche": None,
            }
        ]
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.trouver_par_ids(997,997)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id_joueur"], 1)
        mock_cursor.execute.assert_called_once()

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_supprimer_par_id_manche(self, mock_db):
        """Test suppression des participations d’une manche"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 2
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.supprimer_par_id_manche(1)
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_supprimer_participation(self, mock_db):
        """Test suppression d’une seule participation"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.supprimer_participation(1, 2)
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
