"""Implémentation de la classe Manche"""

from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from business_object.board import Board
from business_object.evaluateur_combinaison import EvaluateurCombinaison
from business_object.combinaison.combinaison import AbstractCombinaison

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
        Reserve.melanger(self.__reserve)
        InfoManche.assignation_mains(self.__info, distribuer(self.__reserve, len(self.__info.joueurs)))
        InfoManche.miser(self.__info, 0, self.__grosse_blind/2)
        InfoManche.miser(self.__info, 1, self.__grosse_blind)

    def flop(self):
        for i in range(3):
            Board.reveler(self.__reserve, self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def turn(self):
        Board.reveler(self.__reserve, self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def river(self):
        Board.reveler(self.__reserve, self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def ajouter_au_pot(self, credit):
        self.__pot += credit

    def distribuer_pot(self):
        joueurs_en_lice = {}
        board = self.board.cartes
        for i in range(len(self.info.joueurs)):
            if self.info.tour_couche[i] == None:
                main = self.info.mains[i]
                joueurs_en_lice[i] = EvaluateurCombinaison.eval(main.cartes+board)

        """tri par insertion, la comparaison étant celle des forces des combinaisons des joueurs"""
        classement = [i for i in joueurs_en_lice]
        for i in range(1, len(classement)):
            j = i - 1
            while j >= 0 and AbstractCombinaison.gt(joueurs_en_lice[classement[j]], joueurs_en_lice[classement[i]]):
                classement[j + 1] = classement[j]
                j -= 1
            classement[j + 1] = classement[i]
        """on distribue en partant de la meilleure main puis si besoin pots secondaires à répartir"""
        mises = self.info.mises.copy()
        gains = [0] * len(mises)
        for i in classement:
            for j in range(len(mises)):
                gains[i] += max(mises[i], mises[j])
                mises[j] = max(0, mises[j]-mises[i])
        mises = self.info.mises.copy()
        ### reste à ajouter les crédits aux joueurs
        return gains-mises