from business_object.manche import Manche
from dao.manche_dao import MancheDAO


class MancheService:
    dao_manche = MancheDAO()

    def creer_manche(self, manche: Manche) -> None:
        """Crée une manche et l’enregistre via le DAO."""
        self.dao_manche.creer(manche)

    def supprimer_manche(self, manche: Manche) -> bool:
        """
        Supprime une manche existante.

        Retourne :
            bool: True si la suppression a réussi, False sinon.
        """
        return self.dao_manche.supprimer(manche)

    def obtenir_manche_par_id(self, id_manche: int) -> Manche | None:
        """
        Récupère une manche via son identifiant.

        Args:
            id_manche (int): Identifiant unique de la manche.

        Returns:
            Manche | None: L’objet Manche si trouvé, sinon None.
        """
        return self.dao_manche.trouver_par_id(id_manche)

    def lister_manches(self) -> list[Manche]:
        """
        Retourne la liste de toutes les manches enregistrées.
        """
        return self.dao_manche.lister_toutes()
