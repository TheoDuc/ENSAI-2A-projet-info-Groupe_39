from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class DoublePaire(AbstractCombinaison):
    def __init__(self, hauteur: str, kicker: tuple[str]):
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        return 2

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        return len([v for v in set(valeurs) if valeurs.count(v) >= 2]) >= 2

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "DoublePaire":
        valeurs = [c.valeur for c in cartes]
        paires = sorted(
            [v for v in set(valeurs) if valeurs.count(v) >= 2],
            key=lambda x: Carte.VALEURS().index(x),
            reverse=True,
        )
        kicker = tuple(
            sorted(
                [v for v in valeurs if v not in paires],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(
            paires[0], (paires[1], *kicker[:1])
        )  # kicker = deuxième paire + plus fort kicker
