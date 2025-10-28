"""Implémentation de la classe InfoManche"""

from business_object.joueur import Joueur
from business_object.main import Main


class InfoManche:
    """
    Stocke toutes les informations relatives à une manche de poker,
    y compris les joueurs, leurs mains, leurs mises et leur état (couché ou actif).
    """

    STATUTS = ("innactif", "en retard", "à jour", "couché", "all in")

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
        # --- Vérifications ---
        if not isinstance(joueurs, list):
            raise TypeError(
                f"Le paramètre 'joueurs' doit être une liste, pas {type(joueurs).__name__}."
            )
        if not all(isinstance(j, Joueur) for j in joueurs):
            raise TypeError("Tous les éléments de 'joueurs' doivent être des instances de Joueur.")
        if len(joueurs) < 2:
            raise ValueError(f"Au moins deux joueurs doivent être présents : {len(joueurs)}")

        # --- Initialisation des attributs privés ---
        self.__joueurs = joueurs
        self.__statuts = [0 for _ in joueurs]
        self.__mains = [None for _ in joueurs]
        self.__mises = [0 for _ in joueurs]
        self.__tour_couche = [
            None for _ in joueurs
        ]  # None = actif, Entier = couché mais bon le diagramme de classe ne permet pas dans InfoManche de savoir à quel tour on est en fait cet attribut est à visée DAO mais ça ne va pas être possible uniquement via InfoManche pareil pour le gain en attendant juste le statut couché sera indiqué

    # -------------------- Propriétés -------------------- #
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
    def tour_couche(self) -> list:
        """État des joueurs : None pour actif, True pour couché"""
        return self.__tour_couche

    # -------------------- Méthodes d'instance -------------------- #
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

    def miser(self, indice_joueur: int, montant: int):
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
        if not isinstance(montant, (int, float)) or montant <= 0:
            raise ValueError("Le montant doit être un entier strictement positif")
        if self.joueurs[indice_joueur].credit > self.mises[indice_joueur] + montant:
            self.__mises[indice_joueur] += montant
            self.__statuts[indice_joueur] = "à jour"
        if self.joueurs[indice_joueur].credit <= self.mises[indice_joueur] + montant:
            self.__mises[indice_joueur] = self.joueurs[indice_joueur].credit
            self.__statuts[indice_joueur] == "all in"

    def coucher_joueur(self, indice_joueur: int):
        """
        Marque un joueur comme couché.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste
        """
        self.__tour_couche[indice_joueur] = True
        self.__statuts[indice_joueur] == "couché"

    # -------------------- Représentation -------------------- #
    def __str__(self):
        return (
            f"InfoManche(joueurs={self.joueurs}, "
            f"statuts={self.statuts}, "
            f"mains={self.mains}, "
            f"mises={self.mises}, "
            f"tour_couche={self.tour_couche})"
        )
