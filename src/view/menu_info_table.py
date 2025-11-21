import logging
import os

from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
    """Vue du menu de jeu du joueur"""

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu de jeu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Info de session",
                "Lancer manche",
                "Quitter table",
            ],
        ).execute()

        match choix:
            case "Info de session":
                import requests

                from view.menu_joueur_vue import MenuJoueurVue
                from view.session import Session

                session = Session()
                if not session.id:
                    print("Aucun joueur connecté")
                    return MenuJoueurVue()

                # Appel à l'API pour récupérer toutes les tables
                try:
                    res_tables = requests.get(f"{host}/table/")
                    res_tables.raise_for_status()
                    tables = res_tables.json()
                except requests.RequestException:
                    print("Impossible de récupérer la liste des tables")
                    return MenuJoueurVue()
                except ValueError:
                    print("Erreur : impossible de décoder la réponse JSON")
                    return MenuJoueurVue()

                # Chercher la table où le joueur est présent
                table_info = next(
                    (
                        t
                        for t in tables
                        if isinstance(t, dict)
                        and any(
                            isinstance(j, dict) and j.get("id_joueur") == session.id
                            for j in t.get("joueurs", [])
                        )
                    ),
                    None,
                )

                if not table_info:
                    print("Vous n'êtes connecté à aucune table")
                    return MenuJoueurVue()

                # Afficher les infos de la table
                numero_table = table_info.get("numero_table", "?")
                joueurs_list = table_info.get("joueurs", [])
                nb_joueurs = len(joueurs_list)
                nb_max = table_info.get("joueur_max", 0)

                print(f"\nTable n°{numero_table} : {nb_joueurs}/{nb_max} joueurs présents")
                print("-" * 40)
                for j in joueurs_list:
                    if isinstance(j, dict):
                        pseudo = j.get("pseudo", "Inconnu")
                        credit = j.get("credit", 0)
                        print(f"{pseudo} : {credit} crédits")

                return MenuJoueurVue()

            case "Lancer manche":
                from service.joueur_service import JoueurService

                joueur = JoueurService().trouver_par_id(Session().id)
                numero_table = joueur.numero_table
                if numero_table is None:
                    from view.menu_joueur_vue import MenuJoueurVue

                    return MenuJoueurVue(Session().afficher())

                req = requests.get(f"{host}{END_POINT}lancer/{numero_table}")

                if req.status_code == 200:
                    print("Manche lancée !")
                    from view.menu_manche_vue import MenuManche

                    return MenuManche("")
                else:
                    print("Erreur lors du lancement de la manche")
                    from view.menu_joueur_vue import MenuJoueurVue

                    return MenuJoueurVue(Session().afficher())

            case "Quitter table":
                from view.menu_joueur_vue import MenuJoueurVue
                from view.session import Session

                session = Session()
                if not session.id:
                    logger.info("Aucun joueur connecté")
                    return MenuJoueurVue()

                # On récupère le joueur connecté
                joueur_connecte = next(
                    (j for j in Session.joueurs_connectes if j.id_joueur == session.id), None
                )
                if not joueur_connecte:
                    logger.info("Erreur : joueur non trouvé dans les joueurs connectés")
                    return MenuJoueurVue()

                if not joueur_connecte.table:
                    logger.info("Vous n'êtes actuellement à aucune table")
                    return MenuJoueurVue()

                table = joueur_connecte.table
                try:
                    index = table.joueurs.index(joueur_connecte)
                    table.retirer_joueur(index)
                    logger.info(f"Vous avez quitté la table {table.numero_table}")
                except ValueError:
                    logger.info("Erreur : impossible de vous retirer de la table")

                # On met à jour la table globale
                Session.tables_globales[table.numero_table] = table

                return MenuJoueurVue()
