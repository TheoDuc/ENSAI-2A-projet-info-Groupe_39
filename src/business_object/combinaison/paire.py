from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Paire(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 1

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 2 for v in set(valeurs))

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Paire":
        valeurs = [c.valeur for c in cartes]
        paire = max(
            [v for v in set(valeurs) if valeurs.count(v) == 2],
            key=lambda x: Carte.VALEURS().index(x),
        )
        kicker = tuple(
            sorted(
                [v for v in valeurs if v != paire],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(paire, kicker)
