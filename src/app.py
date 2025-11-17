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
def crediter(pseudo, montant: int):
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    credit_service.crediter(joueur, montant)
    return f"l'admin a bien crediter {montant} à {joueur}"


# fonctionne
@app.put("/admin/debiter/{pseudo}/{montant}", tags=["Admin"])
def debiter(pseudo, montant: int):
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    credit_service.debiter(joueur, montant)
    return f"l'admin a bien debiter {montant} à {joueur}"

# fonctionne
@app.get("/joueur/connection/{pseudo}", tags=["Joueurs"])
async def joueur_connection(pseudo:str):
    """Connecte le joueur"""
    logging.info("Connecte le joueur")
    return joueur_service.se_connecter(pseudo)

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
    if not joueur:
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


# les fonctions de room_services me semble pas fini ou bizarre


class TableModel(BaseModel):
    """Définir un modèle Pydantic pour les Table"""

    numero_table: int | None = None  # Champ optionnel
    joueur_max: int
    grosse_blind: int
    mode_jeu: int | None = None  # Champ optionnel


# creer la table mais renvoie une erreur
@app.post("/table/", tags=["Table"])
async def creer_table(t: TableModel):
    """Créer une table"""
    logging.info("Créer une table")

    table = table_service.creer_table(t.joueur_max, t.grosse_blind)
    return table


@app.put("/table/ajouter/{pseudo}", tags=["Table"])
async def ajouter_joueur(pseudo):
    """ajoute un joueur a la table"""
    logging.info("ajoute un joueur a la table")
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    table_service.ajouter_joueur(joueur)
    return f"le joueur {joueur.pseudo} a été ajouté à la table"


@app.put("/table/retirer/{pseudo}", tags=["Table"])
async def retirer_un_joueur(pseudo):
    """retire un joueur a la table"""
    logging.info("retire un joueur a la table")
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    table_service.retirer_joueur(joueur)
    return f"le joueur {joueur.pseudo} a été retiré de la table"


@app.delete("/table/", tags=["Table"])
def supprimer_table(table: TableModel):
    """Supprimer une table"""
    logging.info("Supprimer une table")
    table_service.supprimer(table)
    return f"Table {table.numero_table} supprimé"


@app.put("/table/rotation_dealer", tags=["Table"])
async def rotation_dealer(table: TableModel):
    """change le dealer"""
    logging.info("change le dealer")
    table_service.rotation_dealer(table)
    return "le dealer de la table tourné"


@app.get("/table/", tags=["Table"])
async def liste_tables():
    """liste les tables"""
    logging.info("liste les tables")
    return table_service.liste_tables()


# peut etre créer un joueur model car aucune ne fonctionne avec un argument joueur
@app.get("/action/{joueur}", tags=["Action"])
async def manche_joueur(joueur):
    """Trouver la manche auquel joue le joueur"""
    logging.info("Trouver la manche auquel joue le joueur")
    return action_service.manche_joueur(joueur)


@app.put("/action/all_in/{joueur}", tags=["Action"])
async def all_in(joueur):
    """Joue all_in pour le joueur"""
    logging.info("Joue all_in pour le joueur")
    return action_service.all_in(joueur)


@app.put("/action/checker/{joueur}", tags=["Action"])
async def checker(joueur):
    """Joue checker pour le joueur"""
    logging.info("Joue checker pour le joueur")
    return action_service.checker(joueur)


@app.put("/action/se_coucher/{joueur}", tags=["Action"])
async def se_coucher(joueur):
    """Joue se_coucher pour le joueur"""
    logging.info("Joue se_coucher pour le joueur")
    return action_service.se_coucher(joueur)


@app.put("/action/suivre/{joueur}", tags=["Action"])
async def suivre(joueur):
    """Joue suivre pour le joueur"""
    logging.info("Joue suivre pour le joueur")
    return action_service.suivre(joueur)


# il manque peut etre miser mais il est pas dans actionservice

# Run the FastAPI application
if __name__ == "__main__":
    ResetDatabase().lancer()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5432)

    logging.info("Arret du Webservice")
