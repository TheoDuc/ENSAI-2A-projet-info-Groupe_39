from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Full(AbstractCombinaison):
    def __init__(self, hauteur: str, kicker=None):
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        return 6

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        brelans = [v for v in set(valeurs) if valeurs.count(v) >= 3]
        paires = [v for v in set(valeurs) if valeurs.count(v) >= 2 and v not in brelans]
        return bool(brelans and paires)

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Full":
        valeurs = [c.valeur for c in cartes]
        brelan = max(
            [v for v in set(valeurs) if valeurs.count(v) >= 3],
            key=lambda x: Carte.VALEURS().index(x),
        )
        paire = max(
            [v for v in set(valeurs) if valeurs.count(v) >= 2 and v != brelan],
            key=lambda x: Carte.VALEURS().index(x),
        )
        return cls(brelan, (paire,))
