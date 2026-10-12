import os
import re
import json
import time
import logging
import uuid
import base64
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

from app.config import get_gemini_api_key, UPLOADS_DIR
from app.models import (
    Recipe, ComparisonResult, SuggestionRequest, SuggestionResponse, 
    NutrientInfo, Ingredient, CustomFood, PantryRecipeRequest
)

logger = logging.getLogger(__name__)

def extract_clean_recipe_title(title: str, description: str, source: str = "Red Social") -> str:
    """Extrae un título representativo a partir del título o la descripción de la publicación."""
    generic_prefixes = ["video by", "reel by", "tiktok by", "post by", "instagram video", "vídeo de", "watch?v="]
    clean_title = (title or "").strip()
    is_generic = not clean_title or any(clean_title.lower().startswith(p) for p in generic_prefixes)

    if is_generic and description:
        first_line = description.strip().split("\n")[0]
        # Limpiar hashtags y URLs
        clean_desc = re.sub(r'#\S+', '', first_line).strip()
        clean_desc = re.sub(r'https?://\S+', '', clean_desc).strip()
        if len(clean_desc) >= 3:
            return clean_desc[:70]

    return clean_title if clean_title else f"Receta de {source}"

CULINARY_IMAGE_KEYWORDS = [
    # Categorías específicas de desayunos y repostería primero (evitar que 'avena' o 'fruta' capture tortitas o crepes)
    (["tartar", "aguacate"], "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80"),
    (["tortita", "pancake", "panqueque", "hotcake"], "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=700&auto=format&fit=crop&q=80"),
    (["crepe", "crepes"], "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=700&auto=format&fit=crop&q=80"),
    (["gofre", "waffle"], "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=700&auto=format&fit=crop&q=80"),
    (["banana bread", "pan de plátano", "pan de platano"], "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=700&auto=format&fit=crop&q=80"),
    (["donut", "dona", "rosquilla"], "https://images.unsplash.com/photo-1527515862127-a4fc05baf7a5?w=700&auto=format&fit=crop&q=80"),
    (["biscotti", "galleta", "cookie"], "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=700&auto=format&fit=crop&q=80"),
    (["sandwich", "sándwich", "tosta", "tostada", "bocadillo"], "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=700&auto=format&fit=crop&q=80"),
    (["empanada", "empanadilla"], "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=700&auto=format&fit=crop&q=80"),
    (["quiche", "tarta salada"], "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=700&auto=format&fit=crop&q=80"),
    (["falafel", "faláfel"], "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=700&auto=format&fit=crop&q=80"),
    (["coliflor"], "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=700&auto=format&fit=crop&q=80"),
    (["maki", "sushi"], "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=700&auto=format&fit=crop&q=80"),
    (["berenjena"], "https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?w=700&auto=format&fit=crop&q=80"),
    (["helado", "sorbete", "polo", "polos"], "https://images.unsplash.com/photo-1505394033641-40c6ad1178d7?w=700&auto=format&fit=crop&q=80"),
    (["nugget", "nuggets"], "https://images.unsplash.com/photo-1562967914-608f82629710?w=700&auto=format&fit=crop&q=80"),
    (["salmon", "salmón"], "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700&auto=format&fit=crop&q=80"),
    (["carbonara", "spaghetti", "espagueti", "pasta", "macarron", "tallarin", "lasaña", "lasagna"], "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=700&auto=format&fit=crop&q=80"),
    (["curry", "tikka"], "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=700&auto=format&fit=crop&q=80"),
    (["pollo", "pechuga", "pavo"], "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=700&auto=format&fit=crop&q=80"),
    (["ensalada", "salad", "xató", "xato"], "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=700&auto=format&fit=crop&q=80"),
    (["poke", "bowl"], "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700&auto=format&fit=crop&q=80"),
    (["lubina", "merluza", "bacalao", "pescado", "atun", "atún", "pulpo", "calamar", "marisco", "gamba"], "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80"),
    (["crema", "sopa", "pure", "puré", "gazpacho", "salmorejo", "calabaza"], "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=700&auto=format&fit=crop&q=80"),
    (["tortilla", "huevo", "revuelto", "frittata", "omelet"], "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=700&auto=format&fit=crop&q=80"),
    (["albondiga", "albóndiga", "hamburguesa", "burger", "carne", "ternera", "bife", "solomillo", "lomo"], "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=700&auto=format&fit=crop&q=80"),
    (["arroz", "paella", "risotto", "basmati"], "https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?w=700&auto=format&fit=crop&q=80"),
    (["lenteja", "garbanzo", "alubia", "judia", "judía", "hummus", "legumbre"], "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=700&auto=format&fit=crop&q=80"),
    (["wrap", "fajita", "burrito", "taco", "quesadilla"], "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=700&auto=format&fit=crop&q=80"),
    (["pizza", "focaccia"], "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=700&auto=format&fit=crop&q=80"),
    (["cake", "pastel", "bizcocho", "brownie", "postre", "dulce", "tarta"], "https://images.unsplash.com/photo-1587314168485-3236d6710814?w=700&auto=format&fit=crop&q=80"),
    (["smoothie", "batido", "avena", "porridge", "yogur", "fruta", "desayuno"], "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=700&auto=format&fit=crop&q=80")
]
DEFAULT_CULINARY_IMAGE = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=700&auto=format&fit=crop&q=80"

def get_culinary_image_for_title(title: str) -> str:
    """Devuelve una fotografía gastronómica de alta definición adaptada a la temática de la receta."""
    lower = (title or "").lower()
    for keywords, url in CULINARY_IMAGE_KEYWORDS:
        for k in keywords:
            if k == "tarta" and "tartar" in lower:
                continue
            if k in lower:
                return url
    return DEFAULT_CULINARY_IMAGE

