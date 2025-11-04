"""Implémentation de la classe Admin"""

import logging

from business_object.joueur import Joueur
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class Admin:
<<<<<<< HEAD
    """Modélisation d'un administrateur dans le système de gestion de jeu"""

    def __init__(self, id_admin: int):
        """
        Instanciation d'un administrateur
=======
    def __init__(self, id_admin: int) -> "Admin":
        """
        Crée un administrateur avec un identifiant unique
>>>>>>> ab91c5a7afb55ea2dcd0e7816a0ba4592e502480

        Paramètres
        ----------
        id_admin : int
<<<<<<< HEAD
            Identifiant unique de l'administrateur
=======
            l'identifiant de l'administrateur
>>>>>>> ab91c5a7afb55ea2dcd0e7816a0ba4592e502480

        Renvois
        -------
        Admin
            Instance de 'Admin'
        """
<<<<<<< HEAD
        self._id_admin = id_admin
=======

        if not isinstance(id_admin, int):
            raise TypeError(f"L'identifiant administrateur doit être un int : {type(id_admin)}")

        if id_admin < 1:
            raise ValueError(
                f"L'identifiant du joueur doit être un entier strictement positif : {id_admin}"
            )

        self.__id_admin = id_admin
>>>>>>> ab91c5a7afb55ea2dcd0e7816a0ba4592e502480

    @property
    def id_admin(self) -> int:
<<<<<<< HEAD
        """
        Retourne l'identifiant de l'administrateur

        Renvois
        -------
        int
            Identifiant unique de l'administrateur
        """
        return self._id_admin

    # --- Méthodes principales ---
    def crediter(self, joueur, credits: int):
        """
        Ajoute des crédits à un joueur

        Paramètres
        ----------
        joueur : Joueur
            Instance du joueur à créditer
        credits : int
            Montant de crédits à ajouter

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            Si le nombre de crédits à ajouter est inférieur ou égal à zéro
        """
        if credits <= 0:
            raise ValueError("Le nombre de crédits à ajouter doit être positif.")
        joueur.credits += credits

    def debiter(self, joueur, credits: int):
=======
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
>>>>>>> ab91c5a7afb55ea2dcd0e7816a0ba4592e502480
        """
        Retire des crédits à un joueur

        Paramètres
        ----------
<<<<<<< HEAD
        joueur : Joueur
            Instance du joueur à débiter
        credits : int
            Montant de crédits à retirer
=======
        credits : int
            nombre de crédits à retirer
>>>>>>> ab91c5a7afb55ea2dcd0e7816a0ba4592e502480

        Renvois
        -------
        None
<<<<<<< HEAD

        Exceptions
        ----------
        ValueError
            Si le nombre de crédits à retirer est inférieur ou égal à zéro
            Si le joueur ne dispose pas d'assez de crédits pour effectuer l'opération
        """
        if credits <= 0:
            raise ValueError("Le nombre de crédits à retirer doit être positif.")
        if joueur.credits < credits:
            raise ValueError(
                "Le nombre de crédits à retirer doit être inférieur ou égal au nombre de crédits du joueur"
            )
        joueur.credits -= credits
=======
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
>>>>>>> ab91c5a7afb55ea2dcd0e7816a0ba4592e502480
