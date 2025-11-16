"""Implémentation de la classe InfoManche"""

from business_object.joueur import Joueur
from business_object.main import Main


class InfoManche:
    """
    Stocke toutes les informations relatives à une manche de poker,
    y compris les joueurs, leurs mains, leurs mises et leur état (couché ou actif).
    """

    __STATUTS = ("innactif", "en retard", "à jour", "couché", "all in")

    def __init__(self, joueurs: list[Joueur]):
        """
        Instanciation d'une info de manche.

        Paramètres
        ----------
        joueurs : list[Joueur]
            Liste des joueurs participant à la manche.

        Exceptions
        ----------
        TypeError
            Si joueurs n'est pas une liste de Joueur
        ValueError
            Si la liste des joueurs est vide
        """

        if not isinstance(joueurs, list):
            raise TypeError(
                f"Le paramètre 'joueurs' doit être une liste, pas {type(joueurs).__name__}"
            )

        if not all(isinstance(j, Joueur) for j in joueurs):
            raise TypeError("Tous les éléments de 'joueurs' doivent être des instances de Joueur")

        if len(joueurs) < 2:
            raise ValueError(
                f"Au moins deux joueurs doivent être présents : {len(joueurs)} présents"
            )

        self.__joueurs = joueurs
        self.__statuts = [0 for _ in joueurs]
        self.__mains = [None for _ in joueurs]
        self.__mises = [0 for _ in joueurs]
        self.__tour_couche = [None for _ in joueurs]

    @property
    def joueurs(self) -> list[Joueur]:
        """Liste des joueurs participant à la manche"""
        return self.__joueurs

    @property
    def statuts(self) -> list[int]:
        """Liste des joueurs participant à la manche"""
        return self.__statuts

    @property
    def mains(self) -> list[Main]:
        """Liste des mains de chaque joueur"""
        return self.__mains

    @property
    def mises(self) -> list[int]:
        """Liste des mises actuelles de chaque joueur"""
        return self.__mises

    @property
    def tour_couche(self) -> list[int]:
        """État des joueurs : None pour actif, True pour couché"""
        return self.__tour_couche

    def __str__(self):
        """Représentation informelle d'un objet de type InfoManche"""
        return (
            f"InfoManche(joueurs={self.joueurs}, "
            f"statuts={self.statuts}, "
            f"mains={self.mains}, "
            f"mises={self.mises}, "
            f"tour_couche={self.tour_couche})"
        )

    def modifier_statut(self, indice_joueur, statut: int):
        """Modifie le statut d'un joueur par son indice"""
        self.__statuts[indice_joueur] = statut

    def modifier_mise(self, indice_joueur, nouveau_montant: int):
        """Modifie la mise d'un joueur par son indice"""
        self.__mises[indice_joueur] = nouveau_montant

    def modifier_tour_couche(self, indice_joueur, tour: int):
        """Modifie la mise d'un joueur par son indice"""
        self.__tour_couche[indice_joueur] = tour

    def assignation_mains(self, mains: list[Main]):
        """
        Assigne les mains distribuées aux joueurs.

        Paramètres
        ----------
        mains : list[Main]
            Liste des mains distribuées
        """

        if not isinstance(mains, list) or not all(isinstance(m, Main) for m in mains):
            raise TypeError("Le paramètre 'mains' doit être une liste de Main")

        if len(mains) != len(self.joueurs):
            raise ValueError("Le nombre de mains doit correspondre au nombre de joueurs")

        self.__mains = mains
