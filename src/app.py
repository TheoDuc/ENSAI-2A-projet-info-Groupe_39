import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from service.action_service import ActionService
from service.credit_service import CreditService
from service.joueur_service import JoueurService
from service.table_service import TableService
from utils.log_init import initialiser_logs
from utils.reset_database import ResetDatabase

app = FastAPI(title="Mon webservice")


initialiser_logs("Webservice")

joueur_service = JoueurService()
credit_service = CreditService()
action_service = ActionService()
table_service = TableService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    id_joueur: int | None = None  # Champ optionnel
    pseudo: str
    pays: str
    credit: int | None = None  # Champ optionnel


# fonctionne pas oublier de demander si admin dans les view
@app.put("/admin/crediter/{pseudo}/{montant}", tags=["Admin"])
def crediter(pseudo: str, montant: int, est_admin: bool = False):
    joueur = joueur_service.trouver_par_pseudo(pseudo)

    if not est_admin:
        return {"error": "Vous n'êtes pas autorisé à créditer : accès admin requis."}

    credit_service.crediter(joueur, montant)
    return {"message": f"L'admin a bien crédité {montant} à {joueur.pseudo}"}


# fonctionne
@app.put("/admin/debiter/{pseudo}/{montant}", tags=["Admin"])
def debiter(pseudo, montant: int):
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    credit_service.debiter(joueur, montant)
    return f"l'admin a bien debiter {montant} à {joueur}"


# fonctionne
@app.get("/joueur/connection/{pseudo}", tags=["Joueurs"])
async def joueur_connection(pseudo: str):
    """Connecte le joueur"""
    logging.info("Connecte le joueur")
    return joueur_service.se_connecter(pseudo)


@app.get("/joueur/deconnection/{id_joueur}", tags=["Joueurs"])
async def joueur_deconnection(id_joueur: int):
    """Deconnecte le joueur"""
    logging.info("Deconnecte le joueur")
    return joueur_service.deconnexion(id_joueur)


# fonctionne
@app.get("/joueur/liste/", tags=["Joueurs"])
async def joueur_lister():
    """Liste tous les joueurs"""
    logging.info("Liste tous les joueurs")
    return joueur_service.lister_tous()


# fonctionne
@app.get("/joueur/id/{id_joueur}", tags=["Joueurs"])
async def joueur_par_id(id_joueur: int):
    """Trouver un joueur à partir de son id"""
    logging.info("Trouver un joueur à partir de son id")
    return joueur_service.trouver_par_id(id_joueur)


# fonctionne
@app.get("/joueur/{pseudo}", tags=["Joueurs"])
async def joueur_par_pseudo(pseudo: str):
    """Trouver un joueur à partir de son pseudo"""
    logging.info("Trouver un joueur à partir de son pseudo")
    return joueur_service.trouver_par_pseudo(pseudo)


# fonctionne
@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if joueur_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.pseudo, j.pays)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return joueur


