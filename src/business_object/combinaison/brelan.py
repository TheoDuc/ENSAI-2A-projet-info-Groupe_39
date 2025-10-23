from collections import Counter

from business_object.carte import Carte
from business_object.combinaison.combinaison import AbstractCombinaison


class Brelan(AbstractCombinaison):
    """
    Représente un Brelan (trois cartes de même valeur).

    Un Brelan est une combinaison de poker composée de trois cartes de même valeur
    et de deux cartes supplémentaires appelées "kickers" servant à départager les égalités.
    """

    def __init__(self, hauteur: str, cartes: list[Carte], kicker=None):
        """
        Initialise un objet Brelan avec une hauteur donnée et la liste de ses cartes.

        Paramètres
        ----------
        hauteur : str
            Valeur principale du Brelan (ex. 'Roi', '10', 'As').
        cartes : list[Carte]
            Liste complète des cartes de la main.
        kicker : tuple[str], optionnel
            Valeurs des cartes restantes servant à départager les égalités.

        Renvois
        -------
        None
        """
        super().__init__(hauteur, kicker)
        self.cartes = cartes

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
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        brelans = [v for v, count in compteur.items() if count >= 3]
        if not brelans:
            raise ValueError("Aucun brelan présent dans les cartes")

        hauteur = max(brelans, key=lambda v: Carte.VALEURS().index(v))
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(hauteur, cartes, kicker)

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
            "Brelan([Roi de Coeur, Roi de Pique, Roi de Carreau])".
        """
        cartes_repr = ", ".join(f"{c.valeur} de {c.couleur}" for c in self.cartes)
        return f"Brelan([{cartes_repr}])"
