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
    def test_trouver_par_id_manche(self, mock_db):
        """Test de la récupération des participations"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "id_manche_joueur": 1,
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

        result = self.dao.trouver_par_id_manche(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id_joueur"], 1)
        mock_cursor.execute.assert_called_once()

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_modifier_manche_joueur(self, mock_db):
        """Test de mise à jour d’un joueur"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.modifier_manche_joueur(
            1, 1, statut="couché", mise=200, tour_couche=3
        )

        self.assertTrue(result)
        self.assertIn("UPDATE manche_joueur", mock_cursor.execute.call_args[0][0])

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_modifier_manche_joueur_aucune_modif(self, mock_db):
        """Test sans champ à modifier"""
        result = self.dao.modifier_manche_joueur(1, 1)
        self.assertFalse(result)

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

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_ajouter_credit_succes(self, mock_db):
        """Test ajout de crédit réussi"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Simule une mise à jour réussie
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.ajouter_credit(self.j1, 200)

        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        self.assertIn("UPDATE joueur", mock_cursor.execute.call_args[0][0])

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_ajouter_credit_aucun_joueur(self, mock_db):
        """Test ajout de crédit échoué (aucun joueur trouvé)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Aucun joueur mis à jour
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.ajouter_credit(self.j1, 200)

        self.assertFalse(result)
        mock_cursor.execute.assert_called_once()

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_ajouter_credit_exception(self, mock_db):
        """Test ajout de crédit avec exception SQL"""
        mock_db.return_value.connection.__enter__.side_effect = Exception("DB error")

        result = self.dao.ajouter_credit(self.j1, 200)
        self.assertFalse(result)

    # -----------------------------------------------------------------
    def test_ajouter_credit_montant_invalide(self):
        """Test ajout de crédit avec montant négatif ou nul"""
        with self.assertRaises(ValueError):
            self.dao.ajouter_credit(self.j1, 0)
        with self.assertRaises(ValueError):
            self.dao.ajouter_credit(self.j1, -50)

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_retirer_credit_succes(self, mock_db):
        """Test retrait de crédit réussi"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.retirer_credit(self.j1, 150)

        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        self.assertIn("UPDATE joueur", mock_cursor.execute.call_args[0][0])
        self.assertIn("credit -", mock_cursor.execute.call_args[0][0])

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_retirer_credit_fonds_insuffisants(self, mock_db):
        """Test retrait échoué (fonds insuffisants ou joueur introuvable)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Aucune ligne modifiée
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.dao.retirer_credit(self.j1, 5000)  # Trop grand montant
        self.assertFalse(result)
        mock_cursor.execute.assert_called_once()

    # -----------------------------------------------------------------
    @patch("dao.manche_joueur_dao.DBConnection")
    def test_retirer_credit_exception(self, mock_db):
        """Test retrait de crédit avec exception SQL"""
        mock_db.return_value.connection.__enter__.side_effect = Exception("DB crash")

        result = self.dao.retirer_credit(self.j1, 200)
        self.assertFalse(result)

    # -----------------------------------------------------------------
    def test_retirer_credit_montant_invalide(self):
        """Test retrait de crédit avec montant négatif ou nul"""
        with self.assertRaises(ValueError):
            self.dao.retirer_credit(self.j1, 0)
        with self.assertRaises(ValueError):
            self.dao.retirer_credit(self.j1, -100)


if __name__ == "__main__":
    unittest.main()