def search_culinary_photos(query: str, limit: int = 8) -> List[Dict[str, str]]:
    """Busca fotografías culinarias de calidad combinando colecciones gastronómicas curadas y Wikimedia Commons."""
    results = []
    seen_urls = set()
    clean_q = (query or "").strip()
    if not clean_q:
        return results

    def add_img(title: str, url: str, source: str = "curated"):
        if url and url not in seen_urls:
            seen_urls.add(url)
            results.append({
                "title": title,
                "url": url,
                "source": source
            })

    lower_q = clean_q.lower()

    # 1. Coincidencia en catálogo curado HD (tomamos la más específica)
    for keywords, url in CULINARY_IMAGE_KEYWORDS:
        matched = False
        for k in keywords:
            if k == "tarta" and "tartar" in lower_q:
                continue
            if k in lower_q:
                matched = True
                break
        if matched:
            tag = keywords[0].capitalize()
            add_img(f"Foto HD recomendada ({tag})", url, "curated")
            break

    # 2. Búsqueda en Wikimedia Commons
    TRANSLATIONS = [
        ("tortitas", "pancakes"), ("tortita", "pancake"), ("panqueques", "pancakes"),
        ("platano", "banana"), ("plátano", "banana"),
        ("avena", "oatmeal"), ("manzana", "apple"),
        ("chocolate", "chocolate"), ("fresas", "strawberries"),
        ("ensalada", "salad"), ("pollo", "chicken"),
        ("lentejas", "lentils"), ("arroz", "rice"),
        ("galletas", "cookies"), ("bizcocho", "cake"),
        ("sopa", "soup"), ("crema", "soup"),
        ("pescado", "fish"), ("salmon", "salmon"), ("salmón", "salmon")
    ]
    eng_q = lower_q
    for es, en in TRANSLATIONS:
        eng_q = eng_q.replace(es, en)

    search_terms = []
    # Generar frases clave en inglés y términos específicos
    if "pancake" in eng_q or "tortita" in lower_q:
        if "banana" in eng_q:
            search_terms.append("banana pancakes")
        search_terms.append("pancakes")
    elif "crepe" in eng_q:
        search_terms.append("crepes")
    elif "waffle" in eng_q or "gofre" in lower_q:
        search_terms.append("waffles")
    elif "falafel" in eng_q:
        search_terms.append("falafel")
    elif "hummus" in eng_q:
        search_terms.append("hummus")

    if eng_q not in search_terms:
        search_terms.append(eng_q)
    if clean_q not in search_terms:
        search_terms.append(clean_q)

    for term in search_terms:
        if len(results) >= limit:
            break
        try:
            params = {
                "action": "query",
                "generator": "search",
                "gsrnamespace": "6",
                "gsrsearch": f"{term} filetype:bitmap",
                "gsrlimit": str(min(6, limit - len(results) + 2)),
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": "700",
                "format": "json"
            }
            url = f"https://commons.wikimedia.org/w/api.php?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers={"User-Agent": "RecetasNutriApp/1.0 (culinary-assistant)"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for p in pages.values():
                    info = p.get("imageinfo", [{}])[0]
                    thumb = info.get("thumburl") or info.get("url")
                    title = p.get("title", "").replace("File:", "").rsplit(".", 1)[0]
                    title = title.replace("_", " ")[:60]
                    if thumb and any(thumb.lower().endswith(ext) or ext in thumb.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                        add_img(title, thumb, "wikimedia")
        except Exception as e:
            logger.warning(f"Error buscando en Wikimedia para '{term}': {e}")

    # Fallback si no hubo resultados
    if not results:
        add_img("Plato gastronómico", DEFAULT_CULINARY_IMAGE, "curated")

    return results[:limit]

def generate_recipe_image_ai(recipe_title: str) -> Dict[str, Any]:
    """Intenta generar una fotografía gastronómica con Google Gemini (requiere cuenta con cuota de generación)."""
    client = get_client()
    if not client:
        return {"success": False, "error": "No hay clave API de Gemini configurada."}

    prompt = f"Professional appetizing culinary studio photograph of {recipe_title}. Gourmet presentation on a clean ceramic plate, warm natural restaurant lighting, high resolution, delicious food photography."
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )
        for part in response.parts:
            if part.inline_data:
                img_data = part.inline_data.data
                ext = ".jpg" if "jpeg" in (part.inline_data.mime_type or "") else ".png"
                img_name = f"ai_gen_{uuid.uuid4().hex[:8]}{ext}"
                img_path = UPLOADS_DIR / img_name
                if isinstance(img_data, str):
                    raw_bytes = base64.b64decode(img_data)
                else:
                    raw_bytes = img_data
                with open(img_path, "wb") as f:
                    f.write(raw_bytes)
                return {"success": True, "image_url": f"/uploads/{img_name}"}
        return {"success": False, "error": "El modelo no generó una imagen en la respuesta."}
    except Exception as e:
        err_msg = str(e)
        logger.warning(f"Error generando imagen con IA: {e}")
        if "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
            return {
                "success": False,
                "error": "Tu cuenta de Gemini API no tiene cuota activa para generación de imágenes (requiere plan de pago en Google AI Studio). Te recomendamos usar la pestaña 'Buscar Foto' para obtener fotos reales instantáneas."
            }
        return {"success": False, "error": f"Error al generar con IA: {err_msg[:120]}"}

