"""Implémentation de la classe CreditService"""

import logging

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from service.joueur_service import JoueurService

from utils.log_decorator import log

logger = logging.getLogger(__name__)


class CreditService:
    """Service de gestion des crédits des joueurs"""

    @log
    def crediter(self, joueur: Joueur, montant: int) -> None:
        """
        Crédite un joueur dans la RAM et dans la DAO

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui est débité

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            si le montant à créditer est incorrect

        """

        if montant <= 0:
            raise ValueError("Le montant à créditer doit être positif.")

        ram_modif = False

        try:
            joueur.ajouter_credits(montant)
            ram_modif = True
            JoueurDao().modifier(joueur)
        except Exception as e:
            if ram_modif:
                joueur.retirer_credits(montant)

            logger.error(f"Échec du crédit pour {joueur.pseudo} : {e}")
            raise Exception(f"Échec du crédit pour {joueur.pseudo} : {e}")

    @log
    def debiter(self, id_joueur: int, montant: int) -> None:
        """
        Crédite un joueur dans la RAM et dans la DAO

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui est débité

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            si le montant à créditer est incorrect


        joueur = self.joueur_par_id(id_joueur)
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        if montant <= 0:
            raise ValueError("Le montant à débiter doit être positif.")

        ram_modif = False

        try:
            joueur.retirer_credits(montant)
            ram_modif = True
            JoueurDao().modifier(joueur)
        except Exception as e:
            if ram_modif:
                joueur.ajouter_credits(montant)

            logger.error(f"Échec du débit pour {joueur.pseudo} : {e}")
            raise Exception(f"Échec du crédit pour {joueur.pseudo} : {e}")
