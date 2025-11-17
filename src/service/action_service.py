"""Implémentation de la classe ActionService"""

from business_object.manche import Manche
from service.credit_service import CreditService
from service.joueur_service import JoueurService


class ActionService:
    """Actions possibles d'un joueur dans une Manche"""

    def manche_joueur(self, id_joueur: int) -> Manche:
        """
        Fonction qui renvoie la manche dans laquelle le joueur joue

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur

        Renvois
        -------
        Manche
            la manche dans laquelle est le jouur

        Exceptions
        ----------
        ValueError
            si le joueur n'est pas à une table
            si aucune manche n'est en cours sur la table du joueur
            si le joueur n'est pas dans la manche en cours
        """

        joueur = self.joueur_par_id(id_joueur)

        if joueur.table is None:
            raise ValueError(
                f"Le joueur {joueur.pseudo} n'est à aucune table et ne peut effectuer d'action"
            )

        if joueur.table.manche is None:
            raise ValueError(
                f"Le joueur {joueur.pseudo} est dans une table mais aucune manche n'est en cours"
            )

        if joueur not in joueur.table.manche.info.joueurs:
            raise ValueError(f"Le joueur {joueur.pseudo} ne participe pas à la manche en cours")

        return joueur.table.manche

    def all_in(self, id_joueur: int) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par le all-in d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        montant = manche.info.all_in(indice_joueur)
        CreditService().debiter(joueur, montant)

    def checker(self, id_joueur: int) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par l'action de checker d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        if not manche.info.statuts[indice_joueur] == 2:
            raise ValueError(
                f"{joueur.pseudo} ne peut pas checker car il est en retard sur les mises"
            )

        manche.info.mettre_statut(indice_joueur, 2)

    def se_coucher(self, id_joueur: int) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par l'action de se coucher d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        manche.info.coucher_joueur(indice_joueur, 3)

    def suivre(self, id_joueur: int, relance: int = 0) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par le suivi d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        montant = manche.info.suivre(indice_joueur, relance)
        CreditService().debiter(joueur, montant)
