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
        """Indique si la manche est terminée"""
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

    def est_tour(self, joueur) -> bool:
        """Vérifie si c'est au tour du joueur"""
        return self.indice_joueur_actuel == self.indice_joueur(joueur)

    def indice_joueur_suivant(self) -> int:
        """
        Retourne l'indice du joueur suivant à qui c'est le tour de jouer

        Renvois
        -------
        int
            Indice du prochain joueur actif
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
        """Passe au joueur suivant"""
        self.__indice_joueur_actuel = self.indice_joueur_suivant()

    # ---------------------------------------
    # Phases de la manche
    # ---------------------------------------

    def indice_nouveau_tour(self):
        """Donne la main au joueur après le dealer encore en jeu"""
        self.__indice_joueur_actuel = len(self.info.joueurs) - 1
        self.joueur_suivant()

    def statuts_nouveau_tour(self):
        """Met à jour les statuts des joueurs pour un nouveau tour"""
        for i in range(len(self.info.statuts)):
            if self.info.statuts[i] not in [3, 4]:
                self.info.modifier_statut(i, 0)

    def nouveau_tour(self):
        """Passe à la phase suivante et met à jour les statuts des joueurs"""
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
    def turn(self) -> str:
        """Révélation de la quatrième carte commune"""
        self.__reserve.reveler(self.__board)
        self.nouveau_tour()
        return "La phase de turn commence !"

    @log
    def river(self) -> str:
        """Révélation de la cinquième carte commune"""
        self.__reserve.reveler(self.__board)
        self.nouveau_tour()
        return "La phase de river commence !"

    # ---------------------------------------
    # Fin de tour et fin de manche
    # ---------------------------------------

    def fin_du_tour(self) -> bool:
        """Vérifie si tous les joueurs ont égalisé / couché / All-in"""
        return all(s not in [0, 1] for s in self.info.statuts)

    def fin_de_manche(self) -> bool:
        """Vérifie si la manche est terminée"""
        n = sum(1 for s in self.info.statuts if s != 3)
        if n == 0:
            raise ValueError("Les joueurs ne peuvent être tous couchés")
        return n == 1 or (self.fin_du_tour() and self.tour == 3)

    # ---------------------------------------
    # Actions d'un joueur
    # ---------------------------------------

    @log
    def checker(self, indice_joueur: int):
        """Le joueur temporise si il en a la possibilité"""
        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")
        if self.info.statuts[indice_joueur] != 0:
            raise ValueError("Le joueur doit avoir le statut d'innactif pour checker")
        self.info.modifier_statut(indice_joueur, 2)

    @log
    def suivre(self, indice_joueur: int, relance: int = 0) -> int:
        """Ajoute une mise pour un joueur"""
        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")
        if not isinstance(relance, int) or relance < 0:
            raise ValueError("Le montant doit être un entier positif")

        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        if pour_suivre >= self.info.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur doit all-in")
        if relance + pour_suivre >= self.info.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur ne peut relancer autant")

        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = pour_suivre + relance + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)
        self.info.modifier_statut(indice_joueur, 2)

        if relance > 0:
            for i in range(len(self.info.statuts)):
                if i != indice_joueur and self.info.statuts[i] in [0, 2]:
                    self.info.statuts[i] = 1

        return pour_suivre + relance

    @log
    def all_in(self, indice_joueur: int) -> int:
        """Mise tout le crédit d'un joueur"""
        if self.info.statuts[indice_joueur] in [3, 4]:
            raise ValueError("Le joueur ne peut plus all-in")

        montant = self.info.joueurs[indice_joueur].credit
        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = montant + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)
        self.info.modifier_statut(indice_joueur, 4)

        if montant > pour_suivre:
            for i in range(len(self.info.statuts)):
                if self.info.statuts[i] in (0, 2):
                    self.info.statuts[i] = 1

        return montant

    @log
    def se_coucher(self, indice_joueur: int):
        """Marque un joueur comme couché"""
        self.info.modifier_tour_couche(indice_joueur, self.tour)
        self.info.modifier_statut(indice_joueur, 3)

    # ---------------------------------------
    # Pot et gains
    # ---------------------------------------

    def valeur_pot(self) -> int:
        """Retourne la valeur totale du pot"""
        return sum(self.info.mises)

    @property
    def joueurs_en_lice(self) -> list[int]:
        """Renvoie la liste des indices des joueurs qui ne sont pas couchés (statut != 3)"""
        return [i for i, statut in enumerate(self.info.statuts) if statut != 3]

    def classement(self) -> list[int]:
        """Classe les joueurs en fonction de leurs mains. Rang 1 = meilleur."""
        if self.tour < 3 or len(self.board.cartes) < 5:
            raise ValueError("Impossible de classer : board non complète.")

        joueurs_actifs = self.joueurs_en_lice
        evals = {}

        for i in joueurs_actifs:
            cartes_totales = self.info.mains[i].cartes + self.board.cartes
            # On prend la combinaison forcée si elle existe
            if hasattr(self.info.mains[i], "_combinaison") and self.info.mains[i]._combinaison:
                comb = self.info.mains[i]._combinaison
            else:
                comb = EvaluateurCombinaison.eval(cartes_totales)
            evals[i] = comb._valeur_comparaison()

        # Tri décroissant par valeur de combinaison
        sorted_joueurs = sorted(joueurs_actifs, key=lambda i: evals[i], reverse=True)

        classement_dict = {}
        rang = 1
        idx = 0

        while idx < len(sorted_joueurs):
            debut = idx
            # Regroupe les ex-aequo
            while (
                idx + 1 < len(sorted_joueurs)
                and evals[sorted_joueurs[idx + 1]] == evals[sorted_joueurs[debut]]
            ):
                idx += 1
            # Attribuer le même rang à tous les ex-aequo
            for k in range(debut, idx + 1):
                classement_dict[sorted_joueurs[k]] = rang
            # Incrément du rang après les ex-aequo
            rang += idx - debut + 1
            idx += 1

        # Rang pour les joueurs non-actifs (statut != 2)
        for i in range(len(self.info.joueurs)):
            if i not in classement_dict:
                classement_dict[i] = rang

        # Debug optionnel
        print("Classement:", classement_dict)
        for i in range(len(self.info.joueurs)):
            combo = getattr(self.info.mains[i], "_combinaison", None)
            print(f"Joueur {i} combo:", combo)

        return [classement_dict[i] for i in range(len(self.info.joueurs))]

    def recuperer(self, mise: int, montant_a_recupere: int) -> list[int]:
        """Récupère une certaine quantité d'un entier"""
        if montant_a_recupere >= mise:
            return [0, mise]
        return [mise - montant_a_recupere, montant_a_recupere]

    def gains(self) -> dict[int, float]:
        """
        Calcule les gains de chaque joueur à la fin de la manche.
        Prend en compte les ex-aequo et les side pots.

        Retour
        ------
        dict[int, float] : clé = id_joueur, valeur = gain
        """
        if self.tour < 3 or len(self.board.cartes) < 5:
            raise ValueError("Le board n'est pas complet, impossible de calculer les gains.")

        n_joueurs = len(self.info.joueurs)
        mises_restantes = self.info.mises[:]
        classement = self.classement()  # Rang 1 = meilleur
        gains = {j.id_joueur: 0.0 for j in self.info.joueurs}

        # Tant qu'il reste des mises à distribuer
        while any(m > 0 for m in mises_restantes):
            # Joueurs actifs pour ce pot
            participants = [i for i, m in enumerate(mises_restantes) if m > 0]
            if not participants:
                break

            # Montant minimum parmi les mises restantes
            mise_min = min(mises_restantes[i] for i in participants)
            # Montant du pot courant
            pot = sum(min(mises_restantes[i], mise_min) for i in participants)

            # Déduire la mise_min de chaque participant
            for i in participants:
                mises_restantes[i] -= mise_min

            # Identifier les meilleurs joueurs pour ce pot
            min_rang = min(classement[i] for i in participants)
            meilleurs = [i for i in participants if classement[i] == min_rang]

            # Partage équitable du pot
            part = pot / len(meilleurs)
            for i in meilleurs:
                gains[self.info.joueurs[i].id_joueur] += part

        return gains

    # ---------------------------------------
    # Fonction générale d'évolution de la partie
    # ---------------------------------------

    @log
    def action(self, joueur, action: str, relance: int = 0):
        """
        Effectue l'action souhaitée d'un joueur et met à jour la manche

        Paramètres
        ----------
        joueur : Joueur
            Le joueur effectuant l'action
        action : str
            Action souhaitée ("checker", "suivre", "all-in", "se coucher")
        relance : int, optionnel
            Montant de la relance si action = "suivre"

        Renvois
        -------
        int ou dict[int, float]
            Montant misé si tour non terminé, sinon gains si fin de manche

        Exceptions
        ----------
        Exception : si ce n'est pas au joueur de jouer ou si la manche est terminée
        ValueError : si l'action est invalide
        """
        indice_joueur = self.indice_joueur(joueur)

        if indice_joueur != self.indice_joueur_actuel:
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")
        if self.fin:
            raise Exception("La manche est déjà terminée, aucune action ne peut être effectuée")

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
            raise ValueError(f"L'action {action} n'existe pas, actions possibles {actions}")

        if self.fin_de_manche():
            self.fin = True
            return self.gains()

        if self.fin_du_tour():
            if self.tour == 0:
                self.flop()
            elif self.tour == 1:
                self.turn()
            elif self.tour == 2:
                self.river()
            return montant

        self.joueur_suivant()
        return montant
