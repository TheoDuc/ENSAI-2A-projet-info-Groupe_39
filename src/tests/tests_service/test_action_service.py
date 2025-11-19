from unittest.mock import Mock, patch

import pytest

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.manche import Manche
from src.service.action_service import ActionService


class Test_Action_Service:
    def test_manche_joueur_normal(self):
        # GIVEN
        joueur1 = Joueur(1, "A", 100, "France")
        joueur2 = Joueur(2, "B", 100, "France")
        info = InfoManche(joueurs=[joueur1, joueur2])
        manche = Manche(info=info, grosse_blind=50)
        table = type("Table", (), {"manche": manche})()
        joueur1._Joueur__table = table

        service = ActionService()
        service.joueur_par_id = lambda _id: joueur1

        # WHEN
        result = service.manche_joueur(joueur1.id_joueur)

        # THEN
        assert result == manche

    def test_manche_joueur_table_sans_manche(self):
        # GIVEN
        joueur1 = Joueur(1, "A", 100, "France")
        table = type("Table", (), {"manche": None})()
        joueur1._Joueur__table = table

        service = ActionService()
        service.joueur_par_id = lambda _id: joueur1

        # WHEN / THEN
        with pytest.raises(ValueError, match="aucune manche n'est en cours"):
            service.manche_joueur(joueur1.id_joueur)

    def test_manche_joueur_pas_dans_manche(self):
        # GIVEN
        joueur1 = Joueur(1, "A", 100, "France")
        joueur2 = Joueur(2, "B", 100, "France")
        joueur3 = Joueur(3, "C", 100, "France")

        info = InfoManche(joueurs=[joueur2, joueur3])  # joueur1 pas dedans
        manche = Manche(info=info, grosse_blind=50)
        table = type("Table", (), {"manche": manche})()
        joueur1._Joueur__table = table

        service = ActionService()
        service.joueur_par_id = lambda _id: joueur1

        # WHEN / THEN
        with pytest.raises(ValueError, match="ne participe pas à la manche"):
            service.manche_joueur(joueur1.id_joueur)

    def test_manche_all_in_pas_tour(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = False

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN / THEN
        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            instance_joueur_service = MockJoueurService.return_value
            instance_joueur_service.trouver_par_id.return_value = joueur

            with patch("src.service.action_service.CreditService") as MockCreditService:
                instance_credit_service = MockCreditService.return_value
                instance_credit_service.debiter = Mock()

                with pytest.raises(Exception, match=f"Ce n'est pas à {joueur.pseudo} de jouer"):
                    service.all_in(id_joueur=1)

    def test_manche_all_in_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0
        manche.info.all_in.return_value = 100

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN
        with (
            patch("src.service.action_service.JoueurService") as MockJoueurService,
            patch("src.service.action_service.CreditService") as MockCreditService,
        ):
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            MockCreditService.return_value.debiter = Mock()

            service.all_in(id_joueur=1)

            # THEN
            MockCreditService.return_value.debiter.assert_called_once_with(joueur, 100)

    def test_checker_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0
        manche.info.statuts = [2]  # statut correct

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN
        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            service.checker(id_joueur=1)

            # THEN
            manche.info.mettre_statut.assert_called_once_with(0, 2)

    def test_checker_pas_tour(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = False

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN / THEN
        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            with pytest.raises(Exception, match=f"Ce n'est pas à {joueur.pseudo} de jouer"):
                service.checker(id_joueur=1)

    def test_checker_statut_incorrect(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0
        manche.info.statuts = [1]  # joueur ne peut pas checker

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN / THEN
        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            with pytest.raises(ValueError, match=f"{joueur.pseudo} ne peut pas checker"):
                service.checker(id_joueur=1)

    def test_se_coucher_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN
        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            service.se_coucher(id_joueur=1)

            # THEN
            manche.info.coucher_joueur.assert_called_once_with(0, 3)

    def test_suivre_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0
        manche.info.suivre.return_value = 50

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        # WHEN
        with (
            patch("src.service.action_service.JoueurService") as MockJoueurService,
            patch("src.service.action_service.CreditService") as MockCreditService,
        ):
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            MockCreditService.return_value.debiter = Mock()

            service.suivre(id_joueur=1)

            # THEN
            manche.info.suivre.assert_called_once_with(0, 0)
            MockCreditService.return_value.debiter.assert_called_once_with(joueur, 50)