RECIPE_ANALYSIS_SYSTEM_PROMPT = """Eres un Nutricionista Clínico y Chef Profesional experto en análisis bromatológico y cálculo nutricional de recetas.
Tu misión es analizar la receta proporcionada (a través de texto, imágenes de platos o ingredientes, o vídeos de cocina) y desglosarla con máxima precisión:

1. Identificar todos los ingredientes con cantidades estimadas exactas (si no se especifican, estima raciones culinarias estándar).
2. Calcular las calorías totales y por porción (Kcal) con precisión científica.
3. Calcular macronutrientes: Proteínas (g), Carbohidratos (g), Grasas totales (g), Grasas saturadas (g), Fibra (g), Azúcares (g) y Sodio (mg).
4. Indicar micronutrientes destacados (vitaminas y minerales clave con cantidad estimada).
5. Determinar el Nutri-Score europeo (A, B, C, D o E) justificado por el balance de nutrientes favorables (fibra, proteína, vegetales) vs desfavorables (azúcar, grasas saturadas, sodio, calorías).
6. Asignar etiquetas dietéticas relevantes (ej: 'Alta en proteína', 'Baja en carbohidratos', 'Keto', 'Vegana', 'Mediterránea', 'Baja en sodio').
7. Proporcionar un veredicto nutricional profesional honesto (puntos fuertes, alertas y a qué objetivos deportivos o de salud se adapta mejor).
8. Ofrecer 2-3 sugerencias concretas de sustituciones o trucos para hacer la receta aún más saludable y ligera.
9. Asignar obligatoriamente la categoría del plato en el campo 'category' eligiendo exactamente uno de estos cuatro valores: 'desayuno', 'comida', 'merienda-postre', o 'cena'.

Debes responder siempre en español y cumplir estrictamente el esquema JSON indicado."""

AVAILABLE_GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite",
]

def optimize_image_bytes(image_bytes: bytes, max_dim: int = 1280) -> tuple[bytes, str]:
    """Comprime y redimensiona imágenes grandes para agilizar transferencia y evitar sobrecarga."""
    try:
        from PIL import Image
        import io
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGB")
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=85, optimize=True)
            return out.getvalue(), "image/jpeg"
    except Exception as e:
        logger.warning(f"No se pudo optimizar la imagen con PIL: {e}. Usando original.")
        return image_bytes, "image/jpeg"

def generate_content_with_fallback(
    client: genai.Client,
    contents: Any,
    system_instruction: str,
    response_json_schema: Optional[Any] = None,
    temperature: float = 0.2
) -> str:
    """Ejecuta generate_content rotando entre modelos si Google devuelve 503 UNAVAILABLE o 429 RESOURCE_EXHAUSTED."""
    last_error = None
    for model_name in AVAILABLE_GEMINI_MODELS:
        try:
            logger.info(f"Invocando Gemini ({model_name})...")
            config_args = {
                "system_instruction": system_instruction,
                "temperature": temperature,
            }
            if response_json_schema:
                config_args["response_mime_type"] = "application/json"
                config_args["response_json_schema"] = response_json_schema

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(**config_args)
            )
            if response and response.text:
                logger.info(f"Respuesta exitosa recibida de {model_name}")
                return response.text
        except Exception as e:
            err_msg = str(e)
            logger.warning(f"Aviso en modelo {model_name} (posible 503/429): {err_msg[:120]}. Probando siguiente modelo...")
            last_error = e
            time.sleep(0.5)

    raise RuntimeError(f"Todos los modelos de Gemini están experimentando alta demanda temporal: {last_error}")

def get_client() -> Optional[genai.Client]:
    api_key = get_gemini_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def analyze_recipe_from_text(text: str) -> Recipe:
    """Analiza una receta proporcionada en formato texto."""
    client = get_client()
    if not client:
        return _mock_recipe_analysis(
            title="Receta Analizada (Modo Demo)",
            source_type="text",
            source_ref="Texto ingresado",
            user_input=text
        )

    prompt = f"Analiza nutricionalmente la siguiente receta o descripción:\n\n{text}"
    
    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[prompt],
            system_instruction=RECIPE_ANALYSIS_SYSTEM_PROMPT,
            response_json_schema=Recipe.model_json_schema(),
            temperature=0.2
        )
        data = json.loads(text_response)
        data["source_type"] = "text"
        data["source_reference"] = "Texto manual"
        if not data.get("image_url"):
            data["image_url"] = get_culinary_image_for_title(data.get("title", ""))
        return Recipe(**data)
    except Exception as e:
        logger.error(f"Error analizando texto con Gemini: {e}")
        recipe = _mock_recipe_analysis(
            title="Receta Analizada (Respaldo)",
            source_type="text",
            source_ref="Texto manual",
            user_input=text
        )
        recipe.dietary_tags = list(set((recipe.dietary_tags or []) + ["Modo Demostración (Servidor de IA ocupado)"]))
        return recipe

def analyze_recipe_from_image(image_bytes: bytes, mime_type: str, file_name: str = "foto_receta.jpg") -> Recipe:
    """Analiza una receta a partir de una foto de plato, libro de cocina o lista de ingredientes."""
    client = get_client()
    if not client:
        return _mock_recipe_analysis(
            title=f"Plato detectado en imagen: {file_name}",
            source_type="image",
            source_ref=file_name,
            user_input="Análisis visual de imagen"
        )

    # Optimizar imagen para agilizar transferencia y evitar errores de sobrecarga
    opt_bytes, opt_mime = optimize_image_bytes(image_bytes)
    image_part = types.Part.from_bytes(data=opt_bytes, mime_type=opt_mime)
    prompt = (
        "Examina detalladamente la imagen adjunta. Reconoce el plato cocinado, los ingredientes visibles, "
        "las porciones probables y proporciona el análisis nutricional completo, lista de ingredientes estimados, "
        "instrucciones culinarias deducidas y consejos de mejora."
    )

    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[image_part, prompt],
            system_instruction=RECIPE_ANALYSIS_SYSTEM_PROMPT,
            response_json_schema=Recipe.model_json_schema(),
            temperature=0.2
        )
        data = json.loads(text_response)
        data["source_type"] = "image"
        data["source_reference"] = file_name
        if not data.get("image_url"):
            data["image_url"] = get_culinary_image_for_title(data.get("title", ""))
        return Recipe(**data)
    except Exception as e:
        logger.error(f"Error analizando imagen con Gemini: {e}")
        recipe = _mock_recipe_analysis(
            title=f"Plato en imagen: {file_name.split('.')[0]}",
            source_type="image",
            source_ref=file_name,
            user_input="Análisis con respaldo nutricional por saturación temporal de API"
        )
        recipe.dietary_tags = list(set((recipe.dietary_tags or []) + ["Modo Demostración (Servidor de IA ocupado)"]))
        return recipe

