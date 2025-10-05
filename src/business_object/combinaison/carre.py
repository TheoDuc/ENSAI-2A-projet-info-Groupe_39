from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Carre(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 7

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 4 for v in valeurs)

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Carre":
        valeurs = [c.valeur for c in cartes]
        hauteur = next(v for v in set(valeurs) if valeurs.count(v) == 4)
        kicker = tuple(
            sorted(
                [v for v in valeurs if v != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(hauteur, kicker)
