from pydantic import BaseModel, Field
from typing import List, Optional

class NutrientInfo(BaseModel):
    calories: float = Field(0.0, description="Calorías en Kcal")
    protein: float = Field(0.0, description="Proteínas en gramos (g)")
    carbohydrates: float = Field(0.0, description="Carbohidratos totales en gramos (g)")
    fats: float = Field(0.0, description="Grasas totales en gramos (g)")
    fiber: float = Field(0.0, description="Fibra dietética en gramos (g)")
    sugar: float = Field(0.0, description="Azúcares simples en gramos (g)")
    sodium: float = Field(0.0, description="Sodio en miligramos (mg)")
    saturated_fat: Optional[float] = Field(0.0, description="Grasas saturadas en gramos (g)")
    cholesterol: Optional[float] = Field(0.0, description="Colesterol en miligramos (mg)")
    potassium: Optional[float] = Field(0.0, description="Potasio en miligramos (mg)")
    vitamins_and_minerals: List[str] = Field(default_factory=list, description="Lista de vitaminas y minerales destacados")

class Ingredient(BaseModel):
    name: str = Field(..., description="Nombre del ingrediente")
    amount: str = Field(..., description="Cantidad con unidad de medida (ej: 200g, 1 taza)")
    calories: Optional[float] = Field(None, description="Calorías estimadas")
    protein: Optional[float] = Field(None, description="Proteína estimada en g")
    carbs: Optional[float] = Field(None, description="Carbohidratos estimados en g")
    fat: Optional[float] = Field(None, description="Grasas estimadas en g")
    notes: Optional[str] = Field(None, description="Notas nutricionales o sustituciones")

class Recipe(BaseModel):
    id: Optional[str] = Field(None, description="Identificador único")
    title: str = Field(..., description="Nombre de la receta")
    description: str = Field("", description="Breve descripción apetitosa de la receta")
    servings: int = Field(1, description="Número de porciones o raciones")
    prep_time_minutes: Optional[int] = Field(None, description="Tiempo de preparación en minutos")
    cook_time_minutes: Optional[int] = Field(None, description="Tiempo de cocción en minutos")
    source_type: str = Field("text", description="text, image, video_file, social_url, ai_generated")
    source_reference: Optional[str] = Field(None, description="URL de origen o nombre de archivo")
    video_url: Optional[str] = Field(None, description="URL directa del vídeo si proviene de redes sociales (Instagram, TikTok, YouTube)")
    category: str = Field("comida", description="Momento del día / categoría: desayuno, comida, merienda, cena, postre")
    image_url: Optional[str] = Field(None, description="URL o ruta de imagen si está disponible")
    ingredients: List[Ingredient] = Field(default_factory=list, description="Ingredientes de la receta")
    instructions: List[str] = Field(default_factory=list, description="Pasos de preparación detallados")
    per_serving: NutrientInfo = Field(default_factory=NutrientInfo, description="Información nutricional por ración")
    total: NutrientInfo = Field(default_factory=NutrientInfo, description="Información nutricional total de la receta")
    nutri_score: str = Field("A", description="Nutri-Score estimado: A, B, C, D o E")
    dietary_tags: List[str] = Field(default_factory=list, description="Etiquetas dietéticas (ej: Alta en proteína, Keto, Vegano, Baja en sodio)")
    health_verdict: str = Field("", description="Dictamen nutricional completo: puntos fuertes y áreas de mejora")
    healthier_alternatives: List[str] = Field(default_factory=list, description="Consejos de sustitución para hacer la receta aún más saludable")
    created_at: Optional[str] = Field(None, description="Fecha de creación ISO")

class RecipeTextRequest(BaseModel):
    text: str = Field(..., description="Texto de la receta o lista de ingredientes y pasos")

class RecipeUrlRequest(BaseModel):
    url: str = Field(..., description="Enlace a vídeo de TikTok, Instagram Reel o YouTube")

