from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Quinte(AbstractCombinaison):
    def __init__(self, hauteur: str, kicker=None):
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        return 4

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        # Vérifie s'il y a une quinte parmi les cartes
        valeurs_indices = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        for i in range(len(valeurs_indices) - 4):
            if valeurs_indices[i + 4] - valeurs_indices[i] == 4:
                return True
        return False

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Quinte":
        valeurs_indices = sorted({Carte.VALEURS().index(c.valeur) for c in cartes}, reverse=True)
        for i in range(len(valeurs_indices) - 4):
            if valeurs_indices[i] - valeurs_indices[i + 4] == 4:
                hauteur = Carte.VALEURS()[valeurs_indices[i]]
                return cls(hauteur)
        raise ValueError("Pas de quinte dans ces cartes")
