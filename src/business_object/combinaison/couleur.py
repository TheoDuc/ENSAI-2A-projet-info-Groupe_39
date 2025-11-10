from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Couleur(AbstractCombinaison):
    """
    Classe représentant une combinaison de type *Couleur* (Flush) au poker.

    Une couleur est composée de cinq cartes (ou plus) de la même couleur,
    sans considération d'ordre. La force de la combinaison est déterminée
    par la carte la plus haute, puis par les kickers éventuels.
    """

    def __init__(self, hauteur: tuple[str]) -> None:
        """
        Initialise une combinaison Couleur.

        Paramètres
        ----------
        hauteur : tuple[str]
            Valeur de la carte la plus haute de la couleur .
        kicker: None
        """
        super().__init__(hauteur, kicker=None)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison *Couleur*.

        Renvois
        -------
        int
            Valeur entière représentant la force de la combinaison.

        """
        return 5

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si une *Couleur* (Flush) est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte représentant la main à évaluer.

        Renvois
        -------
        bool
            True si au moins cinq cartes partagent la même couleur, False sinon.



        """
        couleurs = [c.couleur for c in cartes]
        return any(couleurs.count(c) >= 5 for c in set(couleurs))

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Couleur":
        """
        Construit une instance de Couleur à partir d’une liste de cartes.

        Recherche automatiquement la couleur majoritaire (présente au moins 5 fois)
        et détermine la carte la plus haute ainsi que les kickers correspondants.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à partir desquelles on veut créer la combinaison.

        Renvois
        -------
        Couleur
            Instance de la classe Couleur correspondant à la meilleure couleur trouvée.

        Exceptions
        ----------
        ValueError
            Si aucune couleur valide (au moins cinq cartes identiques en couleur) n’est trouvée.


        """
        cls.verifier_min_cartes(cartes)
        couleurs = [c.couleur for c in cartes]
        couleur_max = next((c for c in set(couleurs) if couleurs.count(c) >= 5), None)

        if couleur_max is None:
            raise ValueError("Aucune Couleur présente dans les cartes")

        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
        cartes_couleur.sort(key=lambda c: Carte.VALEURS().index(c.valeur), reverse=True)
        hauteur = [c.valeur for c in cartes_couleur[:5]]
        return cls(hauteur)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la *Couleur*.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne lisible par un joueur, par exemple : "Couleur de As".
        """
        return "Couleur"

    def __repr__(self) -> str:
        """
        Renvoie une représentation détaillée de la *Couleur* pour le débogage.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne descriptive incluant toutes les cartes formant la couleur,
            par exemple : "Couleur([As de cœur, Roi de cœur, Dame de cœur, Valet de cœur, 9 de cœur])".
        """

        return f"Couleur(hauteur={self.hauteur})"
