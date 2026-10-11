import os
import sqlite3
import json
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv

# Cargar variables de entorno de .env
load_dotenv()

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parent.parent / "recipes.db"

def get_cleaned_database_url() -> Optional[str]:
    candidates = [
        "DATABASE_URL", "POSTGRES_URL", "POSTGRESQL_URL",
        "NEON_DATABASE_URL", "DATABASE_URI", "DB_URL"
    ]
    raw = None
    for key in candidates:
        v = os.environ.get(key)
        if v and v.strip():
            raw = v.strip()
            break
            
    if not raw:
        for k, v in os.environ.items():
            if isinstance(v, str) and ("postgres://" in v or "postgresql://" in v):
                raw = v.strip()
                break

    if not raw:
        return None

    raw = raw.strip("'\"` \t\r\n")
    if raw.startswith("psql "):
        raw = raw[5:].strip().strip("'\"` \t\r\n")
    if raw.startswith("psql:"):
        raw = raw[5:].strip().strip("'\"` \t\r\n")
    if "=" in raw and not raw.startswith("postgres"):
        parts = raw.split("=", 1)
        if len(parts) > 1 and "postgres" in parts[1]:
            raw = parts[1].strip().strip("'\"` \t\r\n")
    if raw.startswith("postgres://"):
        raw = raw.replace("postgres://", "postgresql://", 1)

    return raw

CLEAN_DATABASE_URL = get_cleaned_database_url()
IS_POSTGRES = False

if CLEAN_DATABASE_URL:
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        test_conn = psycopg2.connect(CLEAN_DATABASE_URL, connect_timeout=6)
        test_conn.close()
        IS_POSTGRES = True
        logger.info("[DATABASE] Conectado exitosamente a PostgreSQL en la nube (Neon).")
    except Exception as e:
        logger.warning(f"[DATABASE] ADVERTENCIA: Falló conexión a PostgreSQL: {e}. Usando SQLite local.")
        IS_POSTGRES = False
else:
    logger.info("[DATABASE] Usando SQLite local.")

