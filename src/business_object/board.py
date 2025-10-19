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