def analyze_recipe_from_video_file(video_path: str, file_name: str = "video.mp4", extra_context: str = "", real_title: str = "") -> Recipe:
    """Analiza un archivo de vídeo subido usando la File API de Gemini."""
    client = get_client()
    display_title = real_title or file_name
    if not client:
        return _mock_recipe_analysis(
            title=f"{display_title}",
            source_type="video_file",
            source_ref=file_name,
            user_input=f"{display_title}\n{extra_context}"
        )

    uploaded_file = None
    try:
        # Subir el archivo de vídeo a Gemini File API
        uploaded_file = client.files.upload(file=video_path)
        logger.info(f"Subido archivo de vídeo {uploaded_file.name}, esperando procesamiento...")

        # Esperar a que el vídeo esté en estado ACTIVE
        max_retries = 30
        for _ in range(max_retries):
            file_info = client.files.get(name=uploaded_file.name)
            if file_info.state == "ACTIVE":
                break
            elif file_info.state == "FAILED":
                raise RuntimeError("El procesamiento del vídeo falló en los servidores de Gemini.")
            time.sleep(2)

        prompt = (
            f"Analiza detalladamente este vídeo de cocina.\n"
            f"{f'Contexto y publicación del creador: {extra_context}' if extra_context else ''}\n\n"
            "Escucha las explicaciones, observa los ingredientes utilizados, las cantidades mostradas "
            "en la preparación, los pasos culinarios y calcula el análisis nutricional completo con "
            "macronutrientes, calorías, Nutri-Score y sugerencias saludables."
        )

        text_response = generate_content_with_fallback(
            client=client,
            contents=[uploaded_file, prompt],
            system_instruction=RECIPE_ANALYSIS_SYSTEM_PROMPT,
            response_json_schema=Recipe.model_json_schema(),
            temperature=0.2
        )
        data = json.loads(text_response)
        data["source_type"] = "video_file"
        data["source_reference"] = file_name
        if not data.get("image_url"):
            data["image_url"] = get_culinary_image_for_title(data.get("title", ""))
        return Recipe(**data)
    except Exception as e:
        logger.error(f"Error analizando vídeo con Gemini: {e}")
        recipe = _mock_recipe_analysis(
            title=f"{display_title}",
            source_type="video_file",
            source_ref=file_name,
            user_input=f"{display_title}\n{extra_context}"
        )
        recipe.dietary_tags = list(set((recipe.dietary_tags or []) + ["Modo Demostración (Servidor de IA ocupado)"]))
        return recipe
    finally:
        if uploaded_file and client:
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass

def analyze_recipe_from_social_metadata(url: str, metadata: Dict[str, Any], video_path: Optional[str] = None) -> Recipe:
    """Analiza la receta de una red social (TikTok, Instagram Reel, YouTube Shorts)."""
    raw_title = metadata.get("title", "")
    description = metadata.get("description", "")
    source = metadata.get("source", "Social Media")
    clean_title = extract_clean_recipe_title(raw_title, description, source)
    extra_context = f"Título del post: {clean_title}\nTexto de la publicación: {description}"

    # Si tenemos el archivo de vídeo descargado, usamos el análisis visual y auditivo completo
    if video_path and os.path.exists(video_path):
        recipe = analyze_recipe_from_video_file(
            video_path,
            file_name=f"{clean_title} ({source})",
            extra_context=extra_context,
            real_title=clean_title
        )
        recipe.source_type = "social_url"
        recipe.source_reference = url
        recipe.video_url = url
        recipe.image_url = metadata.get("thumbnail")
        return recipe

    # Si sólo tenemos título y descripción/transcripción
    client = get_client()
    if not client:
        recipe = _mock_recipe_analysis(
            title=clean_title,
            source_type="social_url",
            source_ref=url,
            user_input=extra_context
        )
        recipe.image_url = metadata.get("thumbnail")
        recipe.video_url = url
        return recipe

    prompt = (
        f"Analiza la siguiente receta extraída de una publicación de redes sociales ({url}):\n\n"
        f"{extra_context}\n\n"
        "Extrae todos los ingredientes, cantidades, pasos e infiere el valor nutricional completo y calorías."
    )

    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[prompt],
            system_instruction=RECIPE_ANALYSIS_SYSTEM_PROMPT,
            response_json_schema=Recipe.model_json_schema(),
            temperature=0.2
        )
        data = json.loads(text_response)
        data["source_type"] = "social_url"
        data["source_reference"] = url
        data["video_url"] = url
        data["image_url"] = metadata.get("thumbnail") or get_culinary_image_for_title(data.get("title", ""))
        return Recipe(**data)
    except Exception as e:
        logger.error(f"Error analizando metadatos sociales con Gemini: {e}")
        recipe = _mock_recipe_analysis(
            title=clean_title,
            source_type="social_url",
            source_ref=url,
            user_input=extra_context
        )
        recipe.image_url = metadata.get("thumbnail") or get_culinary_image_for_title(recipe.title)
        recipe.video_url = url
        recipe.dietary_tags = list(set((recipe.dietary_tags or []) + ["Modo Demostración (Servidor de IA ocupado)"]))
        return recipe

