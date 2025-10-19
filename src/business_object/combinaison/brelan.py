# On importe Counter pour compter facilement les occurrences de chaque valeur de carte
from collections import Counter

# On importe la classe Carte qui représente une carte individuelle
from business_object.carte import Carte

# On importe AbstractCombinaison, classe parente pour toutes les combinaisons de poker
from business_object.combinaison.combinaison import AbstractCombinaison


class Brelan(AbstractCombinaison):
    """Représente un Brelan (trois cartes de même valeur)."""

    # Constructeur de la classe
    def __init__(self, hauteur: str, cartes: list[Carte], kicker=None):
        # Appel du constructeur de la classe parente pour initialiser hauteur et kicker
        super().__init__(hauteur, kicker)
        # Stocke la liste complète des cartes de la main
        self.cartes = cartes

    # Méthode de classe pour connaître la force relative d’un Brelan
    @classmethod
    def FORCE(cls) -> int:
        return 4  # 4 indique que le Brelan est une combinaison plus forte qu’une paire mais moins qu’un carré

    # Méthode pour vérifier si un Brelan est présent parmi les cartes données
    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """Vérifie s’il existe trois cartes de même valeur."""
        # On récupère uniquement les valeurs des cartes
        valeurs = [c.valeur for c in cartes]
        # On regarde si au moins une valeur apparaît exactement 3 fois
        return any(valeurs.count(v) == 3 for v in set(valeurs))

    # Méthode pour créer un objet Brelan à partir d’une liste de cartes
    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Brelan":
        """Construit un Brelan à partir d’une liste de cartes."""
        # On récupère les valeurs de toutes les cartes
        valeurs = [c.valeur for c in cartes]
        # On compte combien de fois chaque valeur apparaît
        compteur = Counter(valeurs)

        # On sélectionne les valeurs qui apparaissent au moins 3 fois (candidats Brelan)
        brelans = [v for v, count in compteur.items() if count >= 3]
        # Si aucune valeur n’a trois occurrences, on lève une erreur
        if not brelans:
            raise ValueError("Aucun brelan présent dans les cartes")

        # On prend la valeur la plus haute pour constituer le Brelan
        hauteur = max(brelans, key=lambda v: Carte.VALEURS().index(v))

        # On prépare les cartes restantes (kicker), triées de la plus forte à la plus faible
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        # On crée et retourne l’objet Brelan
        return cls(hauteur, cartes, kicker)

    # Représentation lisible pour un joueur de poker
    def __str__(self):
        return f"Brelan de {self.hauteur}"  # Exemple : "Brelan de Roi"

    # Représentation technique pour le développeur ou le débogage
    def __repr__(self):
        # On construit une chaîne qui montre toutes les cartes
        cartes_repr = ", ".join(f"{c.valeur} de {c.couleur}" for c in self.cartes)
        return f"Brelan([{cartes_repr}])"  # Exemple : "Brelan([Roi de Coeur, Roi de Pique, Roi de Carreau, ...])"
