"""Implémentation de la classe Reserve"""

from business_object.board import Board
from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes
from business_object.main import Main


class Reserve(AbstractListeCartes):
    """Modélisation de la reserve"""

    def __init__(self, cartes: list[Carte] = None):
        """
        Instanciation de la reserve de carte

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes

        Renvois
        -------
        Reserve
            Instance de 'Reserve'
        """

        super().__init__(cartes)

    def bruler(self):
        """
        Positionne la premiere carte du paquet en dernier

        Paramètres
        ----------
        None

        Renvois
        -------
        None
        """

        self.ajouter_carte(self.retirer_carte())

    def reveler(self, board):
        """
        Prend une carte de le reserve et la met dans le board

        Paramètres
        ----------
        board : Board
            Le board associé à la reserve

        Renvois
        -------
        None
        """

        if not isinstance(board, Board):
            raise ValueError(f"board pas de type Board : {type(board)}")

        board.ajouter_carte(self.retirer_carte())

    def distribuer(self, n_joueurs):
        """
        Distribue 2 cartes de la reserve dans la Main de chaque joueur

        Paramètres
        ----------
        n_joueur : int
            Le nombre de mains à créer

        Renvois
        -------
        list[Main]
            Une liste de mains
        """

        # Vérification qu'il y a assez de cartes à distribuer
        if len(self.cartes) < n_joueurs * 2:
            raise ValueError(
                f"le nombre de carte dans la reserve est trop petit : {len(self.cartes)}"
            )

        distribution = [[] for i in range(n_joueurs)]

        # Distribution des cartes dans des listes
        for _ in range(0, 2):
            for joueur in range(0, n_joueurs):
                carte = self.retirer_carte()
                distribution[joueur].append(carte)

        # Converson des listes de cartes en mains
        for main in range(len(distribution)):
            distribution[main] = Main(distribution[main])

        return distribution
