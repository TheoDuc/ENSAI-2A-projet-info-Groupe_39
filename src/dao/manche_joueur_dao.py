"""Implémentation de la classe MancheJoueurDAO"""

import logging
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton
from business_object.joueur import Joueur
from business_object.info_manche import InfoManche

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
                    for i, joueur in enumerate(info_manche.joueurs):
                        # On récupère les cartes du joueur si elles existent
                        carte1 = None
                        carte2 = None
                        if hasattr(info_manche, "cartes_mains"):
                            try:
                                carte1, carte2 = info_manche.cartes_mains[i]
                            except (IndexError, TypeError):
                                pass  # si non défini, reste None

                        # Insertion SQL
                        cursor.execute(
                            """
                            INSERT INTO manche_joueur (
                                id_manche,
                                id_joueur,
                                carte_main_1,
                                carte_main_2,
                                gain,
                                mise,
                                tour_couche,
                                statut
                            )
                            VALUES (
                                %(id_manche)s,
                                %(id_joueur)s,
                                %(carte_main_1)s,
                                %(carte_main_2)s,
                                %(gain)s,
                                %(mise)s,
                                %(tour_couche)s,
                                %(statut)s
                            );
                            """,
                            {
                                "id_manche": id_manche,
                                "id_joueur": joueur.id_joueur,
                                "carte_main_1": carte1,
                                "carte_main_2": carte2,
                                "gain": getattr(info_manche, "gains", [0] * len(info_manche.joueurs))[i],
                                "mise": getattr(info_manche, "mises", [0] * len(info_manche.joueurs))[i],
                                "tour_couche": getattr(info_manche, "tours_couche", [0] * len(info_manche.joueurs))[i],
                                "statut": getattr(info_manche, "statuts", ["en cours"] * len(info_manche.joueurs))[i],
                            },
                        )
            return True

        except Exception as e:
            logging.error(f"[ERREUR DAO] Création manche_joueur : {e}")
            return False

    # ---------------------------------------------------------------------
    @log
    def trouver_par_id_manche(self, id_manche: int) -> list[dict]:
        """
        Récupère toutes les lignes de la table manche_joueur associées à une manche donnée.

        Parameters
        ----------
        id_manche : int
            Identifiant unique de la manche concernée

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
                         WHERE id_manche = %(id_manche)s;
                        """,
                        {"id_manche": id_manche},
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
                        "id_manche_joueur": row["id_manche_joueur"],
                        "id_manche": row["id_manche"],
                        "id_joueur": row["id_joueur"],
                        "statut": row["statut"],
                        "mise": row["mise"],
                        "tour_couche": row["tour_couche"],
                    }
                )
        return participations

    # ---------------------------------------------------------------------
    @log
    def modifier_manche_joueur(
        self,
        id_manche: int,
        id_joueur: int,
        statut: str | None = None,
        mise: int | None = None,
        tour_couche: int | None = None,
    ) -> bool:
        """
        Met à jour les informations d'un joueur pour une manche donnée.
        """
        champs = []
        valeurs = {"id_manche": id_manche, "id_joueur": id_joueur}

        if statut is not None:
            champs.append("statut = %(statut)s")
            valeurs["statut"] = statut
        if mise is not None:
            champs.append("mise = %(mise)s")
            valeurs["mise"] = mise
        if tour_couche is not None:
            champs.append("tour_couche = %(tour_couche)s")
            valeurs["tour_couche"] = tour_couche

        if not champs:
            return False  # rien à modifier

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                        UPDATE manche_joueur
                           SET {', '.join(champs)}
                         WHERE id_manche = %(id_manche)s
                           AND id_joueur = %(id_joueur)s;
                        """,
                        valeurs,
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"[ERREUR DAO] Modification manche_joueur : {e}")
            return False

        return res == 1

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
    @log
    def ajouter_credit(self, joueur, montant: int) -> bool:
        """
        Ajoute un crédit à un joueur dans la table 'joueur'.
        Renvoie True si la mise à jour SQL a bien eu lieu, False sinon.
        """
        if montant <= 0:
            raise ValueError("Le montant à créditer doit être positif.")

        try:
            with DBConnection().connection as conn:
                with conn.cursor() as cursor:
                    query = """
                        UPDATE joueur
                        SET credit = credit + %s
                        WHERE id_joueur = %s
                    """
                    cursor.execute(query, (montant, joueur.id_joueur))
                    if cursor.rowcount == 1:
                        return True
                    else:
                        logger.warning(f"Aucun joueur trouvé pour id {joueur.id_joueur}")
                        return False

        except Exception as e:
            logger.error(f"Erreur lors de l’ajout de crédits pour {joueur.pseudo} : {e}")
            return False

    # -----------------------------------------------------------------
    @log
    def retirer_credit(self, joueur, montant: int) -> bool:
        """
        Retire un crédit à un joueur dans la table 'joueur'.
        Renvoie True si la mise à jour SQL a bien eu lieu, False sinon.
        """
        if montant <= 0:
            raise ValueError("Le montant à débiter doit être positif.")

        try:
            with DBConnection().connection as conn:
                with conn.cursor() as cursor:
                    query = """
                        UPDATE joueur
                        SET credit = credit - %s
                        WHERE id_joueur = %s AND credit >= %s
                    """
                    cursor.execute(query, (montant, joueur.id_joueur, montant))
                    if cursor.rowcount == 1:
                        return True
                    else:
                        logger.warning(
                            f"Impossible de retirer {montant} crédits à {joueur.pseudo} "
                            f"(fonds insuffisants ou joueur introuvable)"
                        )
                        return False

        except Exception as e:
            logger.error(f"Erreur lors du retrait de crédits pour {joueur.pseudo} : {e}")
            return False
