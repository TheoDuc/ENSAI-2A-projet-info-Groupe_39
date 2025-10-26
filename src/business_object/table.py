"""Implémentation de la classe Table"""

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.manche import Manche


class Table:
    """Modélisation d'une table de jeu"""

    def __init__(
        self,
        joueur_max: int,
        grosse_blind: int,
        mode_jeu: int = 1,
        joueurs: list = [],
        manche: Manche = None,
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
        self.__mode_jeu = mode_jeu
        self.__joueurs = joueurs
        self.__manche = Manche

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

    def __len__(self) -> int:
        """Retourne le nombre de joueurs à la table"""
        return len(self.__joueurs)

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
        if len(self.__joueurs) >= self.__joueur_max:
            raise ValueError("Nombre maximum de joueurs atteint")
        elif not isinstance(joueur, Joueur):
            raise TypeError("Le joueur n'est pas une instance de joueur")
        else:
            self.__joueurs.append(joueur)

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
        if 0 > indice:
            raise IndexError("Indice négatif impossible")
        else:
            return self.__joueurs.pop(indice)

    def mettre_grosse_blind(self, credit: int) -> None:
        """
        Change la valeur de la grosse blind

        Paramètres
        ----------
        credit : int
            nouvelle valeur de la grosse blind

        """
        if not isinstance(credit, int):
            raise TypeError("Le crédit doit être un entier")
        else:
            self.__grosse_blind = credit

    def rotation_dealer(self) -> None:
        """Change l'ordre dans la liste de joueur"""
        dealer = self.retirer_joueur(0)
        self.ajouter_joueur(dealer)

    def nouvelle_manche(self) -> None:
        """Lance une manche"""
        for indice_joueur in len(self.__joueurs):
            if self.__joueurs[indice_joueur].credit < self.__grosse_blind:
                self.retirer_joueur(indice_joueur)

        if len(self.__joueurs) < 2:
            raise Exception(
                f"Trop peu de joeuurs sur la table pour lancer une manche : {len(self.__joueurs)}"
            )

        self.__manche = Manche(info=InfoManche(self.__joueurs), grosse_blind=self.__grosse_blind)
        self.__manche.jouer()
        self.rotation_dealer()
