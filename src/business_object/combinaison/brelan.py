from collections import Counter

from business_object.carte import Carte
from business_object.combinaison.combinaison import AbstractCombinaison


class Brelan(AbstractCombinaison):
    """
    Représente un Brelan (trois cartes de même valeur).

    Un Brelan est une combinaison de poker composée de trois cartes de même valeur
    et de deux cartes supplémentaires appelées "kickers" servant à départager les égalités.
    """

    def __init__(self, hauteur: str, kicker: tuple[str] = None):
        """
        Initialise un objet Brelan avec une hauteur donnée et la liste de ses cartes.

        Paramètres
        ----------
        hauteur : str
            Valeur principale du Brelan (ex. 'Roi', '10', 'As').

        kicker : tuple[str], optionnel
            Valeurs des cartes restantes servant à départager les égalités.

        Renvois
        -------
        None
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force relative de la combinaison.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        int
            Force numérique associée au Brelan (4).
            Une valeur plus élevée indique une combinaison plus forte.
        """
        return 4

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si un Brelan (trois cartes de même valeur) est présent dans la main.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste des cartes parmi lesquelles on recherche un Brelan.

        Renvois
        -------
        bool
            True si au moins une valeur apparaît exactement trois fois, sinon False.
        """
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 3 for v in set(valeurs))

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Brelan":
        """
        Construit un objet Brelan à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste des cartes disponibles.

        Renvois
        -------
        Brelan
            Instance de la classe représentant le Brelan détecté.

        Exceptions
        ----------
        ValueError
            Levée si aucune combinaison de trois cartes de même valeur n’est trouvée.
        """
        if len(cartes) < 5:
            raise ValueError("Il faut au moins 5 cartes pour former un Brelan")
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        brelans = [v for v, count in compteur.items() if count == 3]
        if not brelans:
            details = ", ".join(f"{val}:{nb}" for val, nb in compteur.items())
            raise ValueError(f"Aucun brelan présent dans les cartes {details}")

        hauteur = max(brelans, key=lambda v: Carte.VALEURS().index(v))
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )[:2]  # On retient seulement les deux plus hauts kickers dans la combinaison
        )
        return cls(hauteur, kicker)

    def __str__(self):
        """
        Renvoie une représentation textuelle lisible du Brelan.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne lisible par un joueur, par exemple : "Brelan de Roi".
        """
        if self.hauteur == "As":
            return "Brelan d'As"
        return f"Brelan de {self.hauteur}"

    def __repr__(self):
        """
        Renvoie une représentation technique du Brelan.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne détaillant la combinaison, par exemple :
            "Brelan(hauteur=Roi, kickers=(As, Dame))"
        """

        if self.kicker:
            return f"Brelan(hauteur={self.hauteur}, kickers={self.kicker})"
        else:
            return f"Brelan(hauteur={self.hauteur})"