def suggest_recipes_by_nutrition(request: SuggestionRequest) -> List[Recipe]:
    """Genera sugerencias de recetas adaptadas a objetivos nutricionales precisos."""
    client = get_client()
    if not client:
        return _mock_suggestions(request)

    # Ajuste si los requerimientos de proteína y calorías son físicamente incompatibles (1g prot = 4 kcal)
    prot_cal_note = ""
    if request.min_protein and request.target_calories and (request.min_protein * 4 > request.target_calories):
        prot_cal_note = f"\n(Nota dietética: {request.min_protein}g de proteína aportan al menos {request.min_protein * 4} kcal. Ajusta las recetas para maximizar el aporte proteico posible dentro del límite de {request.target_calories} kcal de forma segura)."

    prompt = f"""Genera {request.count} recetas culinarias originales, deliciosas y detalladas que cumplan con las siguientes metas nutricionales:

- Calorías objetivo por porción: {request.target_calories or 'Equilibradas (400-600 kcal)'} Kcal
- Mínimo de proteína por porción: {request.min_protein or 'No especificado'} g{prot_cal_note}
- Máximo de carbohidratos por porción: {request.max_carbs or 'No especificado'} g
- Máximo de grasas por porción: {request.max_fat or 'No especificado'} g
- Tipo de dieta: {request.diet_type}
- Momento del día: {request.meal_type}
- Ingredientes disponibles en casa: {request.available_ingredients or 'Cualquiera'}
- Ingredientes a evitar o alérgenos: {request.excluded_ingredients or 'Ninguno'}

Cada receta debe estar completamente calculada y lista para cocinar."""

    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[prompt],
            system_instruction="Eres un Nutricionista Chef especializado en prescripción dietética personalizada. Genera sugerencias de recetas exactas en el formato estructurado.",
            response_json_schema=SuggestionResponse.model_json_schema(),
            temperature=0.3
        )
        data = json.loads(text_response)
        suggestions = []
        for item in data.get("suggestions", []):
            item["source_type"] = "ai_generated"
            item["source_reference"] = "Sugerencia por Objetivos"
            if not item.get("category"):
                req_meal = (request.meal_type or "").lower()
                if "desayun" in req_meal:
                    item["category"] = "desayuno"
                elif "cen" in req_meal:
                    item["category"] = "cena"
                elif any(k in req_meal for k in ["snack", "meriend", "postre"]):
                    item["category"] = "merienda-postre"
                else:
                    item["category"] = "comida"
            if not item.get("image_url"):
                item["image_url"] = get_culinary_image_for_title(item.get("title", ""))
            suggestions.append(Recipe(**item))
        return suggestions
    except Exception as e:
        logger.error(f"Error generando sugerencias con Gemini: {e}")
        return _mock_suggestions(request)

def compare_recipes_nutrition(recipes: List[Recipe]) -> ComparisonResult:
    """Compara 2 o más recetas nutricionalmente y genera un análisis profesional."""
    client = get_client()
    
    recipes_summary = []
    for r in recipes:
        recipes_summary.append({
            "id": r.id,
            "title": r.title,
            "servings": r.servings,
            "per_serving": r.per_serving.model_dump(),
            "nutri_score": r.nutri_score,
            "dietary_tags": r.dietary_tags,
            "ingredients_count": len(r.ingredients)
        })

    if not client:
        # Fallback local comparison calculation
        return _local_recipe_comparison(recipes)

    prompt = f"""Compara nutricionalmente y de forma crítica las siguientes recetas:\n\n{json.dumps(recipes_summary, indent=2, ensure_ascii=False)}

Determina con justificación técnica:
1. Cuál es la mejor opción para ganar masa muscular (hipertrofia).
2. Cuál es la mejor opción para pérdida de grasa / déficit calórico.
3. Cuál es la receta más equilibrada y densa en micronutrientes para salud general.
4. Resumen analítico comparativo y puntos clave diferenciales."""

    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[prompt],
            system_instruction="Eres un Nutricionista Deportivo y Clínico comparando dietas y recetas.",
            response_json_schema=ComparisonResult.model_json_schema(),
            temperature=0.2
        )
        data = json.loads(text_response)
        data["recipes"] = recipes
        return ComparisonResult(**data)
    except Exception as e:
        logger.error(f"Error en comparación con Gemini: {e}")
        return _local_recipe_comparison(recipes)

def _local_recipe_comparison(recipes: List[Recipe]) -> ComparisonResult:
    """Comparación heurística cuando la API key no está configurada o hay fallo de red."""
    # Winner for muscle: highest protein
    best_protein = max(recipes, key=lambda r: r.per_serving.protein)
    # Winner for fat loss: lowest calories and highest protein/calorie ratio
    best_fat_loss = min(recipes, key=lambda r: r.per_serving.calories)
    # Winner for general health: Nutri-Score A/B and higher fiber
    best_health = max(recipes, key=lambda r: (r.per_serving.fiber * 2 + (50 if r.nutri_score in ['A', 'B'] else 0)))

    key_diffs = []
    for r in recipes:
        key_diffs.append(
            f"'{r.title}': {r.per_serving.calories:.0f} kcal, {r.per_serving.protein:.1f}g proteína, "
            f"{r.per_serving.carbohydrates:.1f}g carbohidratos, {r.per_serving.fats:.1f}g grasas (Nutri-Score: {r.nutri_score})."
        )

    return ComparisonResult(
        recipes=recipes,
        comparison_summary=(
            f"Se compararon {len(recipes)} recetas. La diferencia calórica entre la más ligera ('{best_fat_loss.title}') "
            f"y la más energética es de {max(r.per_serving.calories for r in recipes) - min(r.per_serving.calories for r in recipes):.0f} kcal por ración."
        ),
        winner_for_muscle_gain=f"'{best_protein.title}' es la mejor opción para masa muscular aportando {best_protein.per_serving.protein:.1f}g de proteína por ración.",
        winner_for_fat_loss=f"'{best_fat_loss.title}' es la más adecuada para déficit calórico con solo {best_fat_loss.per_serving.calories:.0f} kcal por ración.",
        winner_for_general_health=f"'{best_health.title}' destaca por su densidad nutricional, aporte de fibra ({best_health.per_serving.fiber:.1f}g) y perfil equilibrado.",
        key_differences=key_diffs
    )

