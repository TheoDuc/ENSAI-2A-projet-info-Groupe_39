import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from business_object.joueur import Joueur
from service.joueur_service import JoueurService
from service.credit_service import CreditService
from utils.reset_database import ResetDatabase
from utils.log_init import initialiser_logs

app = FastAPI(title="Mon webservice")


initialiser_logs("Webservice")

joueur_service = JoueurService()
credit_service = CreditService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

# exemple pour plus tard
@app.put("/admin/crediter2/{joueur}/{montant}", tags=["Admin"])
def crediter(joueur, montant:int):
    reponse = input("Etes-vous un admin (oui ou non)")
    if reponse == 'oui':
        credit_service.crediter(joueur,montant)
    else:
        return (f"vous n'êtes pas admin")
    return(f"l'admin a bien crediter {montant} à {joueur}")

# fonctionne pas car Joueur() devient un str en entree
@app.put("/admin/crediter/{joueur}/{montant}", tags=["Admin"])
def crediter(joueur, montant:int):
    credit_service.crediter(joueur,montant)
    return(f"l'admin a bien crediter {montant} à {joueur}")

# fonctionne pas car Joueur() devient un str en entree
@app.put("/admin/debiter/{joueur}/{montant}", tags=["Admin"])
def debiter(joueur, montant:int):
    credit_service.debiter(joueur,montant)
    return(f"l'admin a bien debiter {montant} à {joueur}")

# fonctionne 
@app.get("/joueur/liste", tags=["Joueurs"])
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

class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    id_joueur: int | None = None  # Champ optionnel
    pseudo: str
    pays: str

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

# probleme avec les joueur.pays et joueur.pays qu'on ne peut pas modifier
@app.put("/joueur/{id_joueur}", tags=["Joueurs"])
def modifier_joueur(id_joueur: int, j: JoueurModel):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur.pseudo = j.pseudo
    joueur.pays = j.pays
    joueur = joueur_service.modifier(joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la modification du joueur")

    return f"Joueur {j.pseudo} modifié"

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


# Run the FastAPI application
if __name__ == "__main__":
    ResetDatabase().lancer()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5432)

    logging.info("Arret du Webservice")
