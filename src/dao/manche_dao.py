"""Implémentation de la classe MancheDAO"""

import json
import os
from typing import Optional

from business_object.info_manche import InfoManche
from business_object.manche import Manche


class MancheDAO:
    """
    DAO pour la persistance des objets Manche dans un fichier JSON.
    """

    FILE_PATH = "manches.json"

    # ----------------------------------------------------------
    # Méthodes principales
    # ----------------------------------------------------------
    @classmethod
    def lire_manche(cls, id_manche: int) -> Optional[Manche]:
        """
        Lit une manche depuis le fichier JSON.
        Retourne un objet Manche ou None si non trouvée.
        """
        data = cls._charger_donnees()
        manche_dict = data.get(str(id_manche))

        if manche_dict is None:
            return None

        return cls._dict_to_manche(manche_dict)

    # ----------------------------------------------------------
    # Méthodes internes
    # ----------------------------------------------------------
    @classmethod
    def _charger_donnees(cls) -> dict:
        """Charge les données depuis le fichier JSON."""
        if not os.path.exists(cls.FILE_PATH):
            return {}
        with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _sauver_donnees(cls, data: dict) -> None:
        """Sauvegarde les données dans le fichier JSON."""
        with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _manche_to_dict(manche: Manche) -> dict:
        """Convertit une Manche en dictionnaire JSON-sérialisable."""
        return {
            "grosse_blind": manche.grosse_blind,
            "pot": manche.pot,
            "tour": manche.tour,
            "indice_joueur_actuel": getattr(manche, "_Manche__indice_joueur_actuel", 0),
            # InfoManche n’est pas sérialisée en détail ici
            "info": str(manche.info.__class__.__name__),  # ou manche.info.to_dict() si dispo
        }

    # Dans manche_dao.py
    @staticmethod
    def _dict_to_manche(data: dict) -> Manche:
        """Recrée une Manche à partir d’un dictionnaire JSON."""
        grosse_blind = data.get("grosse_blind", 0)

        # On crée deux joueurs factices
        joueurs_fictifs = [
            Joueur(id_joueur=1, pseudo="J1", credit=1000, pays="FR"),
            Joueur(id_joueur=2, pseudo="J2", credit=1000, pays="FR"),
        ]
        info = InfoManche(joueurs_fictifs)

        manche = Manche(info, grosse_blind)

        manche._Manche__pot = data.get("pot", 0)
        manche._Manche__tour = data.get("tour", 0)
        manche._Manche__indice_joueur_actuel = data.get("indice_joueur_actuel", 0)

        return manche
