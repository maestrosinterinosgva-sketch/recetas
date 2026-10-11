import os
import shutil
import uuid
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import get_gemini_api_key, set_gemini_api_key
from app.models import (
    Recipe, RecipeTextRequest, RecipeUrlRequest, 
    ComparisonRequest, ComparisonResult,
    SuggestionRequest, SuggestionResponse,
    CustomFood, FoodEstimateRequest, PantryRecipeRequest
)
from app.database import (
    init_db, list_recipes, get_recipe, save_recipe, delete_recipe,
    list_custom_foods, get_custom_food, save_custom_food, delete_custom_food
)
from app.gemini_service import (
    analyze_recipe_from_text,
    analyze_recipe_from_image,
    analyze_recipe_from_video_file,
    analyze_recipe_from_social_metadata,
    suggest_recipes_by_nutrition,
    compare_recipes_nutrition,
    estimate_food_nutrition,
    suggest_recipe_from_pantry,
    optimize_image_bytes
)
from app.media_service import download_social_video_or_info, cleanup_file

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base directories
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Initialize FastAPI
app = FastAPI(
    title="NutriChef AI - Analizador & Comparador Nutricional de Recetas",
    description="Analiza recetas desde texto, fotos o vídeos de redes sociales, compara perfiles nutricionales y recibe sugerencias inteligentes.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Startup event
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Base de datos y directorios inicializados con éxito.")

# Web Page Route
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    index_file = BASE_DIR / "templates" / "index.html"
    return FileResponse(str(index_file))

# API Routes: Config
class ApiKeyPayload(BaseModel):
    api_key: str

@app.get("/api/config")
async def get_config():
    key = get_gemini_api_key()
    has_key = bool(key and len(key) > 5)
    masked_key = f"{key[:4]}...{key[-4:]}" if has_key else ""
    return {
        "has_api_key": has_key,
        "masked_key": masked_key,
        "model": "Gemini AI (Multi-modelo activo)"
    }

@app.post("/api/config")
async def save_config(payload: ApiKeyPayload):
    set_gemini_api_key(payload.api_key)
    return {
        "success": True, 
        "message": "Clave API de Gemini guardada correctamente.",
        "has_api_key": bool(payload.api_key.strip())
    }

# API Routes: Recipes CRUD
@app.get("/api/recipes", response_model=List[Dict[str, Any]])
async def api_get_recipes():
    return list_recipes()

@app.get("/api/recipes/{recipe_id}")
async def api_get_recipe(recipe_id: str):
    recipe = get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return recipe

@app.post("/api/recipes")
async def api_save_recipe(recipe: Recipe):
    recipe_dict = recipe.model_dump()
    saved = save_recipe(recipe_dict)
    return saved

@app.delete("/api/recipes/{recipe_id}")
async def api_delete_recipe(recipe_id: str):
    deleted = delete_recipe(recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"success": True, "message": "Receta eliminada correctamente."}

@app.post("/api/recipes/{recipe_id}/image")
async def api_update_recipe_image(
    recipe_id: str,
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None)
):
    recipe = get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
        
    new_image_url = None
    if file and file.filename:
        file_bytes = await file.read()
        if len(file_bytes) > 0:
            opt_bytes, ext = optimize_image_bytes(file_bytes)
            img_name = f"recipe_{recipe_id}_{uuid.uuid4().hex[:6]}{ext}"
            img_path = UPLOADS_DIR / img_name
            with open(img_path, "wb") as f:
                f.write(opt_bytes)
            new_image_url = f"/uploads/{img_name}"
    elif image_url and image_url.strip():
        new_image_url = image_url.strip()
        
    if not new_image_url:
        raise HTTPException(status_code=400, detail="Debes proporcionar un archivo de imagen o una URL válida.")
        
    recipe["image_url"] = new_image_url
    saved = save_recipe(recipe)
    return {"success": True, "image_url": new_image_url, "recipe": saved}

# API Routes: Analyze Recipes
@app.post("/api/analyze/text", response_model=Recipe)
async def api_analyze_text(payload: RecipeTextRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="El texto de la receta no puede estar vacío.")
    try:
        recipe = analyze_recipe_from_text(payload.text)
        return recipe
    except Exception as e:
        logger.error(f"Error analizando texto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/image", response_model=Recipe)
