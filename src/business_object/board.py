"""Implémentation de la classe Board"""

from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes


class Board(AbstractListeCartes):
    """Modélisation du board de poker"""

    def __init__(self, cartes: list[Carte] = []):
        """
        Instanciation d'un board

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes

        Renvois
        -------
        Board
            Instance de 'Board'
        """

        if cartes is not None and len(cartes) > 5:
            raise ValueError(f"Le nombre de cartes dans le board est trop grand : {len(cartes)}")

        else:
            super().__init__(cartes)

    def ajouter_carte(self, carte: Carte):
        """
        Ajoute une carte dans le board. Et vérifie que le nombre de cartes reste en dessous de 5

        Paramètres
        ----------
        carte : Carte
            carte à ajouter au board
        """
        if carte is not None and len(self.cartes) > 4:
            raise ValueError(
                f"Le nombre de cartes dans le board est trop grand : {len(self.cartes) + 1}"
            )
        else:
            self.ajouter_carte_base(carte)