def get_connection():
    if IS_POSTGRES:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        return psycopg2.connect(CLEAN_DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_connection()
    try:
        cur = conn.cursor()
        if IS_POSTGRES:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    source_type TEXT,
                    category TEXT,
                    calories REAL,
                    protein REAL,
                    carbs REAL,
                    fats REAL,
                    nutri_score TEXT,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS custom_foods (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    brand TEXT,
                    category TEXT,
                    serving_size_g REAL,
                    calories REAL,
                    protein REAL,
                    carbs REAL,
                    fats REAL,
                    fiber REAL,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            conn.commit()
        else:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    source_type TEXT,
                    category TEXT,
                    calories REAL,
                    protein REAL,
                    carbs REAL,
                    fats REAL,
                    nutri_score TEXT,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            try:
                cur.execute("ALTER TABLE recipes ADD COLUMN category TEXT")
            except Exception:
                pass

            cur.execute("""
                CREATE TABLE IF NOT EXISTS custom_foods (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    brand TEXT,
                    category TEXT,
                    serving_size_g REAL,
                    calories REAL,
                    protein REAL,
                    carbs REAL,
                    fats REAL,
                    fiber REAL,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            conn.commit()
    finally:
        conn.close()

    # Si la base de datos está vacía, sembrar o migrar
    if count_recipes() == 0:
        if IS_POSTGRES and DB_PATH.exists():
            # Si estamos en Neon y tenemos el SQLite local con datos, migrar automáticamente
            migrated = migrate_sqlite_to_postgres()
            if migrated == 0:
                seed_starter_recipes()
        else:
            seed_starter_recipes()

    if count_custom_foods() == 0:
        if IS_POSTGRES and DB_PATH.exists():
            migrate_custom_foods_from_sqlite()
        if count_custom_foods() == 0:
            seed_starter_foods()

def count_recipes() -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM recipes")
        row = cur.fetchone()
        return row[0] if isinstance(row, tuple) else list(row.values())[0]
    finally:
        conn.close()

def list_recipes() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT data_json FROM recipes ORDER BY created_at DESC")
        rows = cur.fetchall()
        result = []
        for row in rows:
            val = row[0] if isinstance(row, tuple) else row["data_json"]
            result.append(json.loads(val))
        return result
    finally:
        conn.close()

def get_recipe(recipe_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        param_char = "%s" if IS_POSTGRES else "?"
        cur.execute(f"SELECT data_json FROM recipes WHERE id = {param_char}", (recipe_id,))
        row = cur.fetchone()
        if row:
            val = row[0] if isinstance(row, tuple) else row["data_json"]
            return json.loads(val)
        return None
    finally:
        conn.close()

def save_recipe(recipe_data: Dict[str, Any]) -> Dict[str, Any]:
    if not recipe_data.get("id"):
        recipe_data["id"] = str(uuid.uuid4())
    if not recipe_data.get("created_at"):
        recipe_data["created_at"] = datetime.now().isoformat()

    recipe_id = recipe_data["id"]
    title = recipe_data.get("title", "Receta sin título")
    source_type = recipe_data.get("source_type", "text")

    raw_cat = str(recipe_data.get("category") or "comida").lower().strip()
    if "desayun" in raw_cat:
        category = "desayuno"
    elif any(k in raw_cat for k in ["postre", "meriend", "snack", "dulce", "batido", "helado", "galleta"]):
        category = "merienda-postre"
    elif "cen" in raw_cat:
        category = "cena"
    else:
        category = "comida"
    recipe_data["category"] = category

    src_ref = str(recipe_data.get("source_reference") or "")
    if not recipe_data.get("video_url") and (src_ref.startswith("http://") or src_ref.startswith("https://")):
        recipe_data["video_url"] = src_ref

    per_serving = recipe_data.get("per_serving", {})
    calories = per_serving.get("calories", 0.0)
    protein = per_serving.get("protein", 0.0)
    carbs = per_serving.get("carbohydrates", 0.0)
    fats = per_serving.get("fats", 0.0)
    nutri_score = recipe_data.get("nutri_score", "B")

    data_json = json.dumps(recipe_data, ensure_ascii=False)
    created_at = recipe_data["created_at"]

    conn = get_connection()
    try:
        cur = conn.cursor()
        if IS_POSTGRES:
            cur.execute("""
                INSERT INTO recipes 
                (id, title, source_type, category, calories, protein, carbs, fats, nutri_score, data_json, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    source_type = EXCLUDED.source_type,
                    category = EXCLUDED.category,
                    calories = EXCLUDED.calories,
                    protein = EXCLUDED.protein,
                    carbs = EXCLUDED.carbs,
                    fats = EXCLUDED.fats,
                    nutri_score = EXCLUDED.nutri_score,
                    data_json = EXCLUDED.data_json,
                    created_at = EXCLUDED.created_at
            """, (recipe_id, title, source_type, category, calories, protein, carbs, fats, nutri_score, data_json, created_at))
        else:
            cur.execute("""
                INSERT OR REPLACE INTO recipes 
                (id, title, source_type, category, calories, protein, carbs, fats, nutri_score, data_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (recipe_id, title, source_type, category, calories, protein, carbs, fats, nutri_score, data_json, created_at))
        conn.commit()
    finally:
        conn.close()

    return recipe_data

def delete_recipe(recipe_id: str) -> bool:
    conn = get_connection()
    try:
        cur = conn.cursor()
        param_char = "%s" if IS_POSTGRES else "?"
        cur.execute(f"DELETE FROM recipes WHERE id = {param_char}", (recipe_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()

def count_custom_foods() -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM custom_foods")
        row = cur.fetchone()
        return row[0] if isinstance(row, tuple) else list(row.values())[0]
    finally:
        conn.close()

def list_custom_foods() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT data_json FROM custom_foods ORDER BY name ASC")
        rows = cur.fetchall()
        result = []
        for row in rows:
            val = row[0] if isinstance(row, tuple) else row["data_json"]
            result.append(json.loads(val))
        return result
    finally:
        conn.close()

def get_custom_food(food_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        param_char = "%s" if IS_POSTGRES else "?"
        cur.execute(f"SELECT data_json FROM custom_foods WHERE id = {param_char}", (food_id,))
        row = cur.fetchone()
        if row:
            val = row[0] if isinstance(row, tuple) else row["data_json"]
            return json.loads(val)
        return None
    finally:
        conn.close()

def save_custom_food(food_data: Dict[str, Any]) -> Dict[str, Any]:
    if not food_data.get("id"):
        food_data["id"] = str(uuid.uuid4())
    if not food_data.get("created_at"):
        food_data["created_at"] = datetime.now().isoformat()

    food_id = food_data["id"]
    name = str(food_data.get("name") or "Alimento sin nombre").strip()
    brand = food_data.get("brand") or ""
    category = str(food_data.get("category") or "despensa").lower().strip()
    serving_size_g = float(food_data.get("serving_size_g") or 100.0)
    calories = float(food_data.get("calories") or 0.0)
    protein = float(food_data.get("protein") or 0.0)
    carbs = float(food_data.get("carbohydrates") if food_data.get("carbohydrates") is not None else food_data.get("carbs", 0.0))
    fats = float(food_data.get("fats") if food_data.get("fats") is not None else food_data.get("fat", 0.0))
    fiber = float(food_data.get("fiber") or 0.0)

    food_data["carbohydrates"] = carbs
    food_data["fats"] = fats
    data_json = json.dumps(food_data, ensure_ascii=False)
    created_at = food_data["created_at"]

    conn = get_connection()
    try:
        cur = conn.cursor()
        if IS_POSTGRES:
            cur.execute("""
                INSERT INTO custom_foods
                (id, name, brand, category, serving_size_g, calories, protein, carbs, fats, fiber, data_json, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    brand = EXCLUDED.brand,
                    category = EXCLUDED.category,
                    serving_size_g = EXCLUDED.serving_size_g,
                    calories = EXCLUDED.calories,
                    protein = EXCLUDED.protein,
                    carbs = EXCLUDED.carbs,
                    fats = EXCLUDED.fats,
                    fiber = EXCLUDED.fiber,
                    data_json = EXCLUDED.data_json,
                    created_at = EXCLUDED.created_at
            """, (food_id, name, brand, category, serving_size_g, calories, protein, carbs, fats, fiber, data_json, created_at))
        else:
            cur.execute("""
                INSERT OR REPLACE INTO custom_foods
                (id, name, brand, category, serving_size_g, calories, protein, carbs, fats, fiber, data_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (food_id, name, brand, category, serving_size_g, calories, protein, carbs, fats, fiber, data_json, created_at))
        conn.commit()
    finally:
        conn.close()

    return food_data

def delete_custom_food(food_id: str) -> bool:
    conn = get_connection()
    try:
        cur = conn.cursor()
        param_char = "%s" if IS_POSTGRES else "?"
        cur.execute(f"DELETE FROM custom_foods WHERE id = {param_char}", (food_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()

# Migración de SQLite local a Neon PostgreSQL
def migrate_sqlite_to_postgres() -> int:
    if not DB_PATH.exists():
        logger.warning(f"No existe base de datos SQLite local en {DB_PATH}")
        return 0
    
    try:
        s_conn = sqlite3.connect(DB_PATH)
        s_conn.row_factory = sqlite3.Row
        s_cur = s_conn.cursor()
        s_cur.execute("SELECT * FROM recipes")
        rows = s_cur.fetchall()
        s_conn.close()
    except Exception as e:
        logger.error(f"Error leyendo SQLite: {e}")
        return 0

    count = 0
    for r in rows:
        try:
            data = json.loads(r["data_json"])
            save_recipe(data)
            count += 1
        except Exception as e:
            logger.warning(f"Error migrando receta {r['id']}: {e}")

    logger.info(f"[MIGRACIÓN] Se han migrado {count} recetas desde SQLite a Neon.")
    return count

def migrate_custom_foods_from_sqlite() -> int:
    if not DB_PATH.exists():
        return 0
    try:
        s_conn = sqlite3.connect(DB_PATH)
        s_conn.row_factory = sqlite3.Row
        s_cur = s_conn.cursor()
        s_cur.execute("SELECT * FROM custom_foods")
        rows = s_cur.fetchall()
        s_conn.close()
    except Exception as e:
        return 0

    count = 0
    for r in rows:
        try:
            data = json.loads(r["data_json"])
            save_custom_food(data)
            count += 1
        except Exception as e:
            pass

    logger.info(f"[MIGRACIÓN] Se han migrado {count} alimentos desde SQLite a Neon.")
    return count

def seed_starter_recipes():
    starter_recipes = [
        {
            "id": "starter-salmon-bowl",
            "title": "Bowl Fitness de Salmón, Quinoa y Aguacate",
            "description": "Un plato completo y equilibrado cargado de ácidos grasos Omega-3, proteína de alto valor biológico y carbohidratos complejos.",
            "servings": 2,
            "prep_time_minutes": 15,
            "cook_time_minutes": 20,
            "source_type": "ai_generated",
            "source_reference": "Receta Saludable Recomendada",
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700&auto=format&fit=crop&q=80",
            "ingredients": [
                {"name": "Lomo de salmón fresco", "amount": "300g", "calories": 624, "protein": 60, "carbs": 0, "fat": 40, "notes": "Rico en Omega-3"},
                {"name": "Quinoa cocida", "amount": "200g", "calories": 240, "protein": 8.8, "carbs": 42.6, "fat": 3.8, "notes": "Carbohidratos de bajo índice glucémico"},
                {"name": "Aguacate maduro", "amount": "100g (medio)", "calories": 160, "protein": 2, "carbs": 8.5, "fat": 14.7, "notes": "Grasas monoinsaturadas cardiosaludables"},
                {"name": "Pepino en rodajas", "amount": "100g", "calories": 15, "protein": 0.7, "carbs": 3.6, "fat": 0.1, "notes": "Alto contenido en agua y fibra"},
                {"name": "Edamame desgranado", "amount": "80g", "calories": 96, "protein": 9.5, "carbs": 7.1, "fat": 4.2, "notes": "Proteína vegetal extra"},
                {"name": "Salsa de soja baja en sal y sésamo", "amount": "2 cucharadas", "calories": 30, "protein": 1.5, "carbs": 2.5, "fat": 1.2, "notes": "Aliño ligero"}
            ],
            "instructions": [
                "Cocer la quinoa en abundante agua con sal durante 12-14 minutos. Escurrir y enfriar.",
                "Marcar el salmón a la plancha a fuego medio-alto durante 3-4 minutos por lado hasta que quede dorado por fuera y jugoso por dentro.",
                "Cortar el salmón y el aguacate en dados medianos y el pepino en rodajas finas.",
                "Montar los bowls colocando una base de quinoa, los dados de salmón, aguacate, pepino y edamame.",
                "Rociar con salsa de soja baja en sodio y espolvorear semillas de sésamo tostadas."
            ],
            "per_serving": {
                "calories": 582.5,
                "protein": 41.2,
                "carbohydrates": 32.1,
                "fats": 31.9,
                "fiber": 7.8,
                "sugar": 3.2,
                "sodium": 420.0,
                "saturated_fat": 5.2,
                "cholesterol": 78.0,
                "potassium": 820.0,
                "vitamins_and_minerals": ["Vitamina D: 14mcg", "Vitamina B12: 4.8mcg", "Magnesio: 110mg", "Hierro: 3.4mg"]
            },
            "total": {
                "calories": 1165.0,
                "protein": 82.4,
                "carbohydrates": 64.2,
                "fats": 63.8,
                "fiber": 15.6,
                "sugar": 6.4,
                "sodium": 840.0,
                "saturated_fat": 10.4,
                "cholesterol": 156.0,
                "potassium": 1640.0,
                "vitamins_and_minerals": ["Vitamina D: 28mcg", "Vitamina B12: 9.6mcg", "Magnesio: 220mg", "Hierro: 6.8mg"]
            },
            "nutri_score": "A",
            "dietary_tags": ["Alta en proteína", "Rica en Omega-3", "Sin gluten", "Carbohidratos complejos"],
            "health_verdict": "Excelente perfil nutricional. Gran densidad de micronutrientes y aporte equilibrado de macronutrientes. Ideal tanto para deportistas como para comidas saciantes en pérdida de grasa o mantenimiento.",
            "healthier_alternatives": [
                "Para reducir aún más las calorías, reducir a 1/4 de aguacate o usar salsa de yogur 0% con limón en vez de semillas adicionales."
            ],
            "created_at": "2026-10-10T10:00:00"
        }
    ]
    for r in starter_recipes:
        save_recipe(r)

def seed_starter_foods():
    starter_foods = [
        {
            "name": "Pechuga de pollo limpia",
            "brand": "Genérico / Carnicería",
            "category": "proteina",
            "serving_size_g": 100.0,
            "calories": 120.0,
            "protein": 23.5,
            "carbohydrates": 0.0,
            "fats": 2.5,
            "fiber": 0.0,
            "notes": "Proteína magra de alto valor biológico"
        },
        {
            "name": "Huevos camperos enteros",
            "brand": "Clase L",
            "category": "proteina",
            "serving_size_g": 100.0,
            "calories": 143.0,
            "protein": 12.8,
            "carbohydrates": 0.7,
            "fats": 9.9,
            "fiber": 0.0,
            "notes": "Aprox. 2 unidades medianas"
        },
        {
            "name": "Copos de avena integral",
            "brand": "Hacendado / Mercadona",
            "category": "carbohidrato",
            "serving_size_g": 100.0,
            "calories": 375.0,
            "protein": 13.5,
            "carbohydrates": 58.7,
            "fats": 7.0,
            "fiber": 10.0,
            "notes": "Carbohidrato saciante y rico en fibra"
        },
        {
            "name": "Aceite de Oliva Virgen Extra (AOVE)",
            "brand": "Nacional",
            "category": "grasa",
            "serving_size_g": 100.0,
            "calories": 884.0,
            "protein": 0.0,
            "carbohydrates": 0.0,
            "fats": 100.0,
            "fiber": 0.0,
            "notes": "1 cucharada sopera = 10g (~90 kcal)"
        }
    ]
    for f in starter_foods:
        save_custom_food(f)
