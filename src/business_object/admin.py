"""Implémentation de la classe Admin"""

import logging

from business_object.joueur import Joueur
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class Admin:
    def __init__(self, id_admin: int) -> "Admin":
        """
        Crée un administrateur avec un identifiant unique

        Paramètres
        ----------
        id_admin : int
            l'identifiant de l'administrateur

        Renvois
        -------
        Admin
            Instance de 'Admin'
        """

        if not isinstance(id_admin, int):
            raise TypeError(f"L'identifiant administrateur doit être un int : {type(id_admin)}")

        if id_admin < 1:
            raise ValueError(
                f"L'identifiant du joueur doit être un entier strictement positif : {id_admin}"
            )

        self.__id_admin = id_admin

    @property
    def id_admin(self) -> int:
        """Retourne l'identifiant de l'administrateur."""
        return self.__id_admin

    @log
    def crediter(self, joueur: Joueur, credits: int) -> None:
        """
        Ajoute des crédits à un joueur

        Paramètres
        ----------
        credits : int
            nombre de crédits à ajouter

        Renvois
        -------
        None
        """

        logger.info(f"L'admin crédite {credits} à {joueur.pseudo}")
        joueur.ajouter_credits(credits)

    @log
    def debiter(self, joueur: Joueur, credits: int) -> None:
        """
        Retire des crédits à un joueur

        Paramètres
        ----------
        credits : int
            nombre de crédits à retirer

        Renvois
        -------
        None
        """

        logger.info(f"L'admin débite {credits} à {joueur.pseudo}")
        joueur.retirer_credits(credits)

    @log
    def set_credits(self, joueur: Joueur, credits: int) -> None:
        """
        Met les crédits d'un joueur à un certain niveau

        Paramètres
        ----------
        credits : int
            Nouvelle quantité de crédits du joueur

        Renvois
        -------
        None
        """

        logger.info(f"L'admin met les crédits de {joueur.pseudo} à {credits}")
        joueur.retirer_credits(joueur.credit)
        joueur.ajouter_credits(credits)
