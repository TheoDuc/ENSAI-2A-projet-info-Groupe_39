from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Simple(AbstractCombinaison):
    """Classe représentant une combinaison 'Simple' (la carte la plus haute seule)."""

    def __init__(self, hauteur: str, kicker: tuple[str]):
        # Hauteur = carte la plus forte
        # Kicker = toutes les autres cartes triées par valeur décroissante
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        # Force minimale parmi toutes les combinaisons
        return 0

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        # Une Simple est toujours présente si la liste de cartes n'est pas vide
        return len(cartes) > 0

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Simple":
        """
        Crée une Simple à partir d'une liste de cartes :
        - Hauteur = la carte la plus forte
        - Kicker = toutes les autres cartes triées par valeur décroissante
        - Lève une erreur si la liste est vide
        """
        if not cartes:
            raise ValueError("Impossible de créer une Simple avec une liste vide")

        hauteur = max(cartes, key=lambda c: Carte.VALEURS().index(c.valeur)).valeur
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda v: Carte.VALEURS().index(v),
                reverse=True,
            )
        )
        return cls(hauteur, kicker)

    def __str__(self) -> str:
        # Représentation lisible pour le joueur
        # Exemple : "Simple As et Roi Dame 10"
        return f"Simple {self.hauteur}" + (f" et {' '.join(self.kicker)}" if self.kicker else "")

    def __repr__(self) -> str:
        # Représentation pour debug / tests, identique à __str__
        return str(self)
