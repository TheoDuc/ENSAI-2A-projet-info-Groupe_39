"""Implémentation de la classe Main"""

from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes


class Main(AbstractListeCartes):
    """Modélisation de la main d'un joueur"""

    def __init__(self, cartes: list[Carte]):
        """
        Instanciation d'une main

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes

        Renvois
        -------
        Main
            Instance de 'Main'
        """

        if cartes is not None and len(cartes) > 2:
            raise ValueError(f"Le nombre de carte dans la main est trop grand : {len(cartes)}")

        # elif cartes is None:
        # AbstractListeCartes.cartes = []

        else:
            AbstractListeCartes.__init__(self, cartes)

    def intervertir_cartes(self):
        """
        Renvoie une main avec un ordre opposé que le premier

        Renvois
        -------
        Main
            Instance de 'Main'

        """
        carte1 = self.cartes[0]
        carte2 = self.cartes[1]
        return Main([carte2, carte1])
