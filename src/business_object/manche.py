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
    __pot : int
        Montant total du pot
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
        self.__pot = 0
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
            f"pot={self.pot}, "
            f"grosse_blind={self.grosse_blind}, "
            f"board={self.board})"
        )

    # Déroulement des tours
    @log
    def preflop(self):
        """Distribution des cartes initiales et mise des blinds"""
        self.__reserve.melanger()
        self.__info.assignation_mains(self.__reserve.distribuer(len(self.__info.joueurs)))
        self.__info.miser(0, self.__grosse_blind / 2)
        self.joueur_suivant()
        self.info.changer_statut(self.indice_joueur_actuel, 1)
        self.__info.miser(1, self.__grosse_blind)
        self.joueur_suivant()
        self.info.changer_statut(self.indice_joueur_actuel, 2)


    @log
    def flop(self):
        """Révélation des 3 premières cartes communes"""
        for _ in range(3):
            self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2
        for i in range(len(self.__info.statuts)):
            if self.__info.statuts[i] not in [3, 4]:
                self.__info.statuts[i] = 0

    @log
    def turn(self):
        """Révélation de la quatrième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2
        for i in range(len(self.__info.statuts)):
            if self.__info.statuts[i] not in [3, 4]:
                self.__info.statuts[i] = 0

    @log
    def river(self):
        """Révélation de la cinquième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.__indice_joueur_actuel = 2
        for i in range(len(self.__info.statuts)):
            if self.__info.statuts[i] not in [3, 4]:
                self.__info.statuts[i] = 0

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

        for i in range(len(self.info.statuts)):
            if self.info.statuts[i] in ["en retard", "à jour", "all in"]:
                dernier_joueur = i
        if self.__indice_joueur_actuel != dernier_joueur:
            return False
        for s in self.info.statuts:
            if s == "en retard":
                return False
        return True

    # Gestion du pot
    @log
    def ajouter_au_pot(self, credit) -> int:
        """Ajoute un montant au pot courant"""
        self.__pot += credit
        return self.pot

    def distribuer_pot(self):
        """
        Distribution du pot aux joueurs encore en lice selon la force de leur main.

        Renvois
        -------
        list[int]
            Gains attribués à chaque joueur
        """
        joueurs_en_lice = {}
        board = self.board.cartes


        # Évaluation des mains des joueurs encore actifs
        for i in range(len(self.info.joueurs)):
            if self.info.statuts[i] in ["à jour", "all in"]:
                main = self.info.mains[i]
                joueurs_en_lice[i] = EvaluateurCombinaison.eval(main.cartes + board)

        # Tri par insertion selon la force des combinaisons
        classement = [i for i in joueurs_en_lice]
        for i in range(1, len(classement)):
            j = i - 1
            while j >= 0 and AbstractCombinaison.gt(
                joueurs_en_lice[classement[j]], joueurs_en_lice[classement[i]]
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

    # Gestion des joueurs
    def joueur_suivant(self):
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
            while statuts[indice] in ["couché", "all in"]:
                if indice == len(statuts) - 1:
                    indice = 0
                else:
                    indice += 1
            self.__indice_joueur_actuel = indice
            if self.info.statuts[self.indice_joueur_actuel] == 0:
                
    def indice_joueur(self, joueur):
        for i in range(len(self.info.joueurs)):
            if self.info.joueurs[i] == joueur:
                return i
        raise ValueError("Le joueur n'est pas dans cette manche.")
    
    def est_tour(self, joueur):
        if self.indice_joueur_actuel == self.indice_joueur(joueur):
            return True
        else : return False
