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
        self.__fin = False

    # ---------------------------------------
    # Property
    # ---------------------------------------

    @property
    def tour(self) -> int:
        """Tour de jeu actuel"""
        return self.__tour

    @tour.setter
    def tour(self, value: int):
        """Permet de modifier le tour de jeu pour les tests ou progression de la manche"""
        if not isinstance(value, int) or not (0 <= value <= 3):
            raise ValueError("Le tour doit être un entier entre 0 et 3")
        self.__tour = value

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

    @property
    def fin(self) -> bool:
        """Indique si la mance est terminée ou non"""
        return self.__fin

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

    def indice_joueur(self, joueur) -> int:
        """Retourne l'indice du joueur si il est présent dans la manche"""
        for i in range(len(self.info.joueurs)):
            if self.info.joueurs[i] == joueur:
                return i

        raise ValueError("Le joueur n'est pas dans cette manche")

    def est_tour(self, joueur):
        """Vérifie si c'est au tour du joueur"""
        if self.indice_joueur_actuel == self.indice_joueur(joueur):
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

    def nouveau_tour(self):
        """
        Blabla
        """

        if self.tour == 3:
            raise ValueError("La manche est déjà au dernier tour")

        self.__tour += 1
        self.indice_nouveau_tour()
        self.statuts_nouveau_tour()

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
    def flop(self) -> str:
        """Révélation des 3 premières cartes communes"""
        for _ in range(3):
            self.__reserve.reveler(self.__board)

        self.nouveau_tour()

        return "La phase de flop commence !"

    @log
    def turn(self):
        """Révélation de la quatrième carte commune"""
        self.__reserve.reveler(self.__board)

        self.nouveau_tour()

        return "La phase de turn commence !"

    @log
    def river(self):
        """Révélation de la cinquième carte commune"""
        self.__reserve.reveler(self.__board)

        self.nouveau_tour()

        return "La phase de river commence !"

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

        return n == 1 or (self.fin_du_tour and self.tour == 3)

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

        # Si le joueur n'est pas innactif, soulever une erreur
        if self.info.statuts[indice_joueur] != 0:
            raise ValueError("Le joueur doit avoir le statut d'innactif pour checker")

        self.info.modifier_statut(indice_joueur, 2)  # comme c'est une méthode

    @log
    def suivre(self, indice_joueur: int, relance: int = 0) -> int:
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
            # On peut faire return self.all_in(indice_joueur)

        # Si le joueur n'a pas assez de crédits pour relancer autant
        if relance + pour_suivre >= self.info.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur ne peut relancer autant")

        # Calcule et mise à jour de la mise
        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = pour_suivre + relance + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)

        self.info.modifier_statut(indice_joueur, 2)

        return pour_suivre + relance

        # Cas où le joueur relance
        if relance > 0:
            # Met à jour le statut des autres joueurs innactifs ou à jour
            for i in range(len(self.info.statuts)):
                if i != indice_joueur and self.info.statuts[i] in [0, 2]:
                    self.info.statuts[i] = 1

        return pour_suivre + relance

    @log
    def all_in(self, indice_joueur: int) -> int:
        """Mise tout les crédits d'un joueur"""

        if self.info.statuts[indice_joueur] in [3, 4]:
            raise ValueError("Le joueur ne peut plus all-in")

        # Le montant total du all-in
        montant = self.info.joueurs[indice_joueur].credit
        # Le montant nécessaire pour atteindre la mise actuelle
        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = montant + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)
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

    @property
    def joueurs_en_lice(self):
        """Renvoie la liste d'indices des joueurs qui ne sont pas couchés"""
        liste_indices = []
        for i in range(len(self.info.joueurs)):
            if self.info.statuts[i] != 3:
                liste_indices.append(i)
        return liste_indices

    def classement(self) -> list[int]:
        """Renvoie une liste correspondant au classement de la partie"""

        if self.tour < 3 or len(self.board.cartes) < 5:
            raise ValueError(
                "Impossible de classer les joueurs : la board n'est pas dévoilée entièrement"
            )

        n = len(self.info.joueurs)
        joueurs_en_lice = self.joueurs_en_lice
        board = self.board

        Combinaison = [None] * n
        for i in joueurs_en_lice:
            cartes_totales = self.info.mains[i].cartes + board.cartes
            if len(cartes_totales) < 5:
                raise ValueError(f"Pas assez de cartes pour le joueur {i}")
            Combinaison[i] = EvaluateurCombinaison.eval(cartes_totales)

        # Calcul du score et classement (comme avant)
        scores = [0] * n
        for j1 in joueurs_en_lice:
            for j2 in joueurs_en_lice:
                if Combinaison[j1] >= Combinaison[j2]:
                    scores[j1] += 1

        classement = [0] * n
        top_scores = sorted(list(set(scores)), reverse=True)
        rang = 1
        for score in top_scores:
            indices = [i for i, s in enumerate(scores) if s == score and i in joueurs_en_lice]
            for i in indices:
                classement[i] = rang
            rang += len(indices)

        return classement

    def recuperer(self, mise: int, montant_a_recupere: int) -> list[int]:
        """Récupère une certaine quantité d'un entier"""
        if montant_a_recupere >= mise:
            return [0, mise]

        return [mise - montant_a_recupere, montant_a_recupere]

    def gains(self) -> dict:
        """Calcule les gains des joueurs en fin de manche."""

        joueurs = self.info.joueurs
        mises = self.info.mises.copy()
        classement = self.classement()
        en_lice = self.joueurs_en_lice()

        gains = {j: 0 for j in joueurs}

        # Cas avec un seul joueur en lice
        if len(en_lice) == 1:
            gagnant = joueurs[en_lice[0]]
            gains[gagnant] = sum(mises)
            return gains

        # Étape 1 : créer les side pots
        pots = []
        dernier_niveau = 0

        for mise_unique in set(mises):
            # Récupère les indices des participants dont la mise est supérieure ou égale à une mise
            participants = [i for i, m in enumerate(mises) if m >= mise_unique]

            # Si un seul joueur reste à ce niveau → pas de pot contesté
            if len(participants) <= 1:
                continue

            # Calcule la valeur du side pot et l'ajoute à la liste, avec les candidats à ce pot
            valeur_pot = (mise_unique - dernier_niveau) * len(participants)
            pots.append((valeur_pot, participants))
            dernier_niveau = mise_unique

        # Étape 2 : distribuer les pots
        for valeur_pot, participants in pots:
            # Extraire les rangs des participants au pot
            rangs = {i: classement[i] for i in participants if classement[i] > 0}

            # Trouver le meilleur rang (1 = meilleur, puis 2, etc.)
            meilleur_rang = min(rangs.values())

            # Trouver tous les joueurs ex aequo à ce rang
            meilleurs = [i for i, r in rangs.items() if r == meilleur_rang]

            # Partage équitable du pot
            gain_unitaire = valeur_pot // len(meilleurs)
            for i in meilleurs:
                gains[joueurs[i]] += gain_unitaire

        # Étape 3 : restituer le surplus (non contesté)
        if pots:
            dernier_niveau = max([m for m, _ in pots])
        else:
            dernier_niveau = 0

        for i, mise in enumerate(mises):
            if mise > dernier_niveau:
                gains[joueurs[i]] += mise - dernier_niveau

        return gains

    # ---------------------------------------
    # Fonction générale d'avolution de la partie
    # ---------------------------------------

    @log
    def action(self, joueur, action: str, relance: int = 0):
        """
        Effectue l'action souhaitée d'un joueur, et les modifications qui s'en suivents dans la Manche
        """

        indice_joueur = self.indice_joueur(joueur)

        # Vérifie que c'est au tour du joueur qui fait l'action
        if indice_joueur != self.indice_joueur_actuel:
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        # Vérifie que ce n'est pas la fin de la manche
        if self.fin:
            raise Exception("La manche est déjà terminée, aucune action ne peut être effectuée")

        # Réalise l'action désirée par le joueur
        if action == "checker":
            montant = self.checker(indice_joueur)
        elif action == "suivre":
            montant = self.suivre(indice_joueur, relance)
        elif action == "all-in":
            montant = self.all_in(indice_joueur)
        elif action == "se coucher":
            montant = self.se_coucher(indice_joueur)
        else:
            actions = ("checker", "suivre", "all-in", "se coucher")
            raise ValueError(
                f"L'action {action} n'existe pas, les actions possibles sont {actions}"
            )

        # Cas où c'est la fin de la manche
        if self.fin_de_manche():
            self.fin = True
            return self.gains()

        # Cas où c'est la fin d'un tour
        elif self.fin_du_tour():
            if self.tour == 0:
                self.flop()
            elif self.tour == 1:
                self.turn()
            elif self.tour == 2:
                self.river()

            return montant
        
        self.joueur_suivant()
        print(f"C'est à {self.info.joueurs[self.indice_joueur_actuel].pseudo} de jouer !")
        return montant