# fonctionne
@app.put("/joueur/{id_joueur}/{pseudo}/{pays}", tags=["Joueurs"])
def modifier_joueur(id_joueur: int, pseudo: str, pays: str):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    if not joueur_service.pseudo_deja_utilise(pseudo):
        joueur.changer_pseudo(pseudo)
    joueur.changer_pays(pays)
    joueur = joueur_service.modifier(joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la modification du joueur")

    return f"Joueur {pseudo} modifié"


# fonctionne
@app.delete("/joueur/{pseudo}", tags=["Joueurs"])
def supprimer_joueur(pseudo: str):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur_service.supprimer(joueur)
    return f"Joueur {joueur.pseudo} supprimé"


class TableModel(BaseModel):
    """Définir un modèle Pydantic pour les Table"""

    numero_table: int | None = None  # Champ optionnel
    joueur_max: int
    grosse_blind: int
    mode_jeu: int | None = None  # Champ optionnel


# fonctionne
@app.post("/table/", tags=["Table"])
async def creer_table(t: TableModel):
    """Créer une table"""
    logging.info("Créer une table")

    table = table_service.creer_table(t.joueur_max, t.grosse_blind)
    return TableModel(
        numero_table=table.numero_table,
        joueur_max=table.joueur_max,
        grosse_blind=table.grosse_blind,
        mode_jeu=table.mode_jeu,
    )


# fonctionne
@app.put("/table/ajouter/{numero_table}/{id_joueur}", tags=["Table"])
async def ajouter_joueur(numero_table: int, id_joueur: int):
    """ajoute un joueur a la table"""
    logging.info("ajoute un joueur a la table")
    joueur = joueur_service.trouver_par_id(id_joueur)
    table_service.ajouter_joueur(numero_table, id_joueur)
    return f"le joueur {joueur.pseudo} a été ajouté à la table {numero_table}"


# fonctionne pas, le joueur ne garde pas en mémoire la table dans laquel il est
@app.put("/table/retirer/{id_joueur}", tags=["Table"])
async def retirer_un_joueur(id_joueur: str):
    """retire un joueur a la table"""
    logging.info("retire un joueur a la table")
    joueur = joueur_service.trouver_par_id(id_joueur)
    print(joueur.table)
    # pourquoi c'est None ??
    table_service.retirer_joueur(joueur)
    return f"le joueur {joueur.pseudo} a été retiré de la table"


# fonctionne
@app.delete("/table/{numero_table}", tags=["Table"])
def supprimer_table(numero_table: int):
    """Supprimer une table"""
    logging.info("Supprimer une table")
    table_service.supprimer_table(numero_table)
    return f"Table {numero_table} supprimé"


# fonctionne
@app.get("/table/", tags=["Table"])
async def liste_tables():
    """liste les tables"""
    logging.info("liste les tables")
    return table_service.affichages_tables()


@app.get("/table/session/{numero_table}", tags=["Table"])
async def infos_session(numero_table: int):
    """Renvoie les joueurs présents sur une table"""
    table = table_service.table_par_numero(numero_table)

    resultat = [
        {"id_joueur": j.id_joueur, "pseudo": j.pseudo, "credit": j.credit, "pays": j.pays}
        for j in table.joueurs
    ]
    return {"numero_table": table.numero_table, "joueurs": resultat}


# fonctionne pas
@app.get("/table/par_affichage/{affichage}", tags=["Table"])
async def table_par_affichage(affichage: str):
    """trouve une table par affichage"""
    logging.info("trouve une table par affichage")
    return table_service.table_par_affichage(affichage)


# fonctionne
@app.get("/table/lancer/{numero_table}", tags=["Table"])
async def lancer_manche(numero_table: int):
    """lance une manche"""
    logging.info("lance une manche")
    table_service.lancer_manche(numero_table=numero_table)
    return f"la manche est lancé sur la table {numero_table}"


# fonctionne
@app.get("/table/terminer/{numero_table}", tags=["Table"])
async def terminer_manche(numero_table: int):
    """termine une manche"""
    logging.info("termine une manche")
    table_service.terminer_manche(numero_table=numero_table)
    return f"la manche est terminé sur la table {numero_table}"


@app.get("/table/affichage/{numero_table}", tags=["Table"])
async def affichage_general(numero_table: int):
    """affichage general"""
    logging.info("affichage general")
    return table_service.affichage_general(numero_table=numero_table)


@app.get("/table/main/{numero_table}/{id_joueur}", tags=["Table"])
async def regarder_main(numero_table: int, id_joueur: int):
    """regarder sa main"""
    logging.info("regarder sa main")
    return table_service.regarder_main(numero_table=numero_table, id_joueur=id_joueur)


@app.get("/action/{id}", tags=["Action"])
async def manche_joueur(id: int):
    """Trouver la manche auquel joue le joueur"""
    logging.info("Trouver la manche auquel joue le joueur")
    return action_service.manche_joueur(id)


@app.put("/action/all_in/{id}", tags=["Action"])
async def all_in(id: int):
    """Joue all_in pour le joueur"""
    logging.info("Joue all_in pour le joueur")
    return action_service.all_in(id)


@app.put("/action/checker/{id}", tags=["Action"])
async def checker(id: int):
    """Joue checker pour le joueur"""
    logging.info("Joue checker pour le joueur")
    return action_service.checker(id)


@app.put("/action/se_coucher/{id}", tags=["Action"])
async def se_coucher(id: int):
    """Joue se_coucher pour le joueur"""
    logging.info("Joue se_coucher pour le joueur")
    return action_service.se_coucher(id)


@app.put("/action/suivre/{id}", tags=["Action"])
async def suivre(id: int):
    """Joue suivre pour le joueur"""
    logging.info("Joue suivre pour le joueur")
    return action_service.suivre(id)


# Run the FastAPI application
if __name__ == "__main__":
    ResetDatabase().lancer()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5432)

    logging.info("Arret du Webservice")