def _mock_recipe_analysis(title: str, source_type: str, source_ref: str, user_input: str) -> Recipe:
    """Mock amigable cuando aún no se ha configurado la GEMINI_API_KEY."""
    input_lower = f"{title} {user_input}".lower()
    
    # Adaptar mock según si parece postre/dulce o salado
    if any(k in input_lower for k in ["cake", "plum", "bizcocho", "tarta", "pastel", "dulce", "limón", "chocolate", "galleta"]):
        ingredients = [
            Ingredient(name="Harina de trigo de repostería", amount="200g", calories=720, protein=20, carbs=152, fat=2, notes="Base del bizcocho"),
            Ingredient(name="Azúcar o endulzante", amount="120g", calories=480, protein=0, carbs=120, fat=0, notes="Endulzante"),
            Ingredient(name="Mantequilla sin sal (o aceite)", amount="100g", calories=717, protein=0.8, carbs=0, fat=81, notes="Grasa para esponjosidad"),
            Ingredient(name="Huevos medianos", amount="3 unidades", calories=210, protein=18, carbs=1, fat=15, notes="Estructura"),
            Ingredient(name="Ralladura y zumo de limón fresco", amount="1 unidad", calories=20, protein=0.5, carbs=5, fat=0.2, notes="Aroma y acidez natural"),
            Ingredient(name="Levadura química en polvo", amount="1 sobre (16g)", calories=15, protein=0, carbs=3, fat=0, notes="Gasificante")
        ]
        instructions = [
            "Batir la mantequilla con el azúcar hasta blanquear.",
            "Incorporar los huevos uno a uno y añadir la ralladura y zumo de limón.",
            "Tamizar la harina con la levadura e integrar con movimientos envolventes.",
            "Hornear a 180°C durante 35-40 minutos hasta dorar."
        ]
        servings = 8
        per_serving = NutrientInfo(
            calories=270.0,
            protein=4.9,
            carbohydrates=35.1,
            fats=12.3,
            fiber=0.8,
            sugar=16.0,
            sodium=140.0,
            saturated_fat=6.8,
            vitamins_and_minerals=["Vitamina C: 8mg", "Calcio: 35mg"]
        )
        total = NutrientInfo(
            calories=2162.0,
            protein=39.3,
            carbohydrates=281.0,
            fats=98.2,
            fiber=6.4,
            sugar=128.0,
            sodium=1120.0,
            saturated_fat=54.4,
            vitamins_and_minerals=["Vitamina C: 64mg", "Calcio: 280mg"]
        )
        nutri_score = "D"
        dietary_tags = ["⚠️ Modo Demostración", "Repostería Casera", "Requiere Clave Gemini"]
    else:
        ingredients = [
            Ingredient(name="Ingrediente principal (ej: Pollo / Legumbres)", amount="250g", calories=300, protein=55, carbs=2, fat=7, notes="Fuente proteica"),
            Ingredient(name="Vegetales variados (tomate, pimiento, cebolla)", amount="200g", calories=60, protein=3, carbs=12, fat=0.5, notes="Aporte de fibra y vitaminas"),
            Ingredient(name="Base de grano o tubérculo (patata / arroz)", amount="150g", calories=180, protein=4, carbs=38, fat=1, notes="Carbohidratos energéticos"),
            Ingredient(name="Aceite de oliva virgen extra", amount="1 cucharada (10ml)", calories=90, protein=0, carbs=0, fat=10, notes="Grasas cardiosaludables")
        ]
        instructions = [
            "Lavar y trocear todos los ingredientes uniformemente.",
            "Saltear en una sartén con el aceite de oliva a fuego medio durante 10 minutos.",
            "Cocinar a fuego lento hasta que los ingredientes estén en su punto.",
            "Servir caliente y disfrutar."
        ]
        servings = 2
        per_serving = NutrientInfo(
            calories=315.0,
            protein=31.0,
            carbohydrates=26.0,
            fats=9.2,
            fiber=4.5,
            sugar=3.8,
            sodium=340.0,
            vitamins_and_minerals=["Vitamina C: 45mg", "Hierro: 2.3mg"]
        )
        total = NutrientInfo(
            calories=630.0,
            protein=62.0,
            carbohydrates=52.0,
            fats=18.4,
            fiber=9.0,
            sugar=7.6,
            sodium=680.0,
            vitamins_and_minerals=["Vitamina C: 90mg", "Hierro: 4.6mg"]
        )
        nutri_score = "A"
        dietary_tags = ["⚠️ Modo Demostración", "Requiere Clave Gemini"]

    return Recipe(
        id=None,
        title=f"{title} (Modo Demo)",
        description=f"Receta estimada a partir de la publicación. ⚠️ Para análisis audiovisual real mediante visión por computadora, activa tu clave de Gemini en Ajustes.",
        servings=servings,
        prep_time_minutes=15,
        cook_time_minutes=35,
        source_type=source_type,
        source_reference=source_ref,
        image_url=get_culinary_image_for_title(title),
        ingredients=ingredients,
        instructions=instructions,
        per_serving=per_serving,
        total=total,
        nutri_score=nutri_score,
        dietary_tags=dietary_tags,
        health_verdict="⚠️ AVISO DE MODO DEMOSTRACIÓN: No has configurado tu clave GEMINI_API_KEY. Este resultado es una plantilla estimada. Para que la IA procese el archivo de vídeo real y extraiga los ingredientes visuales con precisión, añade tu clave gratuita en 'Gemini / Ajustes' (arriba a la derecha).",
        healthier_alternatives=[
            "Para un análisis real con visión artificial, pulsa en 'Gemini / Ajustes' e introduce tu clave de Google AI Studio.",
            "Versión más ligera: sustituir parte del azúcar por eritritol o compota de manzana."
        ]
    )

