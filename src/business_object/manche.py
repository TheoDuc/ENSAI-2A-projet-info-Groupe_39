"""Implémentation de la classe Manche"""

from business_object.board import Board
from business_object.combinaison.combinaison import AbstractCombinaison
from business_object.evaluateur_combinaison import EvaluateurCombinaison
from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from utils.log_decorator import log


class Manche:
    """
    Modélisation d'une manche de poker, depuis la distribution des cartes
    jusqu'à l'attribution du pot.

    Attributs principaux
    --------------------
    TOURS : tuple
        Les différentes étapes d'une manche de poker.
    __tour : int
        Tour actuel de la manche (0=preflop, 1=flop, 2=turn, 3=river)
    __info : InfoManche
        Informations sur les joueurs, leurs mains, mises et statuts
    __reserve : Reserve
        Pioche de cartes pour la manche
    __board : Board
        Cartes communes visibles sur la table
    __indice_joueur_actuel : int
        Indice du joueur dont c'est le tour
    __grosse_blind : int
        Valeur de la grosse blind
    """

    __TOURS = ("preflop", "flop", "turn", "river")

    def __init__(self, info: InfoManche, grosse_blind: int):
        """
        Initialise une manche de poker.

        Paramètres
        ----------
        info : InfoManche
            Objet contenant les informations des joueurs et leurs mains
        grosse_blind : int
            Montant de la grosse blind, doit être strictement positif

        Exceptions
        ----------
        TypeError : Si info n'est pas un InfoManche ou grosse_blind n'est pas un int
        ValueError : Si grosse_blind <= 0
        """
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
        self.__info = info
        self.__reserve = Reserve(None)
        self.__board = Board([])
        self.__indice_joueur_actuel = 0
        self.__grosse_blind = grosse_blind

    # Propriétés
    @property
    def tour(self) -> int:
        return self.__tour

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
    def indice_joueur_actuel(self) -> int:
        return self.__indice_joueur_actuel

    @property
    def grosse_blind(self) -> int:
        return self.__grosse_blind

    @classmethod
    def TOURS(cls) -> tuple:
        return cls.__TOURS

    def __str__(self):
        return (
            f"Manche(tour={self.tour}, "
            f"grosse_blind={self.grosse_blind}, "
            f"board={self.board})"
        )

    # Déroulement des tours

    def reset_indice_nouveau_tour(self):
        self.__indice_joueur_actuel = 1
        self.joueur_suivant()

    @log
    def preflop(self):
        """Distribution des cartes initiales et mise des blinds"""
        self.__reserve.melanger()
        self.__info.assignation_mains(self.__reserve.distribuer(len(self.__info.joueurs)))
        self.__info.suivre(self.indice_joueur_actuel, self.grosse_blind // 2)
        self.joueur_suivant()
        self.__info.changer_statut(self.indice_joueur_actuel, 1)
        self.__info.suivre(self.indice_joueur_actuel, self.grosse_blind - (self.grosse_blind // 2))
        self.joueur_suivant()
        self.__info.changer_statut(self.indice_joueur_actuel, 2)


    @log
    def flop(self):
        """Révélation des 3 premières cartes communes"""
        for _ in range(3):
            self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.reset_indice_nouveau_tour()
        self.__info.statuts_nouveau_tour()

    @log
    def turn(self):
        """Révélation de la quatrième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.reset_indice_nouveau_tour()
        self.__info.statuts_nouveau_tour()

    @log
    def river(self):
        """Révélation de la cinquième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.reset_indice_nouveau_tour()
        self.__info.statuts_nouveau_tour()

    def fin_du_tour(self) -> bool:
        """
        Indique si les conditions sont réunies pour passer au tour suivant

        Paramètres
        ----------
        None

        Renvois
        -------
        bool
            Vrai si tout les joueurs ont égalisé / couché / All in
        """
        for s in self.info.statuts:
            if s in [0, 1]:
                return False
        return True

    def fin_de_manche(self):
        n = 0
        for s in self.info.statuts:
            if s != 3:
                n += 1
        if n == 0:
            raise ValueError("Les joueurs ne peuvent être tous couchés")
        return (n == 1)

    # Gestion du pot*

    
    def classement(self):
        if self.tour < 3:
            raise RuntimeError("Impossible de classer les joueurs : la board n'est pas dévoilé.")
        
        n = len(self.info.joueurs)
        joueurs_en_lice = self.info.joueurs_en_lice()
        board = self.board
        
        for i in range(n):
            Combinaison[i] = EvaluateurCombinaison.eval(self.info.mains[i].cartes + board.cartes)

        classement = [0] * n
        for i in joueurs_en_lice:
            c = 0
            for j in joueurs_en_lice:
                if Combinaison[j] >= Combinaison[i]:
                    c += 1
            classement[i] = c

    def gains(self):

        if self.tour < 3:
            raise RuntimeError("Impossible de classer les joueurs : la board n'est pas dévoilé.")
        
        a_distribuer = self.info.mises.copy()
        pot = self.info.valeur_pot()
        n = len(a_distribuer)
        classement = self.classement()
        gains = [0] * n
        c = 1
        while pot > 0 and c <= n:
            for i in range(n):
                beneficiaires = []
                if c == classement[i]:
                    beneficiaires.append(i)
            while beneficiaires != []:
                min = 0
                p = len(beneficiaires)
                for b in range(p):
                    if a_distribuer[beneficiaires[p]] < a_distribuer[beneficiaires[min]]:
                        min = b
                for i in range(n):
                    d = min(a_distribuer[beneficiaires[min]], a_distribuer[i])
                    for j in beneficiaires:
                        gains[j] += d/p
                    a_distribuer[i] -= d
                del beneficiaires[min]
            c += 1
            pot = 0
            for i in a_distribuer:
                pot += i
        return gains           

    def distribuer_pot(self):
        """
        Distribution du pot aux joueurs encore en lice selon la force de leur main.

        Renvois
        -------
        list[int]
            Gains attribués à chaque joueur
        """
        if not self.fin_de_manche():
            raise RuntimeError("Impossible de distribuer le pot : la manche n'est pas terminée.")

        if len(joueurs_en_lice) == 0:
            raise RuntimeError("Tous les joueurs ne peuvent être couchés.")

        n = len(self.info.joueurs)

        if self.tour < 3:
            gains = [0] * n
            i = self.info.joueurs_en_lice[0]
            gains[i] = self.info.valeur_pot()

        else:
            gains = self.gains()

        return gains
            
    # Gestion des joueurs
    def indice_joueur_suivant(self):
        """
        Retourne l'indice du joueur suivant qui n'est pas couché ou all in.
        """
        indice = self.indice_joueur_actuel
        statuts = self.info.statuts
        if indice == len(statuts) - 1:
            indice = 0
        else:
            indice += 1
        if all(s == 3 for s in statuts):
            raise ValueError("Tous les joueurs ne peuvent être couchés.")
        else:
            while statuts[indice] in [3, 4]:
                if indice == len(statuts) - 1:
                    indice = 0
                else:
                    indice += 1
        return indice

    def joueur_suivant(self):
        self.__indice_joueur_actuel = self.indice_joueur_suivant()
                
    def joueur_indice(self, joueur):
        for i in range(len(self.info.joueurs)):
            if self.info.joueurs[i] == joueur:
                return i
        raise ValueError("Le joueur n'est pas dans cette manche.")
    
    def est_tour(self, joueur):
        if self.indice_joueur_actuel == self.joueur_indice(joueur):
            return True
        else : return False