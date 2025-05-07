from fastapi import Response
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from sqlalchemy import create_engine, text

# Implementamos la misma lógica de conexión resiliente
try:
    # Primero intentamos con el nombre del servicio en docker-compose
    DATABASE_URL = "mysql+pymysql://root:rootpassword@db:3306/superheroes"
    engine = create_engine(DATABASE_URL)
    # Verificamos la conexión
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ seaborn_consultas.py: Conexión exitosa usando 'db' como host")
except Exception as e:
    try:
        # Si falla, intentamos con localhost y el puerto mapeado
        DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3309/superheroes"
        engine = create_engine(DATABASE_URL)
        # Verificamos la conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ seaborn_consultas.py: Conexión exitosa usando 'localhost:3309'")
    except Exception as e:
        print(f"❌ seaborn_consultas.py: Error de conexión: {str(e)}")
        # Si ambos fallan, lanzamos una excepción
        raise Exception(f"No se pudo conectar a la base de datos: {str(e)}")

def get_top_heroes_por_poderes_grafico(TOP):
    """
    Genera una gráfica de barras con los TOP superhéroes con más poderes
    """
    query = f"""
    SELECT s.superhero_name as name, 
           COUNT(hp.power_id) as powers_count
    FROM superhero s
    JOIN hero_power hp ON s.id = hp.hero_id
    GROUP BY s.superhero_name
    ORDER BY COUNT(hp.power_id) DESC
    LIMIT {TOP}
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(max(10, len(df)*0.8), 6))
    grafica = sns.barplot(x='name', y='powers_count', data=df, palette='viridis')
    
    plt.title(f"TOP {TOP} superhéroes con más poderes")
    plt.ylabel("Cantidad de poderes")
    plt.xlabel("Superhéroes")
    grafica.set_xticklabels(grafica.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")

def get_distribucion_alineaciones_grafico():
    """
    Genera una gráfica de torta con la distribución de alineaciones de superhéroes
    """
    query = """
    SELECT a.alignment, 
           COUNT(s.id) as hero_count
    FROM alignment a
    JOIN superhero s ON a.id = s.alignment_id
    GROUP BY a.alignment
    ORDER BY COUNT(s.id) DESC
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(10, 8))
    plt.pie(df['hero_count'].values, autopct=lambda p: f'{p:.1f}%', startangle=90, 
            colors=sns.color_palette("Set2", len(df)), shadow=True)
    plt.legend(df['alignment'], loc="best")
    plt.axis('equal')
    plt.title("Distribución de superhéroes por alineación")
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")

def get_distribucion_generos_grafico():
    """
    Genera una gráfica de torta con la distribución de géneros de superhéroes
    """
    query = """
    SELECT g.gender, 
           COUNT(s.id) as hero_count
    FROM gender g
    JOIN superhero s ON g.id = s.gender_id
    GROUP BY g.gender
    ORDER BY COUNT(s.id) DESC
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(10, 8))
    colors = sns.color_palette("pastel", len(df))
    plt.pie(df['hero_count'].values, autopct=lambda p: f'{p:.1f}%', startangle=90, 
            colors=colors, shadow=True)
    plt.legend(df['gender'], loc="best")
    plt.axis('equal')
    plt.title("Distribución de superhéroes por género")
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")

def get_top_poderes_grafico(TOP):
    """
    Genera una gráfica de barras horizontales con los TOP poderes más comunes
    """
    query = f"""
    SELECT sp.power_name as power, 
           COUNT(hp.hero_id) as hero_count
    FROM superpower sp
    JOIN hero_power hp ON sp.id = hp.power_id
    GROUP BY sp.power_name
    ORDER BY COUNT(hp.hero_id) DESC
    LIMIT {TOP}
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(12, max(6, len(df)*0.4)))
    grafica = sns.barplot(y='power', x='hero_count', data=df, palette='magma')
    
    plt.title(f"TOP {TOP} poderes más comunes")
    plt.xlabel("Cantidad de superhéroes")
    plt.ylabel("Poder")
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")

