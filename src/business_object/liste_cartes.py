"""Implémentation de la classe AbstractListeCartes"""

from abc import ABC
from copy import deepcopy
from random import shuffle

from business_object.carte import Carte


class AbstractListeCartes(ABC):
    """Modélisation d'une liste de cartes provenant d'un jeu de cartes"""

    def __init__(self, cartes: list[Carte], complet):
        """
        Instanciation d'une liste de cartes

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes

        Renvois
        -------
        _ListeCartes
            Instance de '_ListeCartes'
        """

        if not isinstance(cartes, list) and cartes is not None:
            raise TypeError(f"cartes n'est pas list ou None : {type(cartes)}")

        # Vérifie que toutes les cartes de la liste sont de type 'Carte'
        if cartes is not None:
            for carte in cartes:
                if not isinstance(carte, Carte):
                    raise TypeError(
                        f"cartes ne doit contenir que des objet de type Carte : {type(carte)}"
                    )

        if cartes is None:
            self.__cartes = []

        if cartes is not None:
            self.__cartes = cartes

        # Créer un jeu de cartes complet
        if complet:
            self.__cartes = [
                Carte(valeur, couleur) for valeur in Carte.VALEURS() for couleur in Carte.COULEURS()
            ]

    @property
    def cartes(self) -> list:
        """Retourne une copie profonde de l'attribut 'cartes'"""
        return deepcopy(self.__cartes)

    def __str__(self) -> str:
        """Représentation informelle d'un objet de type _ListeCartes"""
        if len(self.__cartes) == 0:
            return "[]"

        texte = "["
        for carte in self.__cartes:
            texte += f"{carte}, "

        return texte[:-2] + "]"

    def __len__(self) -> int:
        """Renvoie le nombre de cartes dans l'attribut 'cartes'"""
        return len(self.__cartes)

    def __eq__(self, other) -> bool:
        """
        Compare l'égalité entre deux listes de cartes

        Paramètres
        ----------
        other : any
            objet comparée

        Renvois
        -------
        bool
            Vrai si l'ordre des cartes et les cartes sont identiques.
            Le type des deux objets doit aussi être identique.
        """

        if type(self) is not type(other):
            return False

        if len(self) != len(other):
            return False

        for carte in range(len(self)):
            if self.cartes[carte] != other.cartes[carte]:
                return False

        return True

    def ajouter_carte(self, carte: Carte) -> None:
        """
        Ajoute une carte dans la liste de cartes

        Paramètres
        ----------
        carte : Carte
            carte à ajouter à la liste de cartes
        """

        if not isinstance(carte, Carte):
            raise TypeError(f"l'objet à ajouter n'est pas de type Carte : {type(carte)}")

        self.__cartes.append(carte)

    def retirer_carte(self, indice: int = 0) -> Carte:
        """
        Retire une carte de la liste selon son indice

        Paramètres
        ----------
        indice : int
            Indice de la carte à retirer dans la liste de cartes

        Renvois
        -------
        Carte
            Retourne la carte retirée de la liste de cartes
        """

        if len(self) == 0:
            raise Exception("La liste de cartes est vide, aucune carte ne peut être retirée.")

        if not isinstance(indice, int):
            raise TypeError(f"L'indice renseigné n'est pas de type int : {type(indice)}")

        if not (0 <= indice < len(self)):
            raise ValueError(f"L'indice renseigné est trop grand : {indice}")

        return self.__cartes.pop(indice)

    def melanger(self):
        """Mélange l'ordre des cartes"""
        shuffle(self.__cartes)
