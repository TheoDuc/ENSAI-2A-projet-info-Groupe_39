from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Paire(AbstractCombinaison):
    """Classe représentant une Paire (deux cartes de même valeur) au poker."""

    def __init__(self, hauteur: str, kicker: tuple[str, ...]):
        # Initialisation via le constructeur parent : hauteur de la plus forte paire et kicker
        super().__init__(hauteur, kicker)

    # Force relative d'une Paire dans le classement des combinaisons
    @classmethod
    def FORCE(cls) -> int:
        return 1

    # Vérifie si une Paire est présente dans la main
    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        # True si au moins une valeur apparaît exactement deux fois
        return any(valeurs.count(v) == 2 for v in set(valeurs))

    # Construit un objet Paire à partir d'une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Paire":
        valeurs = [c.valeur for c in cartes]

        # Recherche la paire la plus forte
        paire = max(
            [v for v in set(valeurs) if valeurs.count(v) == 2],
            key=lambda x: Carte.VALEURS().index(x),
        )

        # Les kickers = cartes restantes triées par valeur décroissante
        kicker = tuple(
            sorted(
                [v for v in valeurs if v != paire],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )

        return cls(paire, kicker)

    # Représentation lisible pour un joueur de poker
    def __str__(self):
        # Exemple : "Paire As et Roi" si kicker, sinon "Paire As"
        return (
            f"Paire {self.hauteur} et {self.kicker[0]}" if self.kicker else f"Paire {self.hauteur}"
        )

    def __repr__(self):
        return str(self)
