from typing import List, Optional, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Couleur(AbstractCombinaison):
    """Classe représentant une combinaison Couleur (Flush) au poker."""

    def __init__(
        self,
        hauteur: str,
        kicker: Optional[Tuple[str, ...]] = None,
        cartes: Optional[List[Carte]] = None,
    ):
        """
        Initialisation d'une Couleur.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute dans la couleur
        kicker : tuple, optionnel
            Les autres cartes de la couleur triées par valeur décroissante
        cartes : list[Carte], optionnel
            Liste des cartes exactes de la couleur
        """
        # Appel du constructeur parent
        super().__init__(hauteur, kicker)
        # Stocke les cartes de la couleur, ou une liste vide si non fournies
        self.cartes = cartes or []

    # Force relative de la combinaison Couleur
    @classmethod
    def FORCE(cls) -> int:
        return 5

    # Vérifie si une Couleur (Flush) est présente
    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        couleurs = [c.couleur for c in cartes]
        # True si au moins 5 cartes de la même couleur
        return any(couleurs.count(c) >= 5 for c in set(couleurs))

    # Crée un objet Couleur à partir d’une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Couleur":
        # Recherche la couleur ayant au moins 5 cartes
        couleurs = [c.couleur for c in cartes]
        couleur_max = None
        for c in set(couleurs):
            if couleurs.count(c) >= 5:
                couleur_max = c
                break

        # Si aucune couleur avec 5 cartes n’est trouvée, on lève une erreur
        if couleur_max is None:
            raise ValueError("Aucune Couleur présente dans les cartes")

        # On garde toutes les cartes de cette couleur
        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]

        # Hauteur = carte la plus forte de cette couleur
        hauteur = max(cartes_couleur)

        # Kicker = les autres cartes de cette couleur triées par valeur décroissante
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes_couleur if c.valeur != hauteur.valeur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )

        # Retourne la combinaison construite
        return cls(hauteur.valeur, kicker, cartes_couleur)

    # Représentation lisible pour un joueur de poker
    def __str__(self) -> str:
        return f"Couleur de {self.hauteur}"  # Exemple : "Couleur de As"

    # Représentation technique pour le débogage
    def __repr__(self) -> str:
        cartes_str = ", ".join(f"{c.valeur} de {c.couleur}" for c in self.cartes)
        return f"Couleur([{cartes_str}])"  # Exemple : "Couleur([As de Coeur, 10 de Coeur, ...])"
