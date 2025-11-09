"""Implémentation de la classe Manche"""

from business_object.board import Board
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

        if grosse_blind < 2:
            raise ValueError("Le montant de la grosse blind doit être supérieur à 2")

        # Initialisation des attributs
        self.__tour = 0
        self.__info = info
        self.__reserve = Reserve(None)
        self.__board = Board([])
        self.__indice_joueur_actuel = 0
        self.__grosse_blind = grosse_blind

    # ---------------------------------------
    # Property
    # ---------------------------------------

    @property
    def tour(self) -> int:
        """Tour de jeu actuel"""
        return self.__tour

    @property
    def info(self) -> InfoManche:
        """Informations des joueurs dans la partie"""
        return self.__info

    @property
    def reserve(self) -> Reserve:
        """Paquet de carte constituant la pioche"""
        return self.__reserve

    @property
    def board(self) -> Board:
        """Cartes communes à chaque joueurs"""
        return self.__board

    @property
    def indice_joueur_actuel(self) -> int:
        """Indice du joueur à qui c'est le tour"""
        return self.__indice_joueur_actuel

    @property
    def grosse_blind(self) -> int:
        """Valeur de la grosse blind"""
        return self.__grosse_blind

    # ---------------------------------------
    # Classmethod
    # ---------------------------------------

    @classmethod
    def TOURS(cls) -> tuple:
        """Liste des phases de jeu d'une manche"""
        return cls.__TOURS

    # ---------------------------------------
    # Affichage
    # ---------------------------------------

    def __str__(self) -> str:
        """Représentation informelle d'un objet de type 'Manche'"""
        return f"Manche(tour={self.TOURS()[self.tour]}, grosse_blind={self.grosse_blind}, board={self.board})"

    # ---------------------------------------
    # Tours des joueurs et joueurs
    # ---------------------------------------

    def joueur_indice(self, joueur) -> int:
        """Retourne l'indice du joueur si il est présent dans la manche"""
        for i in range(len(self.info.joueurs)):
            if self.info.joueurs[i] == joueur:
                return i

        raise ValueError("Le joueur n'est pas dans cette manche")

    def est_tour(self, joueur):
        """Vérifie si c'est au tour du joueur"""
        if self.indice_joueur_actuel == self.joueur_indice(joueur):
            return True
        else:
            return False

    def indice_joueur_suivant(self):
        """
        Retourne l'indice du joueur suivant à qui c'est le tour de jouer
        """

        if all(s == 3 for s in self.info.statuts):
            raise ValueError("Tous les joueurs ne peuvent être couchés")

        indice = self.indice_joueur_actuel
        statuts = self.info.statuts

        if indice == len(statuts) - 1:
            indice = 0
        else:
            indice += 1

        while statuts[indice] in [3, 4]:
            if indice == len(statuts) - 1:
                indice = 0
            else:
                indice += 1

        return indice

    def joueur_suivant(self):
        """
        Blabla
        """

        self.__indice_joueur_actuel = self.indice_joueur_suivant()

    # ---------------------------------------
    # Phases de la manche
    # ---------------------------------------

    def indice_nouveau_tour(self):
        """Donne la main au joueur après le dealer encore en jeu"""
        self.__indice_joueur_actuel = len(self.info.joueurs) - 1
        self.joueur_suivant()

    def statuts_nouveau_tour(self):
        """Modifie le statut des joueurs à jour en innactif"""
        for i in range(len(self.info.statuts)):
            if self.info.statuts[i] not in [3, 4]:
                self.info.modifier_statut(i, 0)

    @log
    def preflop(self):
        """Distribution des cartes initiales et mise des blinds"""
        self.reserve.melanger()
        self.info.assignation_mains(self.reserve.distribuer(len(self.info.joueurs)))
        self.suivre(self.indice_joueur_actuel, self.grosse_blind // 2)
        self.joueur_suivant()
        self.suivre(self.indice_joueur_actuel, self.grosse_blind - (self.grosse_blind // 2))
        self.joueur_suivant()

    @log
    def flop(self):
        """Révélation des 3 premières cartes communes"""
        for _ in range(3):
            self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.indice_nouveau_tour()
        self.statuts_nouveau_tour()

    @log
    def turn(self):
        """Révélation de la quatrième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.indice_nouveau_tour()
        self.statuts_nouveau_tour()

    @log
    def river(self):
        """Révélation de la cinquième carte commune"""
        self.__reserve.reveler(self.__board)
        self.__tour += 1
        self.indice_nouveau_tour()
        self.statuts_nouveau_tour()

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

    def fin_de_manche(self) -> bool:
        n = 0
        for s in self.info.statuts:
            if s != 3:
                n += 1
        if n == 0:
            raise ValueError("Les joueurs ne peuvent être tous couchés")
        return n == 1

    # ---------------------------------------
    # Actions d'un joueur
    # ---------------------------------------

    @log
    def checker(self, indice_joueur):
        """
        Le joueur temporise si il en a la possibilité
        """

        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")

        # Si le joueur n'est pas innactif, relever une erreur
        if self.info.statuts[indice_joueur] != 0:
            raise ValueError(f"Le joueur doit avoir le statut d'innactif pour checker")
        
        self.info.modifier_statut[indice_joueur, 2]


    @log
    def suivre(self, indice_joueur: int, relance : int = 0) -> int:
        """
        Ajoute une mise pour un joueur

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste
        montant : int
            Montant à miser
        """

        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")

        if not isinstance(relance, int) or relance < 0:
            raise ValueError("Le montant doit être un entier positif")

        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        # Si le joueur n'a pas assez de crédits pour suivre
        if pour_suivre >= self.info.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur doit all-in")

        # Si le joueur n'a pas assez de crédits pour relancer autant
        if relance + pour_suivre >= self.info.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur ne peut relancer autant")

        # Calcule et mise à jour de la mise
        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = pour_suivre + relance + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)

        self.info.modifier_statut(indice_joueur, 2)

        # Cas où le joueur relance
        if relance > 0:
            # Met à jour le statut des autres joueurs innactifs ou à jour
            for i in range(len(self.info.statuts)):
                if self.info.statuts[i] in [0, 2]:
                    self.info.statuts[i] = 1

        return pour_suivre + relance

    @log
    def all_in(self, indice_joueur: int) -> int:
        """Mise tout les crédits d'un joueur"""

        if self.info.statut[indice_joueur] in [3,4]:
            raise ValueError("Le joueur ne peut plus all-in")

        # Le montant total du all-in
        montant = self.info.joueurs[indice_joueur].credit
        # Le montant nécessaire pour atteindre la mise actuelle
        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = montant + ancienne_mise
        self.info.modifier_statut(indice_joueur, 4)

        # Cas où le joueur all-in dépasse la mise la plus haute
        if montant > pour_suivre:
            # Réinitialise le statut des
            for i in range(len(self.info.statuts)):
                if self.info.statuts[i] in (0, 2):
                    self.info.statuts[i] = 1

        return montant

    @log
    def se_coucher(self, indice_joueur: int):
        """
        Marque un joueur comme couché.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste
        """

        self.info.modifier_tour_couche(indice_joueur, self.tour)
        self.info.modifier_statut(indice_joueur, 3)

    # ---------------------------------------
    # Fin de partie et allocation des gains
    # ---------------------------------------

    def valeur_pot(self):
        """Retourne la valer du pot"""
        pot = 0

        for mise in self.info.mises:
            pot += mise
        
        return pot

    def joueurs_en_lice(self):
        """Renvoie la liste d'indices des joueurs qui ne sont pas couchés"""
        liste_indices = []
        for i in range(len(self.info.joueurs)):
            if self.info.statuts[i] != 3:
                liste_indices.append(i)
        return liste_indices

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
            raise RuntimeError("Impossible de classer les joueurs : la board n'est pas dévoilé entièrement")

        a_distribuer = self.info.mises.copy()
        pot = self.valeur_pot()
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
                        gains[j] += d / p
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
