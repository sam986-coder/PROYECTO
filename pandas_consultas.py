import pandas as pd
from sqlalchemy import create_engine, text
import os

# Implementamos la misma lógica de conexión resiliente que en database.py
try:
    # Primero intentamos con el nombre del servicio en docker-compose
    DATABASE_URL = "mysql+pymysql://root:rootpassword@db:3306/superheroes"
    engine = create_engine(DATABASE_URL)
    # Verificamos la conexión
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ pandas_consultas.py: Conexión exitosa usando 'db' como host")
except Exception as e:
    try:
        # Si falla, intentamos con localhost y el puerto mapeado
        DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3309/superheroes"
        engine = create_engine(DATABASE_URL)
        # Verificamos la conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ pandas_consultas.py: Conexión exitosa usando 'localhost:3309'")
    except Exception as e:
        print(f"❌ pandas_consultas.py: Error de conexión: {str(e)}")
        # Si ambos fallan, lanzamos una excepción
        raise Exception(f"No se pudo conectar a la base de datos: {str(e)}")

def get_top_poderes_populares(TOP):
    """
    Obtiene los TOP poderes más populares basado en cantidad de superhéroes
    """
    query = f"""
    SELECT sp.power_name as 'Poder', 
           COUNT(hp.hero_id) as 'Cantidad de Héroes'
    FROM superpower sp
    JOIN hero_power hp ON sp.id = hp.power_id
    GROUP BY sp.power_name
    ORDER BY COUNT(hp.hero_id) DESC
    LIMIT {TOP}
    """
    
    df = pd.read_sql(query, engine)
    return df

def get_top_atributos_heroes(TOP):
    """
    Obtiene los TOP atributos más comunes entre los superhéroes
    """
    query = f"""
    SELECT a.attribute_name as 'Atributo', 
           COUNT(ha.hero_id) as 'Cantidad de Héroes'
    FROM attribute a
    JOIN hero_attribute ha ON a.id = ha.attribute_id
    GROUP BY a.attribute_name
    ORDER BY COUNT(ha.hero_id) DESC
    LIMIT {TOP}
    """
    
    df = pd.read_sql(query, engine)
    return df

def get_generos_distribucion():
    """
    Obtiene la distribución de superhéroes por género
    """
    query = """
    SELECT g.gender as 'Género', 
           COUNT(s.id) as 'Cantidad de Superhéroes'
    FROM gender g
    JOIN superhero s ON g.id = s.gender_id
    GROUP BY g.gender
    ORDER BY COUNT(s.id) DESC
    """
    
    df = pd.read_sql(query, engine)
    return df

def get_razas_distribucion():
    """
    Obtiene la distribución de superhéroes por raza
    """
    query = """
    SELECT r.race as 'Raza', 
           COUNT(s.id) as 'Cantidad de Superhéroes'
    FROM race r
    JOIN superhero s ON r.id = s.race_id
    GROUP BY r.race
    ORDER BY COUNT(s.id) DESC
    """
    
    df = pd.read_sql(query, engine)
    return df

def get_top_publishers_heroes(TOP):
    """
    Obtiene los TOP publishers con más superhéroes
    """
    query = f"""
    SELECT p.publisher_name as 'Editorial', 
           COUNT(s.id) as 'Cantidad de Superhéroes'
    FROM publisher p
    JOIN superhero s ON p.id = s.publisher_id
    GROUP BY p.publisher_name
    ORDER BY COUNT(s.id) DESC
    LIMIT {TOP}
    """
    
    df = pd.read_sql(query, engine)
    return df

def get_top_heroes_por_poderes(TOP):
    """
    Obtiene los TOP superhéroes con más poderes
    """
    query = f"""
    SELECT s.superhero_name as 'Superhéroe', 
           COUNT(hp.power_id) as 'Cantidad de Poderes'
    FROM superhero s
    JOIN hero_power hp ON s.id = hp.hero_id
    GROUP BY s.superhero_name
    ORDER BY COUNT(hp.power_id) DESC
    LIMIT {TOP}
    """
    
    df = pd.read_sql(query, engine)
    return df

def get_alineaciones_distribucion():
    """
    Obtiene la distribución de superhéroes por alineación
    """
    query = """
    SELECT a.alignment as 'Alineación', 
           COUNT(s.id) as 'Cantidad de Superhéroes'
    FROM alignment a
    JOIN superhero s ON a.id = s.alignment_id
    GROUP BY a.alignment
    ORDER BY COUNT(s.id) DESC
    """
    
    df = pd.read_sql(query, engine)
    return df