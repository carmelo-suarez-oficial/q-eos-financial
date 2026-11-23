"""
Q-EOS - Módulo de Base de Datos (SQLite)
"""
import sqlite3

def inicializar_db():
    # Se conecta a la base de datos (si no existe, la crea)
    conn = sqlite3.connect("q_eos.db")
    cursor = conn.cursor()
    
    # Creamos la tabla para guardar los presupuestos
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

if __name__ == "__main__":
    inicializar_db()
    print("Base de datos creada correctamente.")