class ComparisonRequest(BaseModel):
    recipe_ids: List[str] = Field(..., min_length=2, description="Lista de IDs de recetas para comparar")

class ComparisonResult(BaseModel):
    recipes: List[Recipe] = Field(..., description="Lista de recetas comparadas")
    comparison_summary: str = Field(..., description="Resumen comparativo general")
    winner_for_muscle_gain: str = Field(..., description="Receta ganadora para ganar masa muscular y por qué")
    winner_for_fat_loss: str = Field(..., description="Receta ganadora para pérdida de grasa y por qué")
    winner_for_general_health: str = Field(..., description="Receta más equilibrada para salud general")
    key_differences: List[str] = Field(default_factory=list, description="Puntos clave de diferencia")

class SuggestionRequest(BaseModel):
    target_calories: Optional[float] = Field(None, description="Calorías objetivo por porción")
    min_protein: Optional[float] = Field(None, description="Mínimo de proteína en gramos")
    max_carbs: Optional[float] = Field(None, description="Máximo de carbohidratos en gramos")
    max_fat: Optional[float] = Field(None, description="Máximo de grasas en gramos")
    diet_type: Optional[str] = Field("Cualquiera", description="Tipo de dieta: Cualquiera, Mediterránea, Vegetariana, Vegana, Keto, Baja en sodio, Sin gluten")
    meal_type: Optional[str] = Field("Cualquiera", description="Tipo de comida: Desayuno, Almuerzo, Cena, Snack")
    available_ingredients: Optional[str] = Field("", description="Ingredientes que tienes disponibles en casa")
    excluded_ingredients: Optional[str] = Field("", description="Ingredientes no deseados o alérgenos")
    count: int = Field(3, description="Número de recetas a sugerir (por defecto 3)")

class SuggestionResponse(BaseModel):
    suggestions: List[Recipe] = Field(default_factory=list, description="Recetas sugeridas que cumplen con los requisitos")

class CustomFood(BaseModel):
    id: Optional[str] = Field(None, description="Identificador único")
    name: str = Field(..., description="Nombre del alimento o producto (ej: Avena Mercadona, Pechuga de pollo)")
    brand: Optional[str] = Field(None, description="Marca o supermercado (opcional)")
    serving_size_g: float = Field(100.0, description="Tamaño de ración base en gramos o ml (por defecto 100g)")
    calories: float = Field(0.0, description="Calorías (Kcal por ración base)")
    protein: float = Field(0.0, description="Proteínas en gramos (g)")
    carbohydrates: float = Field(0.0, description="Carbohidratos en gramos (g)")
    fats: float = Field(0.0, description="Grasas totales en gramos (g)")
    fiber: Optional[float] = Field(0.0, description="Fibra en gramos (g)")
    category: Optional[str] = Field("proteina", description="proteina, carbohidrato, verdura, lacteo, grasa, despensa")
    notes: Optional[str] = Field(None, description="Notas o comentarios opcionales")
    created_at: Optional[str] = Field(None, description="Fecha de creación ISO")

class FoodEstimateRequest(BaseModel):
    name: str = Field(..., description="Nombre del alimento")
    brand: Optional[str] = Field(None, description="Marca o supermercado opcional")

class PantryRecipeRequest(BaseModel):
    ingredients: str = Field(..., description="Ingredientes que tienes disponibles en casa")
    meal_type: Optional[str] = Field("comida", description="desayuno, comida, merienda, cena, postre, cualquiera")
    cooking_time: Optional[str] = Field("rapida", description="express (15m), media (30m), elaborada")
    servings: Optional[int] = Field(2, description="Número de raciones")
    dietary_preference: Optional[str] = Field("saludable", description="saludable, alta en proteina, baja en calorias, vegetariana")
    selected_pantry_foods: Optional[List[str]] = Field(default_factory=list, description="Nombres de alimentos seleccionados de la despensa")

