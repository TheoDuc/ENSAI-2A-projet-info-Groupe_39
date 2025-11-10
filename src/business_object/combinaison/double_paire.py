from collections import Counter

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class DoublePaire(AbstractCombinaison):
    """
    Classe représentant une combinaison *Double Paire* (deux paires de cartes de même valeur).

    La combinaison est caractérisée par :
    - la hauteur de la paire la plus forte,
    - la hauteur de la deuxième paire ,
    - et éventuellement la carte restante servant de kicker supplémentaire.
    """

    def __init__(self, hauteur: tuple[str], kicker: str) -> None:
        """
        Initialise une combinaison Double Paire.

        Paramètres
        ----------
        hauteur : tuple[str]
        kicker : str
        La carte restante servant de kicker.
        """
        hauteur = sorted(hauteur, key=lambda x: Carte.VALEURS().index(x), reverse=True)
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison *Double Paire*.

        Renvois
        -------
        int
            Valeur entière représentant la force de la combinaison.

        """
        return 2

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une Double Paire est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte représentant la main à analyser.

        Renvois
        -------
        bool
            True si au moins deux valeurs apparaissent au moins deux fois, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        return len([v for v in set(valeurs) if valeurs.count(v) >= 2]) >= 2

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "DoublePaire":
        """
        Construit une instance de Double Paire à partir d’une liste de cartes.

        Recherche les deux paires les plus fortes et détermine le kicker
        éventuel (la carte la plus haute restante).

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte pour générer la combinaison.

        Renvois
        -------
        DoublePaire
            Instance de la combinaison avec la paire la plus forte et le kicker calculé.

        Exceptions
        ----------
        ValueError
            Si moins de deux paires sont présentes dans la main.


        """
        cls.verifier_min_cartes(cartes)

        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        # Trouver toutes les valeurs ayant au moins deux cartes
        paires_possibles = [v for v, count in compteur.items() if count >= 2]
        if len(paires_possibles) < 2:
            raise ValueError("Aucune Double Paire présente dans les cartes")
        # Prendre les deux paires les plus hautes
        paires_hautes = sorted(
            paires_possibles, key=lambda v: Carte.VALEURS().index(v), reverse=True
        )[:2]

        # Déterminer le kicker : carte la plus haute restante
        cartes_restantes = [v for v in valeurs if v not in paires_hautes]

        kicker_val = (
            max(cartes_restantes, key=lambda v: Carte.VALEURS().index(v))
            if cartes_restantes
            else None
        )

        return cls(hauteur=paires_hautes, kicker=kicker_val)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Double Paire.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne lisible par un joueur, par exemple :
            "Double Paire Roi  Dame".
        """
        return f"Double Paire {self.hauteur[0]} {self.hauteur[1]}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Double Paire

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Exemple : "DoublePaire(hauteur=Roi, kicker=(Dame, 9))".
        """
        kicker_str = self.kicker if self.kicker else "None"
        return f"DoublePaire(hauteur={self.hauteur}, kicker={kicker_str})"
