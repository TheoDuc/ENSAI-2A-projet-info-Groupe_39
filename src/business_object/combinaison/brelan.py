from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Brelan(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 3

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 3 for v in valeurs)

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Brelan":
        valeurs = [c.valeur for c in cartes]
        # On prend la valeur qui apparaît 3 fois comme hauteur
        hauteur = next(v for v in set(valeurs) if valeurs.count(v) == 3)
        kicker = tuple(
            sorted(
                [v for v in valeurs if v != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(hauteur, kicker)
