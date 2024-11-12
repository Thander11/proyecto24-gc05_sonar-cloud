import requests
import sqlite3
from flask import g
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine, Index
from sqlalchemy.pool import QueuePool

DATABASE = './RECOMENDACIONES_API/recomendaciones.db'

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

# Funciones para visualizaciones
def crear_visualizacion(usuario_id, contenido_id, duracion, tipo):
    try:
        db = get_db()
        cur = db.cursor()
        
        # Use UPSERT pattern to handle existing entries
        cur.execute('''
            INSERT INTO Visualizacion (usuarioId, contenidoId, fechaVisualizacion, duracion, tipo)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(usuarioId, contenidoId, tipo) 
            DO UPDATE SET 
                fechaVisualizacion = excluded.fechaVisualizacion,
                duracion = excluded.duracion
        ''', (usuario_id, contenido_id, datetime.now().isoformat(), duracion, tipo))
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error creando/actualizando visualización: {e}")
        return False



def obtener_visualizaciones_usuario(usuario_id):
    db = get_db()
    return db.execute('''
        SELECT * FROM Visualizacion 
        WHERE usuarioId = ? 
        ORDER BY datetime(fechaVisualizacion) DESC
    ''', (usuario_id,)).fetchall()

def obtener_visualizacion_especifica(usuario_id, contenido_id):
    db = get_db()
    return db.execute('''
        SELECT * FROM Visualizacion 
        WHERE usuarioId = ? AND contenidoId = ?
    ''', (usuario_id, contenido_id)).fetchone()

# Funciones para favoritos
def crear_favorito(usuario_id, contenido_id, tipo):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute('''
            INSERT INTO Favorito (usuarioId, contenidoId, fechaAgregado,tipo)
            VALUES (?, ?, ?,?)
        ''', (usuario_id, contenido_id, datetime.now().isoformat(),tipo))
        
        db.commit()
        return True
    except sqlite3.IntegrityError:
        raise ValueError("El contenido ya está en favoritos")
    except Exception as e:
        print(f"Error creando favorito: {e}")
        return False

def eliminar_favorito(usuario_id, contenido_id,tipo):
    db = get_db()
    cur = db.cursor()
    
    cur.execute('''
        DELETE FROM Favorito 
        WHERE usuarioId = ? AND contenidoId = ? AND tipo = ?
    ''', (usuario_id, contenido_id,tipo))
    
    db.commit()
    return cur.rowcount > 0

# database.py - Keep only SQL operation
def obtener_favoritos_usuario(usuario_id):
    db = get_db()
    return db.execute('''
        SELECT * FROM Favorito 
        WHERE usuarioId = ? 
        ORDER BY fechaAgregado DESC
    ''', (usuario_id,)).fetchall()
# Funciones para tendencias
def obtener_tendencias_db():
    db = get_db()
    return db.execute('''
        SELECT * FROM Tendencia 
        ORDER BY popularidad DESC 
        LIMIT 10
    ''').fetchall()

# In database.py - Update actualizar_tendencia function
def actualizar_tendencia(contenido_id):
    try:
        db = get_db()
        cur = db.cursor()
        
        # Only update popularity count, preserve existing tipo
        cur.execute('''
            INSERT INTO Tendencia (contenidoId, popularidad, tipo)
            VALUES (?, 1, (SELECT tipo FROM Tendencia WHERE contenidoId = ?))
            ON CONFLICT(contenidoId) DO UPDATE SET
            popularidad = popularidad + 1
            WHERE contenidoId = ?
        ''', (contenido_id, contenido_id, contenido_id))
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error actualizando tendencia: {e}")
        return False

def actualizar_tendencia_tipo(contenido_id, tipo):
    try:
        db = get_db()
        cur = db.cursor()
        
        cur.execute('''
            UPDATE Tendencia
            SET tipo = ?
            WHERE contenidoId = ?
        ''', (tipo, contenido_id))
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error actualizando tipo de tendencia: {e}")
        return False