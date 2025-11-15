"""Implémentation de la classe Main"""

from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes


class Main(AbstractListeCartes):
    """Modélisation de la main d'un joueur"""

    def __init__(self, cartes: list[Carte] = []):
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
            raise ValueError(f"Le nombre de cartes dans la main est trop grand : {len(cartes)}")

        else:
            super().__init__(cartes)

        # Ajout dans Main

    def ajouter_carte(self, carte: Carte):
        """
        Ajoute une carte dans la main. Et vérifie que le nombre de cartes reste en dessous de 2

        Paramètres
        ----------
        carte : Carte
            carte à ajouter à la main
        """

        if carte is not None and len(self.cartes) > 1:
            raise ValueError(
                f"Le nombre de cartes dans la main est trop grand : {len(self.cartes) + 1}"
            )
        else:
            self.ajouter_carte_base(carte)

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
