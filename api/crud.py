from typing import Any, Dict, List, Tuple
from .database import get_conn

def fetch_all(sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def fetch_one(sql: str, params: Tuple = ()) -> Dict[str, Any] | None:
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        row = cur.fetchone()
        return row
    finally:
        cur.close()
        conn.close()

def execute(sql: str, params: Tuple = ()) -> int:
    """INSERT/UPDATE/DELETE, retourne nb lignes affectées."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()

def execute_many(sql: str, params_seq: List[Tuple]) -> int:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.executemany(sql, params_seq)
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()
