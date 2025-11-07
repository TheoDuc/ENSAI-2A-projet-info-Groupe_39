"""Implémentation de la classe Table"""

import logging

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.manche import Manche
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class Table:
    """Modélisation d'une table de jeu"""

    def __init__(
        self,
        joueur_max: int,
        grosse_blind: int,
        numero_table: int = 0,
        mode_jeu: int = 1,
        joueurs: list = [],
        manche: Manche = None
    ):
        """
        Instanciation de la table de jeu

        Paramètres
        ----------
        joueur_max : int
            nombre de joueur maximum sur la table
        grosse_blind : int
            valeur de la grosse blind
        mode_jeu : int
            code du mode de jeu de la tabl
            1 : Texas Hold'em (cash game)
        joueurs : list[Joueur]
            liste des joueurs present sur la table
        manche : Manche
            Manche en cours sur la table

        Renvois
        -------
        Table
            Instance de 'Table'

        """
        self.__joueur_max = joueur_max
        self.__grosse_blind = grosse_blind
        self.__numero_table = numero_table
        self.__mode_jeu = mode_jeu
        self.__joueurs = joueurs
        self.__manche = Manche
        self.dealer_index = 0  # DE la part de cheik pour rotation dealer

    # creer une classe property pour joueur_max, grosse_blind, mode_jeu et joueurs
    @property
    def joueur_max(self):
        """Retourne l'attribut 'joueur_max'"""
        return self.__joueur_max

    @property
    def grosse_blind(self):
        """Retourne l'attribut 'grosse_blind'"""
        return self.__grosse_blind

    @property
    def numero_table(self):
        """Retourne l'attribut 'numero_table'"""
        return self.__numero_table

    @property
    def mode_jeu(self):
        """Retourne l'attribut 'mode_jeu'"""
        return self.__mode_jeu

    @property
    def joueurs(self):
        """Retourne l'attribut 'joueurs'"""
        return self.__joueurs

    @property
    def manche(self):
        """retourne l'attribut 'manche'"""
        return self.__manche

    def __str__(self):
        """Représentation d'une table"""
        return f"Table {self.numero_table}, grosse blind : {self.grosse_blind} ({len(self)}/{self.joueur_max})"

    def __len__(self) -> int:
        """Retourne le nombre de joueurs à la table"""
        return len(self.__joueurs)

    @log
    def ajouter_joueur(self, joueur) -> None:
        """
        Ajoute un joueur à la table

        Paramètres
        ----------
        joueur : Joueur
            joueur à ajouter à la table

        Renvois
        -------
        None
        """

        if not isinstance(joueur, Joueur):
            raise TypeError("Le joueur n'est pas une instance de joueur")

        if len(self.__joueurs) >= self.__joueur_max:
            logger.warning(f"Table pleine : impossible d'ajouter {joueur.pseudo}")
            raise ValueError("Nombre maximum de joueurs atteint")

        self.__joueurs.append(joueur)
        logger.info(f"{joueur.pseudo} rejoint la table ({len(self.joueurs)}/{self.joueur_max})")

    @log
    def retirer_joueur(self, indice: int) -> Joueur:
        """
        Retire un joueur de la liste des joueurs selon son indice

        Paramètres
        ----------
        indice : int
            Indice du joueur à retirer dans la liste des joueurs

        Renvois
        -------
        Joueur
            Retourne le joueru retirée de la liste des joueurs
        """

        if not isinstance(indice, int):
            raise TypeError("L'indice doit être un entier")

        if indice >= len(self.__joueurs):
            raise IndexError(f"Indice plus grand que le nombre de joueurs : {len(self.__joueurs)}")

        if indice < 0:
            raise IndexError("Indice négatif impossible")

        logger.info(f"Le joueur {self.joueurs[indice].pseudo} est retiré de la table")
        return self.__joueurs.pop(indice)

    @log
    def mettre_grosse_blind(self, montant: int) -> None:
        """
        Change la valeur de la grosse blind

        Paramètres
        ----------
        credit : int
            nouvelle valeur de la grosse blind

        """
        if not isinstance(montant, int):
            raise TypeError("Le crédit doit être un entier")

        self.__grosse_blind = montant
        logger.info(f"La grosse blind de la table passe à {montant}")

    @log
    def rotation_dealer(self) -> None:
        """Change l'ordre dans la liste de joueur"""
        dealer = self.retirer_joueur(0)
        self.ajouter_joueur(dealer)

        logger.info(f"{dealer.pseudo} devient dealer")

    @log
    def nouvelle_manche(self) -> None:
        """Lance une manche"""
        for indice_joueur in range(len(self.__joueurs)):
            if self.__joueurs[indice_joueur].credit < self.__grosse_blind:
                self.retirer_joueur(indice_joueur)

        if len(self.__joueurs) < 2:
            raise Exception(
                f"Trop peu de joeuurs sur la table pour lancer une manche : {len(self.__joueurs)}"
            )

        self.__manche = Manche(info=InfoManche(self.__joueurs), grosse_blind=self.__grosse_blind)
