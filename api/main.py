from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .routers import customers, staff, menu, orders, deliveries, bookings, analytics

api_description = """
## Bienvenue dans l’API Restaurant Analytics

API REST développée pour interagir avec la base de données **MySQL** du projet **Restaurant Analytics Data Platform**.
Cette API permet de gérer et d’analyser les données relatives aux clients, commandes, personnel, livraisons et réservations d’un restaurant.
Elle expose divers endpoints pour effectuer des opérations CRUD ainsi que des analyses via des vues SQL.

---

### Fonctionnalités principales :
- **Clients** : créer, lister, modifier ou supprimer les clients enregistrés  
- **Commandes** : suivre les commandes, montants totaux, et plats associés  
- **Personnel** : consulter les employés, leurs rôles et leurs performances  
- **Livraisons** : visualiser les livraisons, statuts et livreurs  
- **Réservations** : suivre les réservations et taux d’occupation  
- **Analytique** : exploiter des vues SQL pour suivre :
  - les ventes par plat   
  - la performance du personnel   
  - les statistiques de livraison  
  - les réservations mensuelles  

---

### Données exposées :
Les endpoints REST couvrent :
| Domaine | Exemple d’endpoint | Description |
|----------|--------------------|--------------|
| **Clients** | `/customers/` | CRUD complet sur les clients |
| **Commandes** | `/orders/` | Suivi des ventes et revenus |
| **Menu** | `/menu/` | Liste et prix des plats |
| **Livraisons** | `/deliveries/` | Suivi des livraisons et statuts |
| **Réservations** | `/bookings/` | Gestion des réservations |
| **Analytique** | `/analytics/sales-by-menu` | Vues consolidées SQL |

---

### Bon à savoir :
- Tous les endpoints supportent la **pagination** (`skip`, `limit`)  
- Des **filtres dynamiques** sont disponibles selon les routes  
- Vous pouvez tester directement toutes les routes via l’interface Swagger  `/docs`  
- En cas d’erreur (ex : ID inexistant), une **réponse JSON structurée** est retournée avec le bon code HTTP

---

### Stack technique :
- **FastAPI** — framework asynchrone moderne  
- **MySQL 8** — base de données relationnelle  
- **Pydantic** — validation stricte des modèles  
- **Uvicorn** — serveur ASGI rapide et léger  
- **Streamlit (à venir)** — tableau de bord analytique  

---
**Auteur** : [Pape Semou NDAO](https://github.com/psndao)  
**Contact** : [papesemoundao2016@gmail.com](mailto:papesemoundao2016@gmail.com)  
**Licence** : MIT License  
"""
app = FastAPI(
    title="Restaurant Analytics API",
    description=api_description,
    version="1.0.0",
)

# CORS
origins = os.getenv("ALLOWED_ORIGINS", "")
origins = [o.strip() for o in origins.split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
app.include_router(customers.router)
app.include_router(staff.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(deliveries.router)
app.include_router(bookings.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Restaurant Analytics", "docs": "/docs"}
