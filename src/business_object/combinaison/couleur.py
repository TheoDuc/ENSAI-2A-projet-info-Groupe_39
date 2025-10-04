from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Couleur(AbstractCombinaison):
    def __init__(self, hauteur: str, kicker=None):
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        return 5

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        couleurs = [c.couleur for c in cartes]
        return any(couleurs.count(c) >= 5 for c in set(couleurs))

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Couleur":
        # On prend la couleur la plus fréquente avec au moins 5 cartes
        couleurs = [c.couleur for c in cartes]
        couleur_max = max(set(couleurs), key=couleurs.count)
        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
        # Hauteur = carte la plus forte de cette couleur
        hauteur = max(cartes_couleur)
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes_couleur if c.valeur != hauteur.valeur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(hauteur.valeur, kicker)
