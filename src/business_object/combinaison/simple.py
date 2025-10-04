from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Simple(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 0

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        # Une "Simple" est toujours présente si aucune combinaison supérieure n'est trouvée
        return len(cartes) > 0

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Simple":
        # La "Simple" prend la carte la plus haute
        hauteur = max(cartes, key=lambda c: Carte.VALEURS().index(c.valeur)).valeur
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda v: Carte.VALEURS().index(v),
                reverse=True,
            )
        )
        return cls(hauteur, kicker)