def get_publisher_por_alineacion_grafico(TOP):
    """
    Genera una gráfica de barras apiladas con los TOP editoriales y las alineaciones de sus superhéroes
    """
    query = f"""
    SELECT p.publisher_name as publisher, 
           a.alignment,
           COUNT(s.id) as hero_count
    FROM publisher p
    JOIN superhero s ON p.id = s.publisher_id
    JOIN alignment a ON s.alignment_id = a.id
    GROUP BY p.publisher_name, a.alignment
    ORDER BY COUNT(s.id) DESC
    """
    
    df = pd.read_sql(query, engine)
    
    # Pivotear los datos para obtener alineaciones como columnas
    pivot_df = df.pivot_table(index='publisher', columns='alignment', values='hero_count', aggfunc='sum')
    
    # Ordenar por total de superhéroes y tomar TOP
    pivot_df['total'] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values('total', ascending=False).head(TOP)
    pivot_df = pivot_df.drop('total', axis=1)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlabel("Editorial")
    ax.set_ylabel("Cantidad de superhéroes")
    
    # Crear la paleta de colores
    colors = sns.color_palette("bright", pivot_df.shape[1])
    
    # Crear la gráfica de barras apiladas
    pivot_df.plot(kind='bar', stacked=True, ax=ax, color=colors)
    
    plt.xticks(rotation=45, ha='right')
    plt.title(f"TOP {TOP} editoriales por alineación de superhéroes")
    plt.tight_layout()
    plt.legend(title="Alineación")
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")

def get_distribucion_caracteristicas_grafico():
    """
    Genera un conjunto de gráficos para la distribución de características físicas
    """
    # Consulta para color de ojos
    eyes_query = """
    SELECT c.colour as eye_color, 
           COUNT(s.id) as hero_count
    FROM colour c
    JOIN superhero s ON c.id = s.eye_colour_id
    GROUP BY c.colour
    ORDER BY COUNT(s.id) DESC
    LIMIT 10
    """
    
    # Consulta para color de cabello
    hair_query = """
    SELECT c.colour as hair_color, 
           COUNT(s.id) as hero_count
    FROM colour c
    JOIN superhero s ON c.id = s.hair_colour_id
    GROUP BY c.colour
    ORDER BY COUNT(s.id) DESC
    LIMIT 10
    """
    
    # Consulta para color de piel
    skin_query = """
    SELECT c.colour as skin_color, 
           COUNT(s.id) as hero_count
    FROM colour c
    JOIN superhero s ON c.id = s.skin_colour_id
    GROUP BY c.colour
    ORDER BY COUNT(s.id) DESC
    LIMIT 10
    """
    
    eyes_df = pd.read_sql(eyes_query, engine)
    hair_df = pd.read_sql(hair_query, engine)
    skin_df = pd.read_sql(skin_query, engine)
    
    # Crear figura con subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Gráfico para color de ojos
    sns.barplot(x='eye_color', y='hero_count', data=eyes_df, ax=axes[0], palette='Blues_d')
    axes[0].set_title('Color de ojos más comunes')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
    
    # Gráfico para color de cabello
    sns.barplot(x='hair_color', y='hero_count', data=hair_df, ax=axes[1], palette='Reds_d')
    axes[1].set_title('Color de cabello más comunes')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
    
    # Gráfico para color de piel
    sns.barplot(x='skin_color', y='hero_count', data=skin_df, ax=axes[2], palette='Greens_d')
    axes[2].set_title('Color de piel más comunes')
    axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")

def get_alturas_pesos_superheroes_grafico():
    """
    Genera un scatterplot comparando altura y peso de superhéroes
    """
    query = """
    SELECT s.superhero_name, 
           s.height_cm, 
           s.weight_kg,
           a.alignment,
           g.gender
    FROM superhero s
    JOIN alignment a ON s.alignment_id = a.id
    JOIN gender g ON s.gender_id = g.id
    WHERE s.height_cm IS NOT NULL AND s.weight_kg IS NOT NULL
    LIMIT 100
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(12, 8))
    
    sns.scatterplot(
        x="height_cm", 
        y="weight_kg", 
        hue="alignment", 
        style="gender",
        s=100,
        data=df
    )
    
    plt.title("Relación entre altura y peso de superhéroes")
    plt.xlabel("Altura (cm)")
    plt.ylabel("Peso (kg)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return Response(content=buffer.read(), media_type="image/png")