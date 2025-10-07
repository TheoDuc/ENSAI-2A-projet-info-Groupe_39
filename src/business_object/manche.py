"""Implémentation de la classe Manche"""

from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from business_object.board import Board

class Manche:
    """ Modélisation d'une manche de poker, c'est-à-dire une séquence complète de jeu 
    depuis la distribution des cartes jusqu'à l'attribution du pot. """

    __TOURS = ("preflop", "flop", "turn", "river")

    def __init__(self, info: InfoManche, grosse_blind: int):
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

        Exceptions
        ----------
        TypeError
            Si un des paramètres n'a pas le bon type.
        ValueError
            Si grosse_blind est inférieure ou égale à 0.
        """

        # --- Vérifications des types ---
        if not isinstance(info, InfoManche):
            raise TypeError(f"Le paramètre 'info' doit être une instance de InfoManche, pas {type(info).__name__}.")
        if not isinstance(grosse_blind, int):
            raise TypeError(f"Le paramètre 'grosse_blind' doit être un entier, pas {type(grosse_blind).__name__}.")
        
        # --- Vérification de la validité de la grosse blind ---
        if grosse_blind <= 0:
            raise ValueError("Le montant de la grosse blind doit être strictement positif.")

        # --- Initialisation des attributs ---
        self.__tour = 0
        self.__pot = 0
        self.__info = info
        self.__reserve = Reserve(None)
        self.__board = Board([])
        self.__indice_joueur_actuel = 0
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

    def __str__(self):
        return (f"Manche(tour={self.tour}, "
                f"pot={self.pot}, "
                f"grosse_blind={self.grosse_blind}, "
                f"board={self.board})")

    def preflop(self):
        melanger(self.__reserve)
        assignation_mains(self.__info, distribuer(self.__reserve, len(self.__info.joueurs)))
        miser(self.__info, 0, self.__grosse_blind/2)
        miser(self.__info, 1, self.__grosse_blind)

    def flop(self):
        for i in range(3):
            reveler(self.__reserve, self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def turn(self):
        reveler(self.__reserve, self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def river(self):
        reveler(self.__reserve, self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def ajouter_au_pot(self, credit):
        self.__pot += credit

    def distribuer_pot(self):
        pass