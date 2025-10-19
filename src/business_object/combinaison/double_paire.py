from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class DoublePaire(AbstractCombinaison):
    """Classe représentant une Double Paire (deux paires de cartes de même valeur)."""

    def __init__(self, hauteur: str, kicker: tuple[str, ...]):
        # Initialisation via le constructeur parent : hauteur de la plus forte paire et kicker
        super().__init__(hauteur, kicker)

    # Force relative de la Double Paire dans le classement des combinaisons
    @classmethod
    def FORCE(cls) -> int:
        return 2

    # Vérifie si une Double Paire est présente dans une liste de cartes
    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        # True si au moins 2 valeurs apparaissent au moins deux fois
        return len([v for v in set(valeurs) if valeurs.count(v) >= 2]) >= 2

    # Construit un objet Double Paire à partir d’une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "DoublePaire":
        valeurs = [c.valeur for c in cartes]

        # Recherche toutes les valeurs apparaissant au moins deux fois
        paires = sorted(
            [v for v in set(valeurs) if valeurs.count(v) >= 2],
            key=lambda x: Carte.VALEURS().index(x),
            reverse=True,  # La paire la plus forte en premier
        )

        # Si moins de 2 paires, on ne peut pas construire la combinaison
        if len(paires) < 2:
            raise ValueError("Pas assez de paires pour créer une Double Paire")

        # Cartes restantes servant de kicker
        kickers = [v for v in valeurs if v not in paires]
        # kicker = deuxième paire + la carte la plus forte restante
        kicker = (
            paires[1],
            *sorted(kickers, key=lambda x: Carte.VALEURS().index(x), reverse=True)[:1],
        )

        return cls(paires[0], kicker)

    # Représentation lisible pour un joueur
    def __str__(self):
        return f"Double Paire {self.hauteur} et {self.kicker[0]}"  # Exemple : "Double Paire Roi et Dame"

    # Représentation technique pour debug / tests
    def __repr__(self) -> str:
        kicker_str = ", ".join(self.kicker)
        return f"DoublePaire(hauteur={self.hauteur}, kicker=({kicker_str}))"
