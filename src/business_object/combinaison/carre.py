from typing import List, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Carre(AbstractCombinaison):
    """Classe représentant un Carré (quatre cartes de même valeur)."""

    def __init__(self, cartes: List[Carte], kicker: Tuple[str, ...] = ()):
        # Vérifie que exactement 4 cartes sont fournies
        if len(cartes) != 4:
            raise ValueError("Un Carré doit être constitué de 4 cartes")
        # Hauteur du carré = valeur des cartes
        hauteur = cartes[0].valeur
        # Vérifie que toutes les cartes ont la même valeur
        if not all(c.valeur == hauteur for c in cartes):
            raise ValueError("Toutes les cartes doivent avoir la même valeur pour un Carré")
        # Appel du constructeur parent pour initialiser hauteur et kicker
        super().__init__(hauteur, kicker)
        # Stocke les cartes réelles pour __repr__ et __str__
        self.cartes = cartes

    # Force relative du Carré dans le classement des combinaisons
    @classmethod
    def FORCE(cls) -> int:
        return 7

    # Vérifie si un Carré est présent dans une liste de cartes
    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 4 for v in set(valeurs))

    # Crée un objet Carre à partir d’une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Carre":
        valeurs = [c.valeur for c in cartes]
        # Recherche la valeur qui apparaît 4 fois
        try:
            hauteur = next(v for v in set(valeurs) if valeurs.count(v) == 4)
        except StopIteration:
            raise ValueError("Aucun Carré présent dans les cartes")
        # Sélectionne les cartes du carré
        carre_cartes = [c for c in cartes if c.valeur == hauteur]
        # Les cartes restantes deviennent les kickers, triées de la plus forte à la plus faible
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        # Retourne le Carré construit
        return cls(carre_cartes, kicker)

    # Représentation lisible pour un joueur
    def __str__(self) -> str:
        return f"Carre de {self.hauteur}"  # Exemple : "Carre de Roi"

    # Représentation technique pour le développeur / debug
    def __repr__(self) -> str:
        cartes_str = ", ".join(f"{c.valeur} de {c.couleur}" for c in self.cartes)
        return f"Carre([{cartes_str}])"  # Exemple : "Carre([Roi de Coeur, Roi de Pique, ...])"
