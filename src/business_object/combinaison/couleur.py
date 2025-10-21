from typing import List, Optional

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Couleur(AbstractCombinaison):
    """Classe représentant une combinaison Couleur (Flush) au poker."""

    def __init__(
        self,
        hauteur: str,
        cartes: Optional[List[Carte]] = None,
    ):
        """
        Initialisation d'une Couleur.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute dans la couleur
        cartes : list[Carte], optionnel
            Liste des cartes exactes de la couleur
        """

        super().__init__(hauteur, kicker=None)
        self.cartes = cartes or []

    # Force relative de la combinaison Couleur
    @classmethod
    def FORCE(cls) -> int:
        return 5

    # Vérifie si une Couleur (Flush) est présente
    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        couleurs = [c.couleur for c in cartes]
        return any(couleurs.count(c) >= 5 for c in set(couleurs))

    # Crée un objet Couleur à partir d’une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Couleur":
        couleurs = [c.couleur for c in cartes]
        couleur_max = next((c for c in set(couleurs) if couleurs.count(c) >= 5), None)

        if couleur_max is None:
            raise ValueError("Aucune Couleur présente dans les cartes")

        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
        hauteur = max(cartes_couleur, key=lambda c: Carte.VALEURS().index(c.valeur))

        # kicker calculé automatiquement
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes_couleur if c.valeur != hauteur.valeur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )

        # retourne la combinaison avec le kicker calculé
        return cls(hauteur.valeur, cartes_couleur)

    def __str__(self) -> str:
        return f"Couleur de {self.hauteur}"

    def __repr__(self) -> str:
        cartes_str = ", ".join(f"{c.valeur} de {c.couleur}" for c in self.cartes)
        return f"Couleur([{cartes_str}])"