async def api_analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo subido debe ser una imagen válida.")
    
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="El archivo de imagen está vacío.")
        
    # Guardar imagen para que quede asociada a la receta
    file_ext = Path(file.filename).suffix or ".jpg"
    img_name = f"photo_{uuid.uuid4().hex[:10]}{file_ext}"
    img_path = UPLOADS_DIR / img_name
    with open(img_path, "wb") as f:
        f.write(file_bytes)

    try:
        recipe = analyze_recipe_from_image(
            image_bytes=file_bytes,
            mime_type=file.content_type,
            file_name=file.filename
        )
        recipe.image_url = f"/uploads/{img_name}"
        return recipe
    except Exception as e:
        logger.error(f"Error analizando imagen: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/video", response_model=Recipe)
async def api_analyze_video(
    file: UploadFile = File(...),
    thumbnail: Optional[UploadFile] = File(None)
):
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = UPLOADS_DIR / temp_filename
    
    thumb_url = None
    if thumbnail:
        try:
            thumb_ext = Path(thumbnail.filename).suffix or ".jpg"
            thumb_name = f"thumb_{uuid.uuid4().hex[:10]}{thumb_ext}"
            thumb_path = UPLOADS_DIR / thumb_name
            thumb_bytes = await thumbnail.read()
            if len(thumb_bytes) > 200:
                with open(thumb_path, "wb") as f:
                    f.write(thumb_bytes)
                thumb_url = f"/uploads/{thumb_name}"
        except Exception as e:
            logger.warning(f"No se pudo guardar la miniatura del vídeo: {e}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        recipe = analyze_recipe_from_video_file(str(temp_path), file_name=file.filename)
        if thumb_url:
            recipe.image_url = thumb_url
        return recipe
    except Exception as e:
        logger.error(f"Error analizando vídeo: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup_file(str(temp_path))

@app.post("/api/analyze/url", response_model=Recipe)
async def api_analyze_url(payload: RecipeUrlRequest):
    if not payload.url.strip():
        raise HTTPException(status_code=400, detail="La URL no puede estar vacía.")
        
    logger.info(f"Procesando enlace de red social: {payload.url}")
    result = download_social_video_or_info(payload.url)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=f"No se pudo extraer el vídeo: {result.get('error', 'Error desconocido')}")
        
    video_path = result.get("video_path")
    try:
        recipe = analyze_recipe_from_social_metadata(
            url=payload.url,
            metadata=result,
            video_path=video_path
        )
        return recipe
    except Exception as e:
        logger.error(f"Error analizando enlace social: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if video_path:
            cleanup_file(video_path)

# API Routes: Comparison
@app.post("/api/compare", response_model=ComparisonResult)
async def api_compare_recipes(payload: ComparisonRequest):
    recipes = []
    for rid in payload.recipe_ids:
        r_dict = get_recipe(rid)
        if r_dict:
            recipes.append(Recipe(**r_dict))
            
    if len(recipes) < 2:
        raise HTTPException(status_code=400, detail="Debes seleccionar al menos 2 recetas válidas para comparar.")
        
    result = compare_recipes_nutrition(recipes)
    return result

# API Routes: Suggest Recipes by Targets
@app.post("/api/suggest", response_model=SuggestionResponse)
async def api_suggest_recipes(payload: SuggestionRequest):
    suggestions = suggest_recipes_by_nutrition(payload)
    return SuggestionResponse(suggestions=suggestions)

# API Routes: Custom Foods / Pantry
@app.get("/api/foods")
async def api_list_custom_foods():
    return list_custom_foods()

@app.post("/api/foods")
async def api_save_custom_food(food: CustomFood):
    saved = save_custom_food(food.model_dump())
    return saved

@app.delete("/api/foods/{food_id}")
async def api_delete_custom_food(food_id: str):
    success = delete_custom_food(food_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return {"status": "deleted", "id": food_id}

@app.post("/api/foods/estimate", response_model=CustomFood)
async def api_estimate_food(payload: FoodEstimateRequest):
    return estimate_food_nutrition(payload.name, payload.brand)

# API Route: Pantry Recipes (Cook with what's at home)
@app.post("/api/suggest/pantry", response_model=SuggestionResponse)
async def api_suggest_from_pantry(payload: PantryRecipeRequest):
    pantry_foods = list_custom_foods()
    suggestions = suggest_recipe_from_pantry(payload, pantry_foods)
    return SuggestionResponse(suggestions=suggestions)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
