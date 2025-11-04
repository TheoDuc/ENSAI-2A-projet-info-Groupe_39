import unittest
from unittest.mock import MagicMock, mock_open, patch
from dao.manche_dao import MancheDAO
from business_object.manche import Manche
from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.main import Main


class TestMancheDAO(unittest.TestCase):
    """Classe de tests unitaires pour MancheDAO"""

    def setUp(self):
        # Création de deux "joueurs" mockés pour éviter ValueError
        self.j1 = Joueur(id_joueur=1, pseudo="Alice", credit=1000, pays="France")
        self.j2 = Joueur(id_joueur=2, pseudo="Bob", credit=800, pays="Belgique")

        # Création d’un InfoManche valide avec les mocks
        self.info = InfoManche([self.j1, self.j2])

        # Création d’une manche factice
        self.manche = Manche(self.info, grosse_blind=50)
        self.manche._Manche__pot = 200
        self.manche._Manche__tour = 3
        self.manche._Manche__indice_joueur_actuel = 1

    # -----------------------------------------------------------------
    @patch("dao.manche_dao.os.path.exists", return_value=False)
    def test_charger_donnees_fichier_absent(self, mock_exists):
        """Test que _charger_donnees renvoie un dictionnaire vide si le fichier n’existe pas"""
        result = MancheDAO._charger_donnees()
        self.assertEqual(result, {})
        mock_exists.assert_called_once_with(MancheDAO.FILE_PATH)

    # -----------------------------------------------------------------
    @patch("dao.manche_dao.os.path.exists", return_value=True)
    @patch("dao.manche_dao.open", new_callable=mock_open, read_data='{"1": {"grosse_blind": 100}}')
    def test_charger_donnees_fichier_existant(self, mock_file, mock_exists):
        """Test du chargement correct depuis un fichier JSON existant"""
        result = MancheDAO._charger_donnees()
        self.assertIn("1", result)
        self.assertEqual(result["1"]["grosse_blind"], 100)
        mock_file.assert_called_once_with(MancheDAO.FILE_PATH, "r", encoding="utf-8")

    # -----------------------------------------------------------------
    @patch("dao.manche_dao.open", new_callable=mock_open)
    def test_sauver_donnees(self, mock_file):
        """Test que _sauver_donnees écrit correctement dans le fichier"""
        data = {"1": {"grosse_blind": 50}}
        MancheDAO._sauver_donnees(data)
        mock_file.assert_called_once_with(MancheDAO.FILE_PATH, "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called()  # au moins une écriture doit avoir eu lieu

    # -----------------------------------------------------------------
    def test_manche_to_dict(self):
        """Test de la conversion d’un objet Manche en dictionnaire"""
        result = MancheDAO._manche_to_dict(self.manche)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["grosse_blind"], 50)
        self.assertEqual(result["pot"], 200)
        self.assertEqual(result["tour"], 3)
        self.assertIn("info", result)
        self.assertIn("indice_joueur_actuel", result)

    # -----------------------------------------------------------------
    @patch.object(MancheDAO, "_charger_donnees", return_value={"1": {"grosse_blind": 100}})
    @patch.object(MancheDAO, "_dict_to_manche", return_value="mock_manche")
    def test_lire_manche_succes(self, mock_dict_to_manche, mock_charger):
        """Test de lecture d’une manche existante"""
        result = MancheDAO.lire_manche(1)
        self.assertEqual(result, "mock_manche")
        mock_charger.assert_called_once()
        mock_dict_to_manche.assert_called_once_with({"grosse_blind": 100})

    # -----------------------------------------------------------------
    @patch.object(MancheDAO, "_charger_donnees", return_value={})
    def test_lire_manche_inexistante(self, mock_charger):
        """Test quand la manche n’existe pas"""
        result = MancheDAO.lire_manche(42)
        self.assertIsNone(result)
        mock_charger.assert_called_once()


if __name__ == "__main__":
    unittest.main()
