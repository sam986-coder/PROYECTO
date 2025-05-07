#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import create_engine, text, inspect
import sys
import time

def test_db_connections():
    """
    Prueba las conexiones a la base de datos utilizando diferentes métodos
    y muestra información detallada sobre el estado de la base de datos
    """
    print("="*80)
    print("VERIFICADOR DE CONEXIÓN A LA BASE DE DATOS DE SUPERHÉROES")
    print("="*80)
    
    # Lista de posibles conexiones a probar
    connection_configs = [
        {
            "method": "Docker",
            "host": "db",
            "port": 3306,
            "sqlalchemy_uri": "mysql+pymysql://root:rootpassword@db:3306/superheroes"
        },
        {
            "method": "Local",
            "host": "localhost",
            "port": 3309,
            "sqlalchemy_uri": "mysql+pymysql://root:rootpassword@localhost:3309/superheroes"
        }
    ]
    
    success = False
    
    for config in connection_configs:
        print(f"\nIntentando conexión a través de {config['method']} - {config['host']}:{config['port']}")
        print("-"*50)
        
        # Intento con PyMySQL directo
        try:
            conn = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user='root',
                password='rootpassword',
                database='superheroes'
            )
            print(f"✅ Conexión PyMySQL directa: EXITOSA")
            
            # Verificar tablas
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"   Tablas encontradas: {len(tables)}")
                if len(tables) == 0:
                    print("   ⚠️  ADVERTENCIA: La base de datos existe pero no contiene tablas.")
                else:
                    print("   Tablas disponibles:")
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                        count = cursor.fetchone()[0]
                        print(f"   - {table[0]}: {count} registros")
            
            conn.close()
            success = True
        except Exception as e:
            print(f"❌ Conexión PyMySQL directa: FALLIDA")
            print(f"   Error: {str(e)}")
        
        # Intento con SQLAlchemy
        try:
            engine = create_engine(config['sqlalchemy_uri'])
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print(f"✅ Conexión SQLAlchemy: EXITOSA")
                
                # Obtener esquema
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                print(f"   Tablas encontradas: {len(tables)}")
                
                if len(tables) == 0:
                    print("   ⚠️  ADVERTENCIA: La base de datos existe pero no contiene tablas.")
                    print("   Puedes inicializar las tablas usando el script SQL proporcionado.")
                else:
                    print("   Intentando consulta de prueba para cada tabla:")
                    for table in tables:
                        try:
                            df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", connection)
                            print(f"   ✅ Tabla {table}: Accesible")
                            columns = inspector.get_columns(table)
                            print(f"      Columnas: {', '.join([col['name'] for col in columns])}")
                        except Exception as e:
                            print(f"   ❌ Tabla {table}: Error al acceder - {str(e)}")
            
            # Si llegamos aquí sin errores
            success = True
            break
        except Exception as e:
            print(f"❌ Conexión SQLAlchemy: FALLIDA")
            print(f"   Error: {str(e)}")
    
    print("\n" + "="*80)
    if success:
        print("✅ CONEXIÓN EXITOSA A LA BASE DE DATOS")
        if "tablas encontradas: 0" in locals():
            print("\n⚠️  RECOMENDACIÓN: Inicializa la base de datos con las tablas necesarias")
            print("   usando el script SQL 'init_superheroes_db.sql' proporcionado.")
    else:
        print("❌ NO SE PUDO CONECTAR A LA BASE DE DATOS")
        print("\nRecomendaciones:")
        print("1. Verifica que los contenedores Docker estén en ejecución:")
        print("   docker-compose ps")
        print("2. Reinicia los servicios:")
        print("   docker-compose down")
        print("   docker-compose up -d")
        print("3. Verifica los logs para errores:")
        print("   docker-compose logs db")
        print("4. Ejecuta el script de inicialización de la base de datos en phpMyAdmin")
    print("="*80)

if __name__ == "__main__":
    print("Esperando unos segundos para que los servicios se inicialicen completamente...")
    time.sleep(3)
    try:
        test_db_connections()
    except Exception as e:
        print(f"Error general: {str(e)}")
        sys.exit(1)