"""Implémentation de la classe Main"""

from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes


class Main(AbstractListeCartes):
    """Modélisation de la main d'un joueur"""

    def __init__(self, cartes: list[Carte] = None, complet: bool = False):
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

        if cartes == "vide":
            cartes = []

        super().__init__(cartes, complet)

    def intervertir_cartes(self):
        """
        Inverse l'ordre des cartes dans la main

        Paramètres
        ----------
        None

        Renvois
        -------
        None

        """

        self.ajouter_carte(self.retirer_carte())