def _mock_suggestions(request: SuggestionRequest) -> List[Recipe]:
    """Sugerencias simuladas si no hay API key disponible."""
    target_cal = request.target_calories or 500
    min_prot = request.min_protein or 35
    return [
        Recipe(
            id=None,
            title="Wok Rápido de Ternera Magra y Brócoli",
            description=f"Plato alto en hierro y proteína formulado para {target_cal:.0f} Kcal y {min_prot:.0f}g de proteína.",
            servings=1,
            prep_time_minutes=10,
            cook_time_minutes=10,
            source_type="ai_generated",
            source_reference="Sugerencia por Objetivos",
            image_url=get_culinary_image_for_title("Wok Rápido de Ternera Magra y Brócoli"),
            ingredients=[
                Ingredient(name="Filete de ternera magra cortado en tiras", amount="180g", calories=250, protein=42, carbs=0, fat=9),
                Ingredient(name="Brócoli al vapor", amount="150g", calories=50, protein=4.2, carbs=10, fat=0.6),
                Ingredient(name="Fideos de arroz o konjac", amount="80g", calories=120, protein=2, carbs=28, fat=0.2),
                Ingredient(name="Aceite de sésamo y salsa de soja baja en sal", amount="1 cucharadita", calories=45, protein=1, carbs=1.5, fat=4)
            ],
            instructions=[
                "Hervir o hacer al vapor los ramilletes de brócoli durante 3 minutos.",
                "En un wok o sartén bien caliente, saltear las tiras de ternera 2 minutos a fuego vivo.",
                "Añadir el brócoli y los fideos con la salsa, saltear 1 minuto más y servir."
            ],
            per_serving=NutrientInfo(
                calories=465.0,
                protein=49.2,
                carbohydrates=39.5,
                fats=13.8,
                fiber=5.2,
                sugar=2.1,
                sodium=410.0,
                vitamins_and_minerals=["Hierro: 4.8mg", "Vitamina C: 95mg", "Zinc: 6.2mg"]
            ),
            total=NutrientInfo(
                calories=465.0,
                protein=49.2,
                carbohydrates=39.5,
                fats=13.8,
                fiber=5.2,
                sugar=2.1,
                sodium=410.0,
                vitamins_and_minerals=["Hierro: 4.8mg", "Vitamina C: 95mg", "Zinc: 6.2mg"]
            ),
            nutri_score="A",
            dietary_tags=["Alta en proteína", "Rica en hierro", "Baja en azúcares"],
            health_verdict="Perfecta para cumplir tus objetivos proteicos con pocas calorías y gran aporte de antioxidantes y zinc.",
            healthier_alternatives=["Usar fideos shirataki / konjac para recortar aún más los carbohidratos si estás en definición estricta."]
        ),
        Recipe(
            id=None,
            title="Tortilla Fitness de Claras, Pavo y Champiñones con Pan Integral",
            description=f"Desayuno o cena ultra ligero y saciante de rápida preparación.",
            servings=1,
            prep_time_minutes=5,
            cook_time_minutes=8,
            source_type="ai_generated",
            source_reference="Sugerencia por Objetivos",
            image_url=get_culinary_image_for_title("Tortilla Fitness de Claras, Pavo y Champiñones con Pan Integral"),
            ingredients=[
                Ingredient(name="Claras de huevo pasteurizadas", amount="200ml", calories=104, protein=22, carbs=1.4, fat=0.4),
                Ingredient(name="1 huevo entero campero", amount="1 unidad", calories=75, protein=6.5, carbs=0.5, fat=5.2),
                Ingredient(name="Pechuga de pavo 95% carne", amount="60g", calories=60, protein=12, carbs=0.8, fat=1.0),
                Ingredient(name="Champiñones laminados", amount="100g", calories=22, protein=3.1, carbs=3.3, fat=0.3),
                Ingredient(name="Pan 100% integral de centeno", amount="1 rebanada (40g)", calories=95, protein=3.5, carbs=18, fat=1.1)
            ],
            instructions=[
                "Dorar los champiñones en sartén con una gota de aceite.",
                "Batir las claras con el huevo entero y salpimentar.",
                "Añadir el pavo troceado y las claras sobre los champiñones, cocinar a fuego medio hasta cuajar.",
                "Servir acompañada de la rebanada de pan integral tostada."
            ],
            per_serving=NutrientInfo(
                calories=356.0,
                protein=47.1,
                carbohydrates=24.0,
                fats=8.0,
                fiber=4.0,
                sugar=2.0,
                sodium=480.0,
                vitamins_and_minerals=["Colina: 150mg", "Vitamina B12: 1.8mcg", "Selenio: 32mcg"]
            ),
            total=NutrientInfo(
                calories=356.0,
                protein=47.1,
                carbohydrates=24.0,
                fats=8.0,
                fiber=4.0,
                sugar=2.0,
                sodium=480.0,
                vitamins_and_minerals=["Colina: 150mg", "Vitamina B12: 1.8mcg", "Selenio: 32mcg"]
            ),
            nutri_score="A",
            dietary_tags=["Alta en proteína", "Baja en grasa", "Muy saciante"],
            health_verdict="Máximo ratio de proteína por caloría. Muy baja densidad energética que previene el hambre en dietas de control de peso.",
            healthier_alternatives=["Añadir tomate fresco rallado al pan integral para sumar licopeno y vitamina C."]
        )
    ]

