"""Implémentation de la classe MancheJoueurDAO"""

import logging
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton
from business_object.joueur import Joueur
from business_object.info_manche import InfoManche
from business_object.manche import Manche

logger = logging.getLogger(__name__)


class MancheJoueurDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder à la table manche_joueur"""

    # ---------------------------------------------------------------------
    @log
    def creer_manche_joueur(self, id_manche: int, info_manche: InfoManche) -> bool:
        """
        Création des entrées de la table manche_joueur pour une manche donnée.

        Parameters
        ----------
        id_manche : int
            Identifiant unique de la manche concernée
        info_manche : InfoManche
            Objet contenant la liste des joueurs, leurs mises, statuts et tours de couchage

        Returns
        -------
        created : bool
            True si la création s'est bien déroulée, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    manche = Manche(info_manche, 5)
                    gains = manche.distribuer_pot()
                    for i, joueur in enumerate(info_manche.joueurs):
                        # On récupère les cartes du joueur si elles existent
                        carte1 = None
                        carte2 = None
                        gain = gains[i]
                        if hasattr(info_manche, "cartes_mains"):
                            try:
                                carte1, carte2 = info_manche.cartes_mains[i]
                            except (IndexError, TypeError):
                                pass  # si non défini, reste None

                        # Insertion SQL
                        cursor.execute(
                            """
                            INSERT INTO manche_joueur(
                                id_joueur,
                                id_manche,
                                carte_main_1,
                                carte_main_2,
                                mise,
                                gain,
                                tour_couche
                            )
                            VALUES (
                                %(id_joueur)s,
                                %(id_manche)s,
                                %(carte_main_1)s,
                                %(carte_main_2)s,
                                %(mise)s,
                                %(gain)s,
                                %(tour_couche)s
                            );
                            """,
                            {
                                "id_manche": id_manche,
                                "id_joueur": joueur.id_joueur,
                                "carte_main_1": carte1,
                                "carte_main_2": carte2,
                                "gain": gains[i],
                                "mise": info_manche.mises[i],
                                "tour_couche": info_manche.tour_couche[i],
                            },
                        )
            return True

        except Exception as e:
            logging.error(f"[ERREUR DAO] Création manche_joueur : {e}")
            return False

    # ---------------------------------------------------------------------
    @log
    def trouver_par_ids(self, id_manche: int, id_joueur: int) -> list[dict]:
        """
        Récupère toutes les lignes de la table manche_joueur associées à une manche donnée.

        Parameters
        ----------
        id_manche : int
            Identifiant de la manche concernée
        id_joueur : int
            Identifiant du joueur concernée

        Returns
        -------
        participations : list[dict]
            Liste des participations des joueurs dans cette manche
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                          FROM manche_joueur
                         WHERE id_manche = %(id_manche)s and id_joueur = %(id_joueur)s;
                        """,
                        {"id_manche": id_manche,
                        "id_joueur": id_joueur},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.error(f"[ERREUR DAO] Lecture manche_joueur : {e}")
            raise

        participations = []
        if res:
            for row in res:
                participations.append(
                    {
                        "id_manche": row["id_manche"],
                        "id_joueur": row["id_joueur"],
                        "carte_main_1": row["carte_main_1"],
                        "carte_main_2": row["carte_main_2"],
                        "gain": row["gain"],
                        "mise": row["mise"],
                        "tour_couche": row["tour_couche"],
                    }
                )
        return participations


    # ---------------------------------------------------------------------
    @log
    def supprimer_par_id_manche(self, id_manche: int) -> bool:
        """
        Supprime toutes les participations liées à une manche.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM manche_joueur
                         WHERE id_manche = %(id_manche)s;
                        """,
                        {"id_manche": id_manche},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"[ERREUR DAO] Suppression manche_joueur : {e}")
            raise

        return res > 0

    # ---------------------------------------------------------------------
    @log
    def supprimer_participation(self, id_manche: int, id_joueur: int) -> bool:
        """
        Supprime la participation d’un joueur spécifique à une manche.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM manche_joueur
                         WHERE id_manche = %(id_manche)s
                           AND id_joueur = %(id_joueur)s;
                        """,
                        {"id_manche": id_manche, "id_joueur": id_joueur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"[ERREUR DAO] Suppression participation : {e}")
            raise

        return res == 1


mjdao = MancheJoueurDAO()
joueur1 = Joueur(998, 'a', 500, 'us') 
joueur2 = Joueur(999, 'admin', 50, 'fr')
info_manche = InfoManche([joueur1, joueur2])
print(mjdao.creer_manche_joueur(1, info_manche))
print(mjdao.trouver_par_ids(997,997))