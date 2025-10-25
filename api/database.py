"""
=========================================================
Module : database.py
---------------------------------------------------------
Ce module gère la connexion MySQL via un pool de connexions
pour l'application FastAPI du projet :
Restaurant Analytics Data Platform
=========================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

# =========================================================
# Chargement des variables d'environnement (.env)
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent  
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Vérification rapide de la configuration
if not all(DB_CONFIG.values()):
    missing = [k for k, v in DB_CONFIG.items() if not v]
    raise ValueError(f"Variables manquantes dans .env : {', '.join(missing)}")


# =========================================================
# Création d’un pool de connexions MySQL
# =========================================================

try:
    cnxpool = pooling.MySQLConnectionPool(
        pool_name="restaurant_pool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG
    )
    print("Pool de connexions MySQL initialisé avec succès.")
except mysql.connector.Error as err:
    print(f"Erreur lors de la création du pool : {err}")
    raise


# =========================================================
# Fonctions utilitaires
# =========================================================

def get_conn():
    """
    Récupère une connexion active depuis le pool.
    """
    try:
        conn = cnxpool.get_connection()
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur lors de l’obtention d’une connexion : {err}")
        raise


def close_conn(conn, cursor=None):
    """
    Ferme proprement la connexion et le curseur.
    """
    try:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    except Exception as e:
        print(f"Erreur lors de la fermeture de connexion : {e}")


def test_connection():
    """
    Test simple pour vérifier que la base est accessible.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"Connexion réussie à la base : {db_name}")

        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]
        print("Tables disponibles :", ", ".join(tables))

    except mysql.connector.Error as err:
        print("Erreur de connexion :", err)
    finally:
        close_conn(conn, cursor)


# =========================================================
# Exemple d’utilisation directe
# =========================================================
if __name__ == "__main__":
    test_connection()
