"""Implémentation de la classe CreditService"""

import logging

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao

logger = logging.getLogger(__name__)


class CreditService:
    """Service de gestion des crédits des joueurs (RAM + DAO)"""

    def crediter(self, joueur: Joueur, montant: int) -> bool:
        """Crédite un joueur dans la RAM et dans la DAO"""

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
            return False

        return True

    def debiter(self, joueur: Joueur, montant: int) -> bool:
        """Débite un joueur dans la RAM et dans la DAO"""

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
            return False
