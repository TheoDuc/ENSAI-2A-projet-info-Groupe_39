from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class QuinteFlush(AbstractCombinaison):
    def __init__(self, hauteur: str, kicker=None):
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        return 8

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        # Vérifie s'il y a une quinte flush parmi les cartes
        if len(cartes) < 5:
            return False
        couleurs = [c.couleur for c in cartes]
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            valeurs_indices = sorted([Carte.VALEURS().index(c.valeur) for c in cartes_couleur])
            for i in range(len(valeurs_indices) - 4):
                if valeurs_indices[i + 4] - valeurs_indices[i] == 4:
                    return True
        return False

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "QuinteFlush":
        couleurs = [c.couleur for c in cartes]
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            valeurs_indices = sorted(
                [Carte.VALEURS().index(c.valeur) for c in cartes_couleur], reverse=True
            )
            for i in range(len(valeurs_indices) - 4):
                if valeurs_indices[i] - valeurs_indices[i + 4] == 4:
                    hauteur = Carte.VALEURS()[valeurs_indices[i]]
                    return cls(hauteur)
        raise ValueError("Pas de quinte flush dans ces cartes")
