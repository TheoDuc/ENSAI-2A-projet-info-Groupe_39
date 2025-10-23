from typing import List, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Carre(AbstractCombinaison):
    """
    Représente un Carré (quatre cartes de même valeur).

    Un Carré est une combinaison de poker composée de quatre cartes identiques et d'une carte supplémentaire
    appelée "kicker" servant à départager les égalités.
    """

    def __init__(self, cartes: List[Carte], kicker: Tuple[str, ...] = ()):
        """
        Initialise un objet Carré avec une liste de cartes et un kicker optionnel.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste des quatre cartes constituant le Carré.
        kicker : Tuple[str, ...], optionnel
            Cartes restantes servant à départager les égalités, triées de la plus forte à la plus faible.

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            Levée si le nombre de cartes n’est pas 4 ou si toutes les cartes n’ont pas la même valeur.
        """
        if len(cartes) != 4:
            raise ValueError(
                f"Un Carré doit être constitué de 4 cartes,mais {len(cartes)} cartes ont été fournies"
            )
        hauteur = cartes[0].valeur
        if not all(c.valeur == hauteur for c in cartes):
            valeurs_diff = [c.valeur for c in cartes if c.valeur != hauteur]
            raise ValueError(
                f"Toutes les cartes doivent avoir la même valeur pour un Carré"
                f", mais les valeurs suivantes diffèrent : {valeurs_diff}"
            )
        super().__init__(hauteur, kicker)
        self.cartes = cartes

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force relative de la combinaison Carré.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        int
            Force numérique associée au Carré (7).
            Une valeur plus élevée indique une combinaison plus forte.
        """
        return 7

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si un Carré est présent dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste des cartes parmi lesquelles rechercher un Carré.

        Renvois
        -------
        bool
            True si une valeur apparaît exactement quatre fois, sinon False.
        """
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 4 for v in set(valeurs))

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Carre":
        """
        Construit un objet Carré à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste des cartes disponibles.

        Renvois
        -------
        Carre
            Instance de la classe représentant le Carré détecté.

        Exceptions
        ----------
        ValueError
            Levée si aucune combinaison de quatre cartes de même valeur n’est trouvée.
        """
        valeurs = [c.valeur for c in cartes]
        try:
            hauteur = next(v for v in set(valeurs) if valeurs.count(v) == 4)
        except StopIteration:
            compte_valeurs = {v: valeurs.count(v) for v in set(valeurs)}
            raise ValueError(
                f"Aucun Carré présent dans les cartes. Occurrences des valeurs : {compte_valeurs}"
            )
        carre_cartes = [c for c in cartes if c.valeur == hauteur]
        kicker = tuple(
            sorted(
                [c.valeur for c in cartes if c.valeur != hauteur],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )
        return cls(carre_cartes, kicker)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible du Carré.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne lisible par un joueur, par exemple : "Carre de Roi".
        """
        return f"Carre de {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique du Carré
        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne détaillant la combinaison, par exemple :
            "Carre([Roi de Coeur, Roi de Pique, Roi de Carreau, Roi de Trèfle])".
        """
        cartes_str = ", ".join(f"{c.valeur} de {c.couleur}" for c in self.cartes)
        return f"Carre([{cartes_str}])"
