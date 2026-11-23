"""
Q-EOS - Módulo de Base de Datos (SQLite)
"""
import sqlite3
import pandas as pd

DB_NAME = "q_eos.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            nombre TEXT,
            ventas REAL,
            margen REAL,
            cargas REAL
        )
    """)
    conn.commit()
    conn.close()

def guardar_presupuesto(nombre: str, ventas: float, margen: float, cargas: float):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO presupuestos (nombre, ventas, margen, cargas)
        VALUES (?, ?, ?, ?)
    """, (nombre, ventas, margen, cargas))
    conn.commit()
    conn.close()

def obtener_presupuestos() -> pd.DataFrame:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM presupuestos ORDER BY fecha DESC", conn)
    conn.close()
    return df

if __name__ == "__main__":
    inicializar_db()
    print("Base de datos creada correctamente.")