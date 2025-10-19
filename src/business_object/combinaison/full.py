from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Full(AbstractCombinaison):
    """Classe représentant un Full (Brelan + Paire) au poker."""

    def __init__(self, hauteur: str, kicker=None):
        # Hauteur = valeur du brelan, kicker = paire
        super().__init__(hauteur, kicker)

    # Force relative du Full dans le classement des combinaisons
    @classmethod
    def FORCE(cls) -> int:
        return 6

    # Vérifie si un Full est présent dans la main
    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        valeurs = [c.valeur for c in cartes]
        # Cherche les brelans et paires
        brelans = [v for v in set(valeurs) if valeurs.count(v) >= 3]
        paires = [v for v in set(valeurs) if valeurs.count(v) >= 2 and v not in brelans]
        # True si au moins un brelan et une paire
        return bool(brelans and paires)

    # Construit un objet Full à partir d’une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Full":
        valeurs = [c.valeur for c in cartes]
        # On prend le brelan le plus fort
        brelan = max(
            [v for v in set(valeurs) if valeurs.count(v) >= 3],
            key=lambda x: Carte.VALEURS().index(x),
        )
        # On prend la paire la plus forte différente du brelan
        paire = max(
            [v for v in set(valeurs) if valeurs.count(v) >= 2 and v != brelan],
            key=lambda x: Carte.VALEURS().index(x),
        )
        # kicker = tuple contenant la paire
        return cls(brelan, (paire,))

    # Représentation lisible pour le joueur de poker
    def __str__(self):
        # Exemple : "Full As et Roi"
        return f"Full {self.hauteur} et {self.kicker[0]}"

    # Représentation technique pour debug / tests
    def __repr__(self):
        # Ici, on utilise simplement la même chaîne que __str__
        return str(self)
