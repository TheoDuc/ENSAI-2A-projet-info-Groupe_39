"""Implémentation de la classe InfoManche"""

from business_object.joueur import Joueur
from business_object.main import Main
from utils.log_decorator import log


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
        # Vérifications
        if not isinstance(joueurs, list):
            raise TypeError(
                f"Le paramètre 'joueurs' doit être une liste, pas {type(joueurs).__name__}."
            )
        if not all(isinstance(j, Joueur) for j in joueurs):
            raise TypeError("Tous les éléments de 'joueurs' doivent être des instances de Joueur.")
        if len(joueurs) < 2:
            raise ValueError(
                f"Au moins deux joueurs doivent être présents : {len(joueurs)} présents"
            )

        # Initialisation des attributs privés
        self.__joueurs = joueurs
        self.__statuts = [0 for _ in joueurs]
        self.__mains = [None for _ in joueurs]
        self.__mises = [0 for _ in joueurs]
        self.__tour_couche = [None for _ in joueurs]

    # Propriétés
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

    # Méthodes d'instance

    def changer_statut(self, indice_joueur, statut : int):
        self.__statuts[indice_joueur] = statut

    def assignation_mains(self, mains: list[Main]):
        """
        Assigne les mains distribuées aux joueurs.

        Paramètres
        ----------
        mains : list[Main]
            Liste des mains distribuées
        """
        if not isinstance(mains, list) or not all(isinstance(m, Main) for m in mains):
            raise TypeError("Le paramètre 'mains' doit être une liste de Main.")
        if len(mains) != len(self.joueurs):
            raise ValueError("Le nombre de mains doit correspondre au nombre de joueurs.")

        self.__mains = mains

    @log
    def suivre(self, indice_joueur: int, relance : int = 0):
        """
        Ajoute une mise pour un joueur.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste
        montant : int
            Montant à miser
        """
        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")
        if not isinstance(relance, int) or montant < 0:
            raise ValueError("Le montant doit être un entier positif")
        suivre_montant = max(self.mises)
        if suivre_montant >= self.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur doit all-in.")
        if relance + suivre_montant >= self.joueurs[indice_joueur].credit:
            raise ValueError("Le joueur ne peut relancer autant.")
        else:
            pour_suivre = suivre_montant - self.mises[indice_joueur]
            self.mises[indice_joueur] += pour_suivre
            self.statuts[indice_joueur] = 2
        if relance > 0:
            self.mises[indice_joueur] += relance
            for i in range(len(self.statuts)):
                if self.statuts[i] == 2:
                    self.statuts[i] = 1
        return pour_suivre + relance

    @log
    def coucher_joueur(self, indice_joueur: int, tour: int):
        """
        Marque un joueur comme couché.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste
        """
        self.__tour_couche[indice_joueur] = tour
        self.__statuts[indice_joueur] = 3

    # Représentation
    def __str__(self):
        return (
            f"InfoManche(joueurs={self.joueurs}, "
            f"statuts={self.statuts}, "
            f"mains={self.mains}, "
            f"mises={self.mises}, "
            f"tour_couche={self.tour_couche})"
        )
