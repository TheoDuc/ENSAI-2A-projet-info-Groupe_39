from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class QuinteFlush(AbstractCombinaison):
    """Classe représentant une Quinte Flush (suite de 5 cartes de même couleur)."""

    def __init__(self, hauteur: str, kicker=None):
        # Hauteur = carte la plus forte de la quinte flush
        super().__init__(hauteur, kicker)

    # Force relative de la Quinte Flush dans le classement poker
    @classmethod
    def FORCE(cls) -> int:
        return 8

    # Vérifie si une Quinte Flush est présente
    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        if len(cartes) < 5:
            return False  # Impossible d'avoir une quinte flush avec moins de 5 cartes

        couleurs = [c.couleur for c in cartes]
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            # On récupère les indices des valeurs triés
            indices = sorted([Carte.VALEURS().index(c.valeur) for c in cartes_couleur])
            # Vérifie toutes les suites de 5 cartes
            for i in range(len(indices) - 4):
                if indices[i + 4] - indices[i] == 4:
                    return True
        return False

    # Construit un objet Quinte Flush à partir de cartes
    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "QuinteFlush":
        couleurs = [c.couleur for c in cartes]
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            # Indices triés décroissants pour prendre la plus haute
            indices = sorted(
                [Carte.VALEURS().index(c.valeur) for c in cartes_couleur], reverse=True
            )
            # Cherche une suite de 5 cartes consécutives
            for i in range(len(indices) - 4):
                if indices[i] - indices[i + 4] == 4:
                    hauteur = Carte.VALEURS()[indices[i]]
                    return cls(hauteur)
        # Si aucune quinte flush trouvée
        raise ValueError("Pas de quinte flush dans ces cartes")

    # Représentation lisible pour le joueur
    def __str__(self) -> str:
        # Exemple : "Quinte Flush As"
        return f"Quinte Flush {self.hauteur}"

    # Représentation pour debug / tests
    def __repr__(self) -> str:
        return str(self)
