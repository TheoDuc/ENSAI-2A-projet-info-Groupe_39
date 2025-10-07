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
        AbstractListeCartes.__init__(self, cartes)

    def bruler(self):
        """
        Positionne la premiere carte du paquet en dernier

        Renvois
        -------
        Reserve
            Instance de 'Reserve'
        """
        carte_bruler = self.retirer_carte()
        self.ajouter_carte(carte_bruler)

    def reveler(self, board):
        """
        Prend une carte de le reserve et la met dans le board

        Paramètres
        ----------
        board : Board
            le board associé à la reserve

        Renvois
        -------
        Reserve
            Instance de 'Reserve'
        Board
            Instance de 'Board'
        """
        if not isinstance(board, Board):
            raise ValueError(f"board pas de type Board : {type(board)}")
        carte_reveler = self.retirer_carte()
        board.ajouter_carte(carte_reveler)
        
    def distribuer(self, n_joueurs):
        """
        Distribue 2 carte de la reserve dans la Main de chaque joueur

        Paramètres
        ----------
        n_joueur : int
            le nombre de Main à créer

        Renvois
        -------
        Reserve
            Instance de 'Reserve'
        mains
            une liste de Main
        """
        distribution = [[] for i in range(n_joueurs)]
        if len(self.cartes) < n_joueurs * 2:
            raise ValueError(
                f"le nombre de carte dans la reserve est trop petit: {len(self.cartes)}"
            )
        for k in range(0, 2):
            for i in range(0, n_joueurs):
                new = self.retirer_carte()
                distribution[i].append(new)
        for i in range(len(distribution)):
            distribution[i] = Main(distribution[i])
        return distribution
