"""Implémentation de la classe Manche"""

from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from business_object.board import Board
from business_object.evaluateur_combinaison import EvaluateurCombinaison
from business_object.combinaison.combinaison import AbstractCombinaison
from business_object.joueur import Joueur


class Manche:
    """ 
    Modélisation d'une manche de poker, depuis la distribution des cartes jusqu'à l'attribution du pot. 
    """

    __TOURS = ("preflop", "flop", "turn", "river")

    def __init__(self, info: InfoManche, grosse_blind: int):
        # Vérifications des types
        if not isinstance(info, InfoManche):
            raise TypeError(
                f"Le paramètre 'info' doit être une instance de InfoManche, pas {type(info).__name__}."
            )
        if not isinstance(grosse_blind, int):
            raise TypeError(
                f"Le paramètre 'grosse_blind' doit être un entier, pas {type(grosse_blind).__name__}."
            )
        if grosse_blind <= 0:
            raise ValueError("Le montant de la grosse blind doit être strictement positif.")

        # Initialisation des attributs
        self.__tour = 0
        self.__pot = 0
        self.__info = info
        self.__reserve = Reserve(None)
        self.__board = Board([])
        self.__indice_joueur_actuel = 0
        self.__grosse_blind = grosse_blind

    # -------------------- Propriétés -------------------- #
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
        return cls.__TOURS

    def __str__(self):
        return (
            f"Manche(tour={self.tour}, "
            f"pot={self.pot}, "
            f"grosse_blind={self.grosse_blind}, "
            f"board={self.board})"
        )

    # -------------------- Déroulement des tours -------------------- #
    def preflop(self):
        """Distribution des cartes initiales et mise des blinds"""
        self.__reserve.melanger()
        self.__info.assignation_mains(
            self.__reserve.distribuer(len(self.__info.joueurs))
        )
        self.__info.miser(0, self.__grosse_blind // 2)
        self.__info.miser(1, self.__grosse_blind)

    def flop(self):
        """Révélation des 3 premières cartes communes"""
        for _ in range(3):
            self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def turn(self):
        """Révélation de la quatrième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    def river(self):
        """Révélation de la cinquième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2

    # -------------------- Gestion du pot -------------------- #
    def ajouter_au_pot(self, credit):
        """Ajoute un montant au pot courant"""
        self.__pot += credit

    def distribuer_pot(self):
        """
        Distribution du pot aux joueurs encore en lice selon la force de leur main.
        Retourne la liste des gains pour chaque joueur.
        """
        joueurs_en_lice = {}
        board = self.board.cartes

        # Évaluation des mains des joueurs encore actifs
        for i in range(len(self.info.joueurs)):
            if self.info.tour_couche[i] is None:
                main = self.info.mains[i]
                joueurs_en_lice[i] = EvaluateurCombinaison.eval(main.cartes + board)

        # Tri par insertion selon la force des combinaisons
        classement = [i for i in joueurs_en_lice]
        for i in range(1, len(classement)):
            j = i - 1
            while (
                j >= 0
                and AbstractCombinaison.gt(joueurs_en_lice[classement[j]], joueurs_en_lice[classement[i]])
            ):
                classement[j + 1] = classement[j]
                j -= 1
            classement[j + 1] = classement[i]

        # Calcul des gains
        mises = self.info.mises.copy()
        gains = [0] * len(mises)
        for i in classement:
            for j in range(len(mises)):
                gains[i] += max(mises[i], mises[j])
                mises[j] = max(0, mises[j] - mises[i])

        mises = self.info.mises.copy()

        # Attribution des crédits aux joueurs
        for i in range(len(gains)):
            joueur = self.__info.joueurs[i]
            joueur.ajouter_credits(gains[i])
            joueur.retirer_credits(mises[i])

        return gains

    # -------------------- Gestion des joueurs -------------------- #
    def joueur_suivant(self):
        """
        Retourne l'indice du joueur suivant qui n'est pas couché.
        """
        indice = self.__indice_joueur_actuel + 1
        tour_couche = self.info.tour_couche

        if None not in tour_couche:
            raise ValueError("Tous les joueurs ne peuvent être couchés.")
        else:
            while tour_couche[indice] is not None:
                if indice == len(tour_couche) - 1:
                    indice = 0
                else:
                    indice += 1
            return indice