def estimate_food_nutrition(name: str, brand: Optional[str] = None) -> CustomFood:
    """Calcula automáticamente los nutrientes por 100g de un alimento usando IA."""
    client = get_client()
    brand_text = f" (marca o supermercado: {brand})" if brand else ""
    default_food = CustomFood(
        name=name,
        brand=brand or "",
        serving_size_g=100.0,
        calories=100.0,
        protein=5.0,
        carbohydrates=10.0,
        fats=2.0,
        fiber=1.0,
        category="despensa",
        notes="Estimación general"
    )
    if not client:
        return default_food

    prompt = f"""Indica el perfil nutricional medio por 100 gramos para el alimento: '{name}'{brand_text}.
Calcula calorías (Kcal), proteínas (g), carbohidratos (g), grasas totales (g), fibra (g) y clasifica la categoría en exactamente una de estas opciones: 'proteina', 'carbohidrato', 'verdura', 'lacteo', 'grasa', 'despensa'."""

    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[prompt],
            system_instruction="Eres una base de datos bromatológica oficial (BEDCA / USDA / OpenFoodFacts). Devuelve los datos nutricionales estándar por 100 gramos del alimento consultado en JSON.",
            response_json_schema=CustomFood.model_json_schema(),
            temperature=0.1
        )
        data = json.loads(text_response)
        data["name"] = name
        if brand:
            data["brand"] = brand
        data["serving_size_g"] = 100.0
        return CustomFood(**data)
    except Exception as e:
        logger.error(f"Error estimando nutrientes de alimento con Gemini: {e}")
        return default_food

def suggest_recipe_from_pantry(request: PantryRecipeRequest, pantry_foods: Optional[List[Dict[str, Any]]] = None) -> List[Recipe]:
    """Genera 2 recetas completas aprovechando los ingredientes disponibles en casa."""
    client = get_client()
    
    pantry_context = ""
    if pantry_foods and len(pantry_foods) > 0:
        food_names = [f["name"] for f in pantry_foods[:15]]
        pantry_context = f"\nAlimentos habituales registrados en la despensa del usuario: {', '.join(food_names)}."

    prompt = f"""Actúa como un Chef y Nutricionista de cocina de aprovechamiento.
El usuario quiere cocinar con lo que tiene en casa y evitar desperdicios.

Ingredientes disponibles en su casa o nevera:
"{request.ingredients}"{pantry_context}

Parámetros de la receta:
- Momento del día / categoría: {request.meal_type}
- Tiempo de cocinado: {request.cooking_time}
- Raciones: {request.servings} comensales
- Estilo o preferencia: {request.dietary_preference}

Diseña 2 recetas culinarias completas, sabrosas y equilibradas que hagan uso principal de los ingredientes indicados (asume que dispone de sal, agua, pimienta o una pizca de aceite).
Cada receta debe incluir su lista de ingredientes calculada para {request.servings} raciones, preparación paso a paso, análisis bromatológico completo (calorías y macronutrientes por ración), Nutri-Score y categoría ('desayuno', 'comida', 'merienda-postre' o 'cena')."""

    if not client:
        return _mock_pantry_recipes(request)

    try:
        text_response = generate_content_with_fallback(
            client=client,
            contents=[prompt],
            system_instruction="Eres un Chef Nutricionista profesional creando recetas a medida con ingredientes disponibles.",
            response_json_schema=SuggestionResponse.model_json_schema(),
            temperature=0.3
        )
        data = json.loads(text_response)
        suggestions = []
        for item in data.get("suggestions", []):
            item["source_type"] = "ai_generated"
            item["source_reference"] = "Nevera / Despensa IA"
            if not item.get("category"):
                req_meal = (request.meal_type or "").lower()
                if "desayun" in req_meal:
                    item["category"] = "desayuno"
                elif "cen" in req_meal:
                    item["category"] = "cena"
                elif any(k in req_meal for k in ["snack", "meriend", "postre"]):
                    item["category"] = "merienda-postre"
                else:
                    item["category"] = "comida"
            if not item.get("image_url"):
                item["image_url"] = get_culinary_image_for_title(item.get("title", ""))
            suggestions.append(Recipe(**item))
        return suggestions
    except Exception as e:
        logger.error(f"Error generando recetas de despensa con Gemini: {e}")
        return _mock_pantry_recipes(request)

def _mock_pantry_recipes(request: PantryRecipeRequest) -> List[Recipe]:
    """Recetas de aprovechamiento de respaldo si no hay conexión de API."""
    ingredients_str = request.ingredients or "Ingredientes de casa"
    return [
        Recipe(
            id=None,
            title="Salteado Rápido de Aprovechamiento Saludable",
            description=f"Receta diseñada para aprovechar: {ingredients_str[:50]}.",
            servings=request.servings or 2,
            prep_time_minutes=10,
            cook_time_minutes=15,
            source_type="ai_generated",
            source_reference="Nevera / Despensa IA",
            category="comida" if "comida" in (request.meal_type or "") else "cena",
            image_url=get_culinary_image_for_title("Salteado Rápido de Verduras"),
            ingredients=[
                Ingredient(name="Ingredientes principales combinados", amount="350g", calories=320, protein=25, carbs=20, fat=12),
                Ingredient(name="Aceite de oliva virgen extra y especias", amount="1 cucharada", calories=90, protein=0, carbs=0, fat=10)
            ],
            instructions=[
                "Picar los ingredientes disponibles en dados o tiras homogéneas.",
                "Saltear a fuego medio-alto con una cucharada de aceite hasta que estén tiernos y dorados.",
                "Ajustar de sal, pimienta y servir caliente."
            ],
            per_serving=NutrientInfo(calories=410.0, protein=25.0, carbohydrates=20.0, fats=22.0, fiber=5.0, sodium=350.0),
            total=NutrientInfo(calories=820.0, protein=50.0, carbohydrates=40.0, fats=44.0, fiber=10.0, sodium=700.0),
            nutri_score="A",
            dietary_tags=["Aprovechamiento", "Fácil", "Saludable"],
            health_verdict="Excelente combinación para no desperdiciar comida y mantener un perfil calórico equilibrado."
        )
    ]

