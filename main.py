from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import os

# Importar las funciones desde los módulos que ya tenemos
from database import get_db, get_tables, get_table_data, execute_query, get_table_to_dataframe, export_table_to_csv, create_bar_chart, create_line_chart, get_database_schema
from formato import tabla_formato
import pandas_consultas as pandas_mod  # Renombrado para evitar conflicto con la librería pandas
import seaborn_consultas as seaborn_mod  # Renombrado para evitar conflicto con la librería seaborn

app = FastAPI(
    title="Superhero Database API",
    description="API para consultar la base de datos de superhéroes",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la base de datos al iniciar la aplicación
@app.on_event("startup")
def startup():
    try:
        # Verificamos la conexión a la base de datos
        db = next(get_db())
        print("✅ Conexión a la base de datos exitosa")
        db.close()
    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Superhero Database API is running"}

# Endpoint para listar tablas
@app.get("/tables")
def list_tables():
    try:
        tables = get_tables()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tablas: {str(e)}")

# Endpoint para obtener datos de una tabla
@app.get("/tables/{table_name}")
def get_table(table_name: str, limit: int = 100):
    try:
        data = get_table_data(table_name, limit)
        return {"table": table_name, "data": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de la tabla: {str(e)}")

# Endpoint para ejecutar consultas SQL personalizadas
@app.post("/query")
def run_query(query: str):
    try:
        data = execute_query(query)
        return {"result": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Endpoint para obtener el esquema de la base de datos
@app.get("/schema")
def get_schema():
    try:
        schema = get_database_schema()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el esquema: {str(e)}")

# Endpoint para exportar una tabla a CSV
@app.get("/export/{table_name}")
def export_to_csv(table_name: str):
    try:
        file_path = f"./exports/{table_name}.csv"
        export_table_to_csv(table_name, file_path)
        return {"message": f"Tabla {table_name} exportada a {file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al exportar la tabla: {str(e)}")

# ----- ENDPOINTS PARA CONSULTAS PANDAS -----

# TOP poderes más populares
@app.get("/pandas/top-poderes")
def top_poderes(top: int = Query(10, description="Cantidad de poderes a mostrar")):
    try:
        df = pandas_mod.get_top_poderes_populares(top)
        return tabla_formato(df, f"TOP {top} Poderes más Populares")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# TOP atributos de héroes
@app.get("/pandas/top-atributos")
def top_atributos(top: int = Query(10, description="Cantidad de atributos a mostrar")):
    try:
        df = pandas_mod.get_top_atributos_heroes(top)
        return tabla_formato(df, f"TOP {top} Atributos más Comunes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# Distribución de géneros
@app.get("/pandas/generos")
def generos_distribucion():
    try:
        df = pandas_mod.get_generos_distribucion()
        return tabla_formato(df, "Distribución de Superhéroes por Género")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# Distribución de razas
@app.get("/pandas/razas")
def razas_distribucion():
    try:
        df = pandas_mod.get_razas_distribucion()
        return tabla_formato(df, "Distribución de Superhéroes por Raza")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# TOP publishers
@app.get("/pandas/top-publishers")
def top_publishers(top: int = Query(10, description="Cantidad de editoriales a mostrar")):
    try:
        df = pandas_mod.get_top_publishers_heroes(top)
        return tabla_formato(df, f"TOP {top} Editoriales con más Superhéroes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# TOP héroes por cantidad de poderes
@app.get("/pandas/top-heroes-poderes")
def top_heroes_poderes(top: int = Query(10, description="Cantidad de héroes a mostrar")):
    try:
        df = pandas_mod.get_top_heroes_por_poderes(top)
        return tabla_formato(df, f"TOP {top} Superhéroes con más Poderes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# Distribución de alineaciones
@app.get("/pandas/alineaciones")
def alineaciones_distribucion():
    try:
        df = pandas_mod.get_alineaciones_distribucion()
        return tabla_formato(df, "Distribución de Superhéroes por Alineación")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")

# ----- ENDPOINTS PARA GRÁFICOS SEABORN -----

# Gráfico de TOP héroes por poderes
@app.get("/seaborn/heroes-poderes-grafico")
def heroes_poderes_grafico(top: int = Query(10, description="Cantidad de héroes a mostrar")):
    try:
        return seaborn_mod.get_top_heroes_por_poderes_grafico(top)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# Gráfico de distribución de alineaciones
@app.get("/seaborn/alineaciones-grafico")
def alineaciones_grafico():
    try:
        return seaborn_mod.get_distribucion_alineaciones_grafico()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# Gráfico de distribución de géneros
@app.get("/seaborn/generos-grafico")
def generos_grafico():
    try:
        return seaborn_mod.get_distribucion_generos_grafico()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# Gráfico de TOP poderes
@app.get("/seaborn/poderes-grafico")
def poderes_grafico(top: int = Query(10, description="Cantidad de poderes a mostrar")):
    try:
        return seaborn_mod.get_top_poderes_grafico(top)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# Gráfico de editoriales por alineación
@app.get("/seaborn/publisher-alineacion-grafico")
def publisher_alineacion_grafico(top: int = Query(10, description="Cantidad de editoriales a mostrar")):
    try:
        return seaborn_mod.get_publisher_por_alineacion_grafico(top)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# Gráfico de características físicas
@app.get("/seaborn/caracteristicas-grafico")
def caracteristicas_grafico():
    try:
        return seaborn_mod.get_distribucion_caracteristicas_grafico()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# Gráfico de alturas y pesos
@app.get("/seaborn/alturas-pesos-grafico")
def alturas_pesos_grafico():
    try:
        return seaborn_mod.get_alturas_pesos_superheroes_grafico()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar gráfico: {str(e)}")

# ----- CONSULTAS SQL PERSONALIZADAS -----

# Consulta personalizada: TOP héroes con más de un tipo de poder específico
@app.get("/sql/heroes-con-poder")
def heroes_con_poder(poder: str = Query(..., description="Nombre del poder a buscar")):
    try:
        query = f"""
        SELECT s.superhero_name as 'Superhéroe', 
               COUNT(hp.power_id) as 'Cantidad de Poderes'
        FROM superhero s
        JOIN hero_power hp ON s.id = hp.hero_id
        JOIN superpower sp ON hp.power_id = sp.id
        WHERE sp.power_name LIKE '%{poder}%'
        GROUP BY s.superhero_name
        ORDER BY COUNT(hp.power_id) DESC
        LIMIT 10
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, f"Superhéroes con poderes relacionados a '{poder}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Consulta personalizada: Comparativa de poderes entre dos superhéroes
@app.get("/sql/comparar-heroes")
def comparar_heroes(heroe1: str = Query(..., description="Nombre del primer superhéroe"),
                   heroe2: str = Query(..., description="Nombre del segundo superhéroe")):
    try:
        query = f"""
        SELECT sp.power_name as 'Poder',
               MAX(CASE WHEN s.superhero_name = '{heroe1}' THEN 'Sí' ELSE 'No' END) as '{heroe1}',
               MAX(CASE WHEN s.superhero_name = '{heroe2}' THEN 'Sí' ELSE 'No' END) as '{heroe2}'
        FROM superpower sp
        LEFT JOIN hero_power hp ON sp.id = hp.power_id
        LEFT JOIN superhero s ON hp.hero_id = s.id AND s.superhero_name IN ('{heroe1}', '{heroe2}')
        GROUP BY sp.power_name
        HAVING MAX(CASE WHEN s.superhero_name = '{heroe1}' THEN 1 ELSE 0 END) = 1 OR
               MAX(CASE WHEN s.superhero_name = '{heroe2}' THEN 1 ELSE 0 END) = 1
        ORDER BY sp.power_name
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, f"Comparativa de poderes: {heroe1} vs {heroe2}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Consulta personalizada: Análisis de atributos por género
@app.get("/sql/atributos-por-genero")
def atributos_por_genero():
    try:
        query = """
        SELECT g.gender as 'Género',
               a.attribute_name as 'Atributo',
               COUNT(ha.hero_id) as 'Cantidad de Héroes'
        FROM gender g
        JOIN superhero s ON g.id = s.gender_id
        JOIN hero_attribute ha ON s.id = ha.hero_id
        JOIN attribute a ON ha.attribute_id = a.id
        GROUP BY g.gender, a.attribute_name
        ORDER BY g.gender, COUNT(ha.hero_id) DESC
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, "Análisis de Atributos por Género")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Consulta personalizada: Poderes más comunes por editorial
@app.get("/sql/poderes-por-editorial")
def poderes_por_editorial(editorial: str = Query(..., description="Nombre de la editorial")):
    try:
        query = f"""
        SELECT sp.power_name as 'Poder',
               COUNT(hp.hero_id) as 'Cantidad de Héroes'
        FROM superpower sp
        JOIN hero_power hp ON sp.id = hp.power_id
        JOIN superhero s ON hp.hero_id = s.id
        JOIN publisher p ON s.publisher_id = p.id
        WHERE p.publisher_name LIKE '%{editorial}%'
        GROUP BY sp.power_name
        ORDER BY COUNT(hp.hero_id) DESC
        LIMIT 15
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, f"Poderes más comunes en héroes de {editorial}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Consulta personalizada: Distribución de características físicas por alineación
@app.get("/sql/caracteristicas-por-alineacion")
def caracteristicas_por_alineacion():
    try:
        query = """
        SELECT a.alignment as 'Alineación',
               'Color de ojos' as 'Característica',
               c.colour as 'Color',
               COUNT(s.id) as 'Cantidad'
        FROM alignment a
        JOIN superhero s ON a.id = s.alignment_id
        JOIN colour c ON s.eye_colour_id = c.id
        GROUP BY a.alignment, c.colour
        
        UNION ALL
        
        SELECT a.alignment as 'Alineación',
               'Color de cabello' as 'Característica',
               c.colour as 'Color',
               COUNT(s.id) as 'Cantidad'
        FROM alignment a
        JOIN superhero s ON a.id = s.alignment_id
        JOIN colour c ON s.hair_colour_id = c.id
        GROUP BY a.alignment, c.colour
        
        UNION ALL
        
        SELECT a.alignment as 'Alineación',
               'Color de piel' as 'Característica',
               c.colour as 'Color',
               COUNT(s.id) as 'Cantidad'
        FROM alignment a
        JOIN superhero s ON a.id = s.alignment_id
        JOIN colour c ON s.skin_colour_id = c.id
        GROUP BY a.alignment, c.colour
        
        ORDER BY 'Alineación', 'Característica', 'Cantidad' DESC
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, "Características Físicas por Alineación")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Consulta personalizada: Análisis de combos de poderes
@app.get("/sql/combos-poderes")
def combos_poderes(top: int = Query(10, description="Cantidad de combinaciones a mostrar")):
    try:
        query = f"""
        SELECT
            sp1.power_name as 'Poder 1',
            sp2.power_name as 'Poder 2',
            COUNT(*) as 'Frecuencia'
        FROM
            hero_power hp1
        JOIN
            hero_power hp2 ON hp1.hero_id = hp2.hero_id AND hp1.power_id < hp2.power_id
        JOIN
            superpower sp1 ON hp1.power_id = sp1.id
        JOIN
            superpower sp2 ON hp2.power_id = sp2.id
        GROUP BY
            sp1.power_name, sp2.power_name
        ORDER BY
            COUNT(*) DESC
        LIMIT {top}
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, f"TOP {top} Combinaciones de Poderes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

# Consulta personalizada: Superhéroes con características similares
@app.get("/sql/heroes-similares")
def heroes_similares(heroe: str = Query(..., description="Nombre del superhéroe")):
    try:
        query = f"""
        WITH hero_features AS (
            SELECT
                s.id,
                s.superhero_name,
                s.gender_id,
                s.eye_colour_id,
                s.hair_colour_id,
                s.skin_colour_id,
                s.race_id,
                s.publisher_id,
                s.alignment_id
            FROM superhero s
            WHERE s.superhero_name = '{heroe}'
        )
        
        SELECT
            s.superhero_name as 'Superhéroe',
            (CASE WHEN s.gender_id = hf.gender_id THEN 1 ELSE 0 END +
             CASE WHEN s.eye_colour_id = hf.eye_colour_id THEN 1 ELSE 0 END +
             CASE WHEN s.hair_colour_id = hf.hair_colour_id THEN 1 ELSE 0 END +
             CASE WHEN s.skin_colour_id = hf.skin_colour_id THEN 1 ELSE 0 END +
             CASE WHEN s.race_id = hf.race_id THEN 1 ELSE 0 END +
             CASE WHEN s.publisher_id = hf.publisher_id THEN 1 ELSE 0 END +
             CASE WHEN s.alignment_id = hf.alignment_id THEN 1 ELSE 0 END) as 'Similitud'
        FROM
            superhero s, hero_features hf
        WHERE
            s.superhero_name <> '{heroe}'
            AND (s.gender_id = hf.gender_id
                OR s.eye_colour_id = hf.eye_colour_id
                OR s.hair_colour_id = hf.hair_colour_id
                OR s.skin_colour_id = hf.skin_colour_id
                OR s.race_id = hf.race_id
                OR s.publisher_id = hf.publisher_id
                OR s.alignment_id = hf.alignment_id)
        ORDER BY
            'Similitud' DESC
        LIMIT 10
        """
        data = execute_query(query)
        df = pd.DataFrame(data)
        return tabla_formato(df, f"Superhéroes similares a {heroe}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)