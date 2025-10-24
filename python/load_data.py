import os
import pandas as pd
import mysql.connector

# --- Connexion MySQL ---
DB_CONFIG = {
    "host": "localhost",
    "user": "psndao96",
    "password": "@Ndao20161696",
    "database": "restaurant_analytics"
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()
print("Connexion réussie à MySQL.")

# --- Dossier de données ---
DATA_DIR = "../data/raw"

# --- Chargement des données ---
TABLES = [
    ("customers.csv", "customers"),
    ("staff.csv", "staff"),
    ("menu.csv", "menu"),
    ("orders.csv", "orders"),
    ("deliveries.csv", "deliveries"),
    ("bookings.csv", "bookings")
]

def insert_data(file_path, table_name):
    print(f"\nChargement du fichier : {file_path}")
    df = pd.read_csv(file_path)
    df = df.where(pd.notnull(df), None)

    # On Vérifie les colonnes existantes dans la table
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    valid_cols = [col[0] for col in cursor.fetchall()]
    df = df[[c for c in df.columns if c in valid_cols]]

    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    for _, row in df.iterrows():
        try:
            cursor.execute(sql, tuple(row))
        except mysql.connector.errors.IntegrityError as e:
            print(f"Ligne ignorée (doublon ou contrainte) : {e}")

    conn.commit()
    print(f"Données insérées dans '{table_name}' ({len(df)} lignes).")

# --- Exécution globale ---
for file_name, table_name in TABLES:
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        insert_data(file_path, table_name)
    else:
        print(f"Fichier manquant : {file_path}")

cursor.close()
conn.close()
print("\nChargement terminé avec succès !")
