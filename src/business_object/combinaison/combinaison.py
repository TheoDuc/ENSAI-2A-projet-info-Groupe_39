from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Optional, Tuple

from business_object.carte import Carte


@total_ordering
class AbstractCombinaison(ABC):
    """
    Classe abstraite représentant une combinaison de cartes au poker.

    Cette classe définit l'interface commune à toutes les combinaisons
    (Paire, Brelan, Full, etc.), ainsi que les mécanismes de comparaison
    entre elles.

    Attributs
    ----------
    _hauteur : str
        Rang principal de la combinaison (par ex. 'Roi', 'Dame', 'As').
    _kicker : tuple[str, ...]
        Cartes de dénouement utilisées pour départager des combinaisons
        de même type et même hauteur.
    """

    def __init__(self, hauteur: str, kicker: Optional[Tuple[str, ...]] = None):
        """
        Initialise une combinaison abstraite à partir d'une hauteur et, éventuellement, d'un kicker.

        Paramètres
        ----------
        hauteur : str
            Valeur principale associée à la combinaison (ex. 'Roi' pour un Brelan de Rois).
        kicker : tuple[str, ...], optionnel
            Cartes de dénouement (par défaut une liste vide).

        Exceptions
        ----------
        ValueError
            Si la hauteur fournie n’est pas une valeur valide dans Carte.VALEURS().
        """
        if hauteur not in Carte.VALEURS():
            raise ValueError(f"Hauteur invalide : {hauteur}")
        self._hauteur = hauteur
        self._kicker = kicker or ()

    @property
    def hauteur(self) -> str:
        """
        Renvoie la hauteur principale de la combinaison.

        Renvois
        -------
        str
            Hauteur de la combinaison (par ex. 'Roi').
        """
        return self._hauteur

    @property
    def kicker(self) -> Tuple[str, ...]:
        """
        Renvoie le ou les kickers associés à la combinaison.

        Renvois
        -------
        tuple[str, ...]
            Tuple des valeurs des cartes de dénouement (peut être vide).
        """
        return self._kicker

    # --- Méthodes abstraites ---

    @classmethod
    @abstractmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison.

        Chaque type de combinaison possède une force relative,
        utilisée pour les comparaisons entre catégories.

        Renvois
        -------
        int
            Valeur entière représentant la force de la combinaison
            (plus la valeur est élevée, plus la combinaison est forte).
        """
        pass

    @classmethod
    @abstractmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si la combinaison est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte représentant la main à analyser.

        Renvois
        -------
        bool
            True si la combinaison est détectée, False sinon.
        """
        pass

    @classmethod
    @abstractmethod
    def from_cartes(cls, cartes: List[Carte]) -> "AbstractCombinaison":
        """
        Construit une instance de la combinaison à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à partir de laquelle on déduit la combinaison.

        Renvois
        -------
        AbstractCombinaison
            Instance concrète représentant la combinaison trouvée.
        """
        pass

    # --- Comparaisons ---

    def _valeur_comparaison(self):
        """
        Convertit la combinaison en valeurs numériques pour comparaison.

        Cette méthode produit un tuple de comparaison incluant :
        - la force de la combinaison,
        - la valeur numérique de la hauteur,
        - et celle des kickers.

        Renvois
        -------
        tuple
            Tuple numérique permettant les comparaisons entre combinaisons.
        """
        kickers = self.kicker
        if isinstance(kickers, str):
            kickers = (kickers,)
        elif isinstance(kickers, list):
            kickers = tuple(kickers)

        return (
            self.FORCE(),
            Carte.VALEURS().index(self.hauteur),
            tuple(Carte.VALEURS().index(k) for k in kickers),
        )

    def __eq__(self, other) -> bool:
        """
        Vérifie l’égalité entre deux combinaisons.

        Paramètres
        ----------
        other : AbstractCombinaison
            Autre combinaison à comparer.

        Renvois
        -------
        bool
            True si les deux combinaisons sont équivalentes, False sinon.
        """
        if not isinstance(other, AbstractCombinaison):
            return False
        return self._valeur_comparaison() == other._valeur_comparaison()

    def __lt__(self, other) -> bool:
        """
        Compare la combinaison courante à une autre pour déterminer l’ordre.

        Paramètres
        ----------
        other : AbstractCombinaison
            Autre combinaison à comparer.

        Renvois
        -------
        bool
            True si la combinaison courante est plus faible que `other`, False sinon.
        """
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() < other._valeur_comparaison()

    # --- Représentations ---

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la combinaison.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            par exemple :
            "Brelan(Roi, ('Dame', '10'))" ou "Paire(Valet)".
        """
        if self.kicker:
            return f"{self.__class__.__name__}({self.hauteur}, {self.kicker})"
        return f"{self.__class__.__name__}({self.hauteur})"

    def __repr__(self) -> str:
        """
        Representation technique de la combinaison.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Représentation textuelle exacte de l’objet.
        """
        return str(self)
