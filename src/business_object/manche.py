"""Implémentation de la classe Manche"""

from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from business_object.board import Board

class Manche:
    """ Modélisation d'une manche de poker, c'est à dire une séquence complète de jeu depuis la 
    distribution des cartes jusqu'à l'attribution du pot. """

    """Attributs de la classe"""
    __TOURS = ("preflop", "flop", "turn", "river")

    def __init__(self, info : InfoManche, reserve : Reserve, board : Board, grosse_blind : int):
        """
        Instanciation d'une manche

        Paramètres
        ----------
        info : InfoManche
            Informations sur la manche
        reserve : Reserve
            Liste des cartes en réserve
        board : Board
            Liste des 5 cartes dévoilées
        grosse_blind : int
            Montant de la blind à la table

        Renvois
        -------
        Manche
            Instance de Manche
        """
        
        self.__tour = 0
        self.__pot = 0
        self.__info = info
        self.__reserve = reserve
        self.__board = board
        self._indice_joueur_actuel = 0
        self.__grosse_blind = grosse_blind

    @property
    def tour(self) -> int:
        return self.__tour

    @property
    def pot(self) -> int:
        return self.__pot

    @property
    def info(self) -> InfoManche:
        return self.__info

    @property
    def reserve(self) -> Reserve:
        return self.__reserve

    @property
    def board(self) -> Board:
        return self.__board

    @property
    def grosse_blind(self) -> int:
        return self.__grosse_blind

    @classmethod
    def TOURS(cls) -> tuple:
        """Retourne la liste des valeurs possibles d'un tour"""
        return cls.__TOURS