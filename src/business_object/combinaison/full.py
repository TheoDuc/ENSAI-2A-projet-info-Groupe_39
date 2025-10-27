from collections import Counter
from typing import List, Optional

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Full(AbstractCombinaison):
    """Classe représentant un Full (Brelan + Paire) au poker."""

    def __init__(self, brelan: str, kicker: Optional[None] = None):
        """
        Initialise une combinaison Full.

        Paramètres
        ----------
        brelan : str
            Valeur du Brelan (trois cartes identiques).
        kicker : None
            Toujours None pour Full.

        Renvois
        -------
        None
        """
        super().__init__(brelan, kicker)
        self._paire: Optional[str] = None  # sera défini après analyse des cartes

    @property
    def brelan(self) -> str:
        """
        Renvoie la valeur du Brelan du Full.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Valeur du Brelan (trois cartes identiques).
        """
        return self.hauteur

    @property
    def paire(self) -> Optional[str]:
        """
        Renvoie la valeur de la Paire du Full.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str | None
            Valeur de la Paire si définie, sinon None.
        """
        return self._paire

    @paire.setter
    def paire(self, valeur: str):
        """
        Définit la valeur de la Paire du Full.

        Paramètres
        ----------
        valeur : str
            Valeur de la Paire à attribuer.

        Renvois
        -------
        None
        """
        self._paire = valeur

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison Full.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        int
            Valeur entière correspondant à la force du Full (6).
        """
        return 6

    @classmethod
    def est_present(cls, cartes: List["Carte"]) -> bool:
        """
        Vérifie si un Full est présent dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si un Brelan et une Paire distincte sont présents, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        brelans = [v for v in set(valeurs) if valeurs.count(v) >= 3]
        paires = [v for v in set(valeurs) if valeurs.count(v) >= 2 and v not in brelans]
        return bool(brelans and paires)

    @classmethod
    def from_cartes(cls, cartes: List["Carte"]) -> "Full":
        """
        Construit une instance de Full à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche un Full.

        Renvois
        -------
        Full
            Instance représentant le Full détecté.

        Exceptions
        ----------
        ValueError
            Si aucun Brelan ou Paire n’est trouvé pour constituer le Full.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        brelans = [v for v in compteur if compteur[v] >= 3]
        if not brelans:
            raise ValueError(f"Aucun Brelan pour Full. Occurrences : {dict(compteur)}")
        brelan = max(brelans, key=lambda x: Carte.VALEURS().index(x))

        paires = [v for v in compteur if compteur[v] >= 2 and v != brelan]
        if not paires:
            raise ValueError(f"Aucune Paire pour Full. Occurrences : {dict(compteur)}")
        paire = max(paires, key=lambda x: Carte.VALEURS().index(x))

        full = cls(brelan)
        full.paire = paire
        return full

    def __str__(self):
        """
        Renvoie une représentation lisible du Full pour le joueur.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Exemple : "Full Dame et Roi".
        """
        return f"Full {self.hauteur} et {self._paire}"

    def __repr__(self):
        """
        Renvoie une représentation technique du Full pour le débogage.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Exemple : "Full(Hauteur(Dame), Paire(Roi))".
        """
        return f"Full(Hauteur({self.hauteur}), Paire({self._paire}))"

    def __eq__(self, other):
        """
        Vérifie l’égalité avec un autre Full.

        Paramètres
        ----------
        other : Full
            L’autre Full à comparer.

        Renvois
        -------
        bool
            True si même brelan et même paire, sinon False.
        """
        if not isinstance(other, Full):
            return False
        return self.hauteur == other.hauteur and self._paire == other._paire

    def __lt__(self, other):
        """
        Compare si ce Full est inférieur à un autre Full.

        Paramètres
        ----------
        other : Full
            L’autre Full à comparer.

        Renvois
        -------
        bool
            True si ce Full est plus faible que l’autre, False sinon.
        """
        if not isinstance(other, Full):
            return NotImplemented
        valeurs = Carte.VALEURS()
        if valeurs.index(self.hauteur) != valeurs.index(other.hauteur):
            return valeurs.index(self.hauteur) < valeurs.index(other.hauteur)
        return valeurs.index(self._paire) < valeurs.index(other._paire)

    def __gt__(self, other):
        """
        Compare si ce Full est supérieur à un autre Full.

        Paramètres
        ----------
        other : Full
            L’autre Full à comparer.

        Renvois
        -------
        bool
            True si ce Full est plus fort que l’autre, False sinon.
        """
        if not isinstance(other, Full):
            return NotImplemented
        valeurs = Carte.VALEURS()
        if valeurs.index(self.hauteur) != valeurs.index(other.hauteur):
            return valeurs.index(self.hauteur) > valeurs.index(other.hauteur)
        return valeurs.index(self._paire) > valeurs.index(other._paire)
