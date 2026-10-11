import json
import uuid
from datetime import datetime
from app.database import save_recipe, list_recipes

# Colección de recetas extraídas de los libros subidos por el usuario:
# 1. "Cocina sana para los peques... y toda la familia" (Gobierno de La Rioja)
# 2. "Comida rápida, barata y saludable" (Boticaria García & Ministerio de Consumo)
# 3. "Recetas de cocina saludable" (Pier Luigi Rossi & Aboca)

BOOK_RECIPES = [
    # --- LIBRO: "Comida rápida, barata y saludable" ---
    {
        "id": "book-boticaria-poke-harvard",
        "title": "Poke de Pollo al Estilo Harvard",
        "description": "Plato completo y equilibrado que sigue la regla del Plato de Harvard: 50% vegetales, 25% proteína saludable y 25% carbohidratos complejos.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pechuga de pollo salteada en dados", "amount": "300g", "calories": 360, "protein": 66, "carbs": 0, "fat": 7.5},
            {"name": "Arroz integral precocido", "amount": "125g (1 vasito)", "calories": 160, "protein": 3.5, "carbs": 33, "fat": 1.2},
            {"name": "Melocotón en láminas", "amount": "150g", "calories": 60, "protein": 1.4, "carbs": 14, "fat": 0.4},
            {"name": "Melón en láminas", "amount": "100g", "calories": 34, "protein": 0.8, "carbs": 8, "fat": 0.2},
            {"name": "Canónigos frescos", "amount": "80g", "calories": 16, "protein": 1.6, "carbs": 2.5, "fat": 0.3},
            {"name": "Tomates cherry", "amount": "100g", "calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
            {"name": "Pepino laminado", "amount": "100g", "calories": 15, "protein": 0.7, "carbs": 3.6, "fat": 0.1},
            {"name": "Anacardos tostados", "amount": "8g (10 unidades)", "calories": 45, "protein": 1.5, "carbs": 2.4, "fat": 3.6},
            {"name": "Aceite de oliva virgen extra y zumo de limón", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Cortar la pechuga de pollo en trozos de un bocado y saltear en una sartén antiadherente con AOVE y sal.",
            "Calentar el vasito de arroz integral en el microondas durante 1 minuto y dejar enfriar.",
            "Pelar y laminar el melocotón y el melón en láminas finas. Cortar el tomate cherry y el pepino.",
            "Montar el bowl colocando en la base los canónigos y el arroz integral, añadir el pollo salteado y las frutas.",
            "Añadir los anacardos y aliñar con el AOVE y unas gotas de zumo de limón."
        ],
        "per_serving": {
            "calories": 450.8,
            "protein": 40.3,
            "carbohydrates": 38.8,
            "fats": 15.0,
            "fiber": 5.8,
            "sugar": 14.4,
            "sodium": 220.0,
            "vitamins_and_minerals": ["Vitamina C: 45mg", "Vitamina A: 180mcg", "Magnesio: 65mg"]
        },
        "total": {
            "calories": 901.5,
            "protein": 80.5,
            "carbohydrates": 77.5,
            "fats": 29.9,
            "fiber": 11.6,
            "sugar": 28.8,
            "sodium": 440.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína", "Plato de Harvard", "Rico en antioxidantes"],
        "health_verdict": "Excelente equilibrio macro y micronutricional. Proporciona más de 40g de proteína magra con una fuente completa de fibra y carbohidratos complejos.",
        "healthier_alternatives": ["Sustituir los anacardos por semillas de cáñamo o chía para aportar Omega-3 vegetal."]
    },
    {
        "id": "book-boticaria-lubina-patatas",
        "title": "Lubina con Patatas y Cama de Verduras al Microondas",
        "description": "Una receta ultrarrápida (menos de 15 minutos) con pescado fresco, patatas y pimientos cocinados al microondas conservando todos sus nutrientes.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Lomos de lubina sin piel ni espinas", "amount": "400g (2 lomos)", "calories": 390, "protein": 76, "carbs": 0, "fat": 8},
            {"name": "Patatas medianas", "amount": "200g (2 patatas)", "calories": 154, "protein": 4, "carbs": 34, "fat": 0.2},
            {"name": "Pimientos de colores en tiras", "amount": "150g", "calories": 39, "protein": 1.5, "carbs": 8, "fat": 0.3},
            {"name": "Cebolla en aros", "amount": "50g (media)", "calories": 20, "protein": 0.6, "carbs": 4.5, "fat": 0.1},
            {"name": "Tomate maduro en rodajas", "amount": "80g (1 tomate)", "calories": 14, "protein": 0.7, "carbs": 3, "fat": 0.2},
            {"name": "Aceite de oliva virgen extra", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Pinchas las patatas con un tenedor y cocerlas al microondas con tapa durante 6 minutos a máxima potencia. Cortar en rodajas.",
            "Cortar la cebolla y los pimientos en tiras, colocar en un estuche de vapor o bol con 2 cucharadas de agua, sal y un hilo de AOVE. Cocinar 5 min.",
            "Añadir el tomate y disponer los lomos de lubina encima de la cama de verduras con una pizca de sal.",
            "Cocinar tapado al microondas durante 5 minutos a media potencia.",
            "Servir la lubina jugosa sobre las patatas y verduras calientes."
        ],
        "per_serving": {
            "calories": 388.9,
            "protein": 45.9,
            "carbohydrates": 20.0,
            "fats": 13.9,
            "fiber": 3.8,
            "sugar": 6.4,
            "sodium": 280.0,
            "vitamins_and_minerals": ["Vitamina C: 95mg", "Fósforo: 340mg", "Potasio: 750mg"]
        },
        "total": {
            "calories": 777.7,
            "protein": 91.9,
            "carbohydrates": 40.0,
            "fats": 27.8,
            "fiber": 7.6,
            "sugar": 12.8,
            "sodium": 560.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína", "Pescado blanco", "Sin gluten", "Baja en calorías"],
        "health_verdict": "Plato limpio, ligero y nutritivo. Aporta casi 46g de proteína de máxima biodisponibilidad con menos de 400 kcal por ración.",
        "healthier_alternatives": ["Añadir una cucharadita de pimentón de la Vera sobre las patatas para un toque aromático."]
    },
    {
        "id": "book-boticaria-rainbow-wrap",
        "title": "Rainbow Wrap con Salsa de Anchoas y Huevo",
        "description": "Wrap vegetal crujiente y colorido con tortilla integral, espinacas, huevo cocido y una deliciosa salsa casera de anchoas.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Tortillas de trigo integral", "amount": "75g (2 unidades)", "calories": 210, "protein": 6, "carbs": 38, "fat": 3.5},
            {"name": "Queso fresco en lonchas", "amount": "60g", "calories": 66, "protein": 7.2, "carbs": 1.8, "fat": 3.6},
            {"name": "Huevos camperos medianos", "amount": "120g (2 unidades)", "calories": 150, "protein": 13, "carbs": 1, "fat": 10},
            {"name": "Hojas de espinacas tiernas", "amount": "150g", "calories": 34, "protein": 4.2, "carbs": 5.4, "fat": 0.6},
            {"name": "Pimiento rojo y zanahoria rallada", "amount": "160g", "calories": 50, "protein": 1.6, "carbs": 10, "fat": 0.3},
            {"name": "Filetes de anchoa en conserva", "amount": "4 unidades (20g)", "calories": 42, "protein": 5, "carbs": 0, "fat": 2.4},
            {"name": "Aceite de oliva virgen extra y limón", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Cocer los huevos durante 6 minutos, enfriar en agua fría y pelar.",
            "Para la salsa: batir los huevos cocidos con el ajo, las anchoas escurridas, el aceite y el zumo de limón hasta obtener una crema.",
            "Calentar las tortillas integrales unos segundos en sartén.",
            "Untar con la salsa de anchoas, disponer las hojas de espinacas, el pimiento en tiras, la zanahoria y el queso fresco.",
            "Enrollar firmemente, cortar en diagonal y disfrutar."
        ],
        "per_serving": {
            "calories": 274.2,
            "protein": 15.5,
            "carbohydrates": 13.8,
            "fats": 17.4,
            "fiber": 4.0,
            "sugar": 8.7,
            "sodium": 420.0,
            "vitamins_and_minerals": ["Vitamina A: 480mcg", "Hierro: 3.2mg", "Calcio: 140mg"]
        },
        "total": {
            "calories": 548.4,
            "protein": 31.0,
            "carbohydrates": 27.6,
            "fats": 34.8,
            "fiber": 8.0,
            "sugar": 17.4,
            "sodium": 840.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Comida para llevar", "Rico en fibra", "Vegetariano con pescado"],
        "health_verdict": "Un almuerzo rápido perfecto para llevar al trabajo o comer fuera. Excelente textura crujiente y aporte vitamínico.",
        "healthier_alternatives": ["Sustituir la salsa de anchoas por hummus de garbanzos tradicional."]
    },
    {
        "id": "book-boticaria-hummus-remolacha",
        "title": "Hummus de Remolacha con Crudités de Apio y Pimiento",
        "description": "Snack antioxidante y saciante en menos de 5 minutos combinando garbanzos, remolacha cocida y bastoncitos frescos.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Garbanzos cocidos de bote (enjuagados)", "amount": "200g", "calories": 240, "protein": 14, "carbs": 38, "fat": 4},
            {"name": "Remolacha cocida y pelada", "amount": "250g", "calories": 107, "protein": 4, "carbs": 24, "fat": 0.5},
            {"name": "Tahini (pasta de sésamo)", "amount": "1 cucharada (15g)", "calories": 90, "protein": 3, "carbs": 3, "fat": 8},
            {"name": "Yogur natural sin azúcar", "amount": "1 cucharada (25g)", "calories": 15, "protein": 1, "carbs": 1.2, "fat": 0.8},
            {"name": "Aceite de oliva virgen extra", "amount": "40ml", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Bastoncitos de apio y pimiento rojo", "amount": "80g", "calories": 20, "protein": 0.8, "carbs": 4, "fat": 0.2},
            {"name": "Diente de ajo, zumo de limón y comino", "amount": "1 pizca", "calories": 10, "protein": 0.4, "carbs": 2, "fat": 0.1}
        ],
        "instructions": [
            "Escurrir y enjuagar bien los garbanzos cocidos.",
            "En el vaso de la batidora poner los garbanzos, la remolacha troceada, el tahini, el yogur, el ajo, el zumo de limón y el comino.",
            "Triturar añadiendo el AOVE hasta conseguir una crema suave y sedosa de color rosa vibrante.",
            "Servir en cuenco espolvoreado con pimentón y acompañado de bastones de pimiento y apio para dipear."
        ],
        "per_serving": {
            "calories": 461.9,
            "protein": 14.8,
            "carbohydrates": 33.4,
            "fats": 29.9,
            "fiber": 9.5,
            "sugar": 10.7,
            "sodium": 240.0,
            "vitamins_and_minerals": ["Folatos (B9): 120mcg", "Vitamina C: 35mg", "Magnesio: 70mg"]
        },
        "total": {
            "calories": 923.8,
            "protein": 29.6,
            "carbohydrates": 66.8,
            "fats": 59.8,
            "fiber": 19.0,
            "sugar": 21.4,
            "sodium": 480.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Rico en fibra", "Cardiosaludable", "Sin gluten"],
        "health_verdict": "Gran densidad de fibra soluble e insoluble con grasas monoinsaturadas cardiosaludables. Favorece la saciedad prolongada.",
        "healthier_alternatives": ["Reducir el AOVE a 20ml para una versión hipocalórica con solo 370 kcal por ración."]
    },

    # --- LIBRO: "Cocina sana para los peques... y toda la familia" (Gobierno de La Rioja) ---
    {
        "id": "book-rioja-alubias-calamares",
        "title": "Alubias Blancas con Calamares",
        "description": "Guiso marinero tradicional riojano que combina la suavidad de las alubias blancas con la proteína magra de los calamares y sofrito de verduras.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (Consejería de Salud)",
        "image_url": "https://images.unsplash.com/photo-1547496502-affa22d38842?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Alubias blancas cocidas", "amount": "400g (1 bote)", "calories": 360, "protein": 24, "carbs": 60, "fat": 2},
            {"name": "Calamares medianos en anillas", "amount": "600g (4 unidades)", "calories": 552, "protein": 96, "carbs": 18, "fat": 8},
            {"name": "Tomates maduros picados", "amount": "300g (2 tomates)", "calories": 54, "protein": 2.7, "carbs": 11, "fat": 0.6},
            {"name": "Pimiento verde y rojo", "amount": "270g", "calories": 65, "protein": 2.5, "carbs": 14, "fat": 0.5},
            {"name": "Cebolla mediana", "amount": "150g", "calories": 60, "protein": 1.8, "carbs": 13, "fat": 0.3},
            {"name": "Vino blanco", "amount": "125ml (1 vasito)", "calories": 105, "protein": 0, "carbs": 3, "fat": 0},
            {"name": "Aceite de oliva virgen", "amount": "30g (3 cucharadas)", "calories": 270, "protein": 0, "carbs": 0, "fat": 30},
            {"name": "Ajos, perejil, sal y laurel", "amount": "Al gusto", "calories": 10, "protein": 0.5, "carbs": 2, "fat": 0.1}
        ],
        "instructions": [
            "En una sartén con aceite dorar los calamares en anillas con 1 diente de ajo y perejil picado. Añadir el vino blanco y dejar reducir.",
            "En cazuela aparte, sofreír la cebolla, el tomate y los pimientos con 2 dientes de ajo hasta que estén tiernos.",
            "Incorporar los calamares a la cazuela de verduras y cocinar 5 minutos para integrar sabores.",
            "Añadir las alubias blancas con un poco de su caldo y cocinar todo junto a fuego suave durante 10 minutos."
        ],
        "per_serving": {
            "calories": 369.0,
            "protein": 27.3,
            "carbohydrates": 36.5,
            "fats": 9.7,
            "fiber": 6.8,
            "sugar": 4.1,
            "sodium": 360.0,
            "vitamins_and_minerals": ["Hierro: 4.8mg", "Fósforo: 310mg", "Vitamina C: 32mg"]
        },
        "total": {
            "calories": 1476.0,
            "protein": 109.0,
            "carbohydrates": 146.0,
            "fats": 38.6,
            "fiber": 27.2,
            "sugar": 16.4,
            "sodium": 1440.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Legumbres con pescado", "Alta en proteína", "Baja en grasa saturada"],
        "health_verdict": "Plato de cuchara ejemplar. La combinación de legumbre con cefalópodo asegura saciedad, bajo índice glucémico y alto valor biológico proteico.",
        "healthier_alternatives": ["Añadir unas hojas de espinaca en los últimos 3 minutos para un aporte extra de ácido fólico."]
    },
    {
        "id": "book-rioja-arroz-calabaza",
        "title": "Arroz con Calabaza al Horno",
        "description": "Receta levantina adaptada de arroz meloso al horno con calabaza asada, tomates naturales y cabeza de ajo confitada.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 30,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (Consejería de Salud)",
        "image_url": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Arroz de grano redondo", "amount": "250g (4 tacitas)", "calories": 890, "protein": 18, "carbs": 195, "fat": 1.5},
            {"name": "Calabaza fresca en dados", "amount": "300g", "calories": 84, "protein": 3, "carbs": 19, "fat": 0.3},
            {"name": "Tomates grandes maduros", "amount": "500g (2 unidades)", "calories": 90, "protein": 4.5, "carbs": 18, "fat": 1},
            {"name": "Dientes de ajo enteros", "amount": "40g (8 dientes)", "calories": 60, "protein": 2.5, "carbs": 13, "fat": 0.2},
            {"name": "Caldo de pollo y verduras casero", "amount": "1 litro (4 vasos)", "calories": 90, "protein": 6, "carbs": 4, "fat": 4},
            {"name": "Aceite de oliva virgen", "amount": "30g (3 cucharadas)", "calories": 270, "protein": 0, "carbs": 0, "fat": 30},
            {"name": "Azafrán en hebra y sal", "amount": "Al gusto", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "En una cazuela de barro poner el aceite con el azafrán, añadir el arroz y nacarar removiendo bien.",
            "Añadir la calabaza cortada en dados de 1 cm y verter el caldo caliente.",
            "Colocar los tomates partidos por la mitad en los bordes y la cabeza de ajos en el centro.",
            "Hornear a 200°C durante 30 minutos hasta que el arroz haya absorbido todo el caldo y esté en su punto."
        ],
        "per_serving": {
            "calories": 348.5,
            "protein": 6.9,
            "carbohydrates": 60.8,
            "fats": 8.7,
            "fiber": 3.4,
            "sugar": 5.2,
            "sodium": 310.0,
            "vitamins_and_minerals": ["Betacarotenos: 1400mcg", "Vitamina C: 25mg", "Potasio: 420mg"]
        },
        "total": {
            "calories": 1394.0,
            "protein": 27.4,
            "carbohydrates": 243.0,
            "fats": 34.8,
            "fiber": 13.6,
            "sugar": 20.8,
            "sodium": 1240.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Vegetariano", "Carbohidratos energéticos", "Sin gluten"],
        "health_verdict": "Plato reconfortante y antioxidante gracias a los betacarotenos de la calabaza y el licopeno del tomate asado.",
        "healthier_alternatives": ["Utilizar arroz integral para duplicar el contenido de fibra."]
    },
    {
        "id": "book-rioja-bacalao-patatas",
        "title": "Bacalao al Horno con Patatas y Cebolla",
        "description": "Receta clásica y jugosa horneada en fuente de barro con láminas de patata, cebolla pochada y lomos tiernos de bacalao.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (Consejería de Salud)",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Lomos de bacalao desalado", "amount": "600g (4 trozos)", "calories": 492, "protein": 108, "carbs": 0, "fat": 6},
            {"name": "Patatas medianas", "amount": "800g (4 patatas)", "calories": 616, "protein": 16, "carbs": 136, "fat": 0.8},
            {"name": "Cebollas medianas en aros", "amount": "600g (4 unidades)", "calories": 240, "protein": 7.2, "carbs": 52, "fat": 1.2},
            {"name": "Huevos camperos", "amount": "180g (3 unidades)", "calories": 225, "protein": 19.5, "carbs": 1.5, "fat": 15},
            {"name": "Aceite de oliva virgen", "amount": "40g (4 cucharadas)", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Pimienta y sal", "amount": "Al gusto", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Cortar las patatas en rodajas de 1/2 cm y las cebollas en aros finos. Freír o pochar ligeramente en la sartén.",
            "En una fuente de horno colocar una base con la mitad de las patatas y cebollas.",
            "Disponer los lomos de bacalao y cubrir con el resto de patatas y cebollas.",
            "Batir los huevos y verter sobre la fuente para amalgamar todo.",
            "Hornear a 180°C durante 15 minutos hasta dorar y cuajar el huevo."
        ],
        "per_serving": {
            "calories": 498.5,
            "protein": 50.5,
            "carbohydrates": 39.0,
            "fats": 15.7,
            "fiber": 4.6,
            "sugar": 5.8,
            "sodium": 480.0,
            "vitamins_and_minerals": ["Vitamina B12: 2.8mcg", "Fósforo: 390mg", "Potasio: 890mg"]
        },
        "total": {
            "calories": 1994.0,
            "protein": 202.0,
            "carbohydrates": 156.0,
            "fats": 62.6,
            "fiber": 18.4,
            "sugar": 23.2,
            "sodium": 1920.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína", "Pescado al horno", "Tradicional"],
        "health_verdict": "Aporte sobresaliente de más de 50g de proteína por persona con un contenido graso moderado y gran densidad de potasio.",
        "healthier_alternatives": ["Cocer las patatas al microondas en vez de freírlas para ahorrar 20g de aceite."]
    },

    # --- LIBRO: "Recetas de cocina saludable" (Pier Luigi Rossi / Aboca) ---
    {
        "id": "book-aboca-crema-budwig",
        "title": "Crema Budwig Funcional al Limón",
        "description": "Desayuno terapéutico molecular concebido por la Dra. Kousmine y el Dr. Rossi que regula el pico glucémico con semillas de lino prensadas y yogur.",
        "servings": 1,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Dr. Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Yogur desnatado natural o de soja", "amount": "4 cucharaditas (60g)", "calories": 36, "protein": 3.4, "carbs": 4.2, "fat": 0.2},
            {"name": "Aceite de lino prensado en frío", "amount": "2 cucharaditas (10ml)", "calories": 90, "protein": 0, "carbs": 0, "fat": 10},
            {"name": "Zumo de medio limón", "amount": "15ml", "calories": 4, "protein": 0.1, "carbs": 1, "fat": 0},
            {"name": "Granos de cereales integrales molidos", "amount": "2 cucharaditas (15g)", "calories": 52, "protein": 1.8, "carbs": 10, "fat": 0.5},
            {"name": "Semillas oleaginosas (almendras/nueces/sésamo)", "amount": "2 cucharaditas (12g)", "calories": 72, "protein": 2.4, "carbs": 1.5, "fat": 6.5},
            {"name": "Plátano maduro", "amount": "1 unidad (100g)", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
            {"name": "Fruta fresca de temporada cortada", "amount": "150g", "calories": 75, "protein": 1, "carbs": 18, "fat": 0.2}
        ],
        "instructions": [
            "En un bol batir el yogur con el aceite de lino con un tenedor hasta conseguir una emulsión cremosa.",
            "Añadir el zumo de limón y mezclar.",
            "Moler los cereales integrales y las semillas oleaginosas en un molinillo y añadirlos al bol.",
            "Aplastar el plátano con tenedor e incorporar a la crema.",
            "Coronar con la fruta fresca de temporada cortada en gajos."
        ],
        "per_serving": {
            "calories": 278.0,
            "protein": 6.4,
            "carbohydrates": 50.1,
            "fats": 13.7,
            "fiber": 6.3,
            "sugar": 24.0,
            "sodium": 45.0,
            "vitamins_and_minerals": ["Omega-3 (ALA): 5.5g", "ORAC: 4936 u", "Vitamina C: 35mg"]
        },
        "total": {
            "calories": 278.0,
            "protein": 6.4,
            "carbohydrates": 50.1,
            "fats": 13.7,
            "fiber": 6.3,
            "sugar": 24.0,
            "sodium": 45.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Desayuno molecular", "Rico en Omega-3", "Vegetariano", "Antiinflamatorio"],
        "health_verdict": "Emulsión funcional de alto poder antioxidante (ORAC 4936). Evita picos de insulina matutinos y nutre la microbiota intestinal.",
        "healthier_alternatives": ["Utilizar frutos rojos (arándanos y frambuesas) como fruta fresca para reducir la carga glucémica."]
    },
    {
        "id": "book-aboca-espaguetis-pulpo",
        "title": "Espaguetis Integrales con Pulpo y Tomatitos",
        "description": "Receta mediterránea anti-pico glucémico con pasta integral al dente, pulpo tierno cocido y tomates cherry a la sartén.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 25,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Dr. Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Espaguetis integrales", "amount": "280g", "calories": 980, "protein": 36, "carbs": 196, "fat": 6},
            {"name": "Pulpo cocido troceado", "amount": "500g", "calories": 410, "protein": 90, "carbs": 11, "fat": 5},
            {"name": "Tomates cherry partidos", "amount": "200g", "calories": 36, "protein": 1.8, "carbs": 7.8, "fat": 0.4},
            {"name": "Aceite de oliva virgen extra", "amount": "30ml", "calories": 270, "protein": 0, "carbs": 0, "fat": 30},
            {"name": "Perejil fresco, pimienta y sal", "amount": "Al gusto", "calories": 5, "protein": 0.3, "carbs": 1, "fat": 0}
        ],
        "instructions": [
            "Cocer los espaguetis integrales al dente en abundante agua con sal.",
            "En sartén saltear el pulpo cocido troceado con 1 cucharada de AOVE y los tomates cherry durante 5 minutos.",
            "Escurrir la pasta e incorporar directamente a la sartén con el pulpo.",
            "Saltear todo junto durante 2 minutos y rematar con abundante perejil fresco picado y pimienta negra molida."
        ],
        "per_serving": {
            "calories": 472.0,
            "protein": 38.6,
            "carbohydrates": 50.0,
            "fats": 13.9,
            "fiber": 8.7,
            "sugar": 3.8,
            "sodium": 340.0,
            "vitamins_and_minerals": ["Hierro: 5.4mg", "Vitamina B12: 18mcg", "Selenio: 45mcg"]
        },
        "total": {
            "calories": 1888.0,
            "protein": 154.5,
            "carbohydrates": 200.2,
            "fats": 55.5,
            "fiber": 34.7,
            "sugar": 15.2,
            "sodium": 1360.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Pasta saludable", "Alta en proteína", "Rico en fibra", "Mariscos"],
        "health_verdict": "Demuestra que la pasta puede ser un plato de índice glucémico controlado y muy nutritivo cuando se elige integral al dente y se combina con proteína marina magra.",
        "healthier_alternatives": ["Comenzar la comida con una ensalada de hojas amargas (escarola o rúcula) para reducir aún más el pico postprandial."]
    }
]

def import_all():
    print(f"Importando {len(BOOK_RECIPES)} recetas de los libros...")
    for rec in BOOK_RECIPES:
        save_recipe(rec)
    print("¡Recetas importadas con éxito!")

if __name__ == "__main__":
    import_all()
