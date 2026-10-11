import json
import sqlite3
from app.database import save_recipe

RECIPES_TO_IMPORT = [
    # =========================================================================
    # LIBRO: "Cocina sana para los peques... y toda la familia" (La Rioja Salud)
    # (Los valores nutricionales del libro están calculados para 4 personas)
    # =========================================================================
    {
        "id": "book-rioja-garbanzos-arroz-horno",
        "title": "Garbanzos con Arroz al Horno en Cazuela de Barro",
        "description": "Receta tradicional de legumbres con arroz, patatas, tomates, pimiento rojo y cabeza de ajos asada al horno.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 30,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Garbanzos secos cocidos", "amount": "120g", "calories": 420, "protein": 24, "carbs": 65, "fat": 6},
            {"name": "Arroz redondo", "amount": "240g", "calories": 840, "protein": 18, "carbs": 185, "fat": 2},
            {"name": "Tomates medianos", "amount": "450g (3 unidades)", "calories": 81, "protein": 4, "carbs": 17, "fat": 0.9},
            {"name": "Patata mediana", "amount": "170g (1 unidad)", "calories": 130, "protein": 3.4, "carbs": 29, "fat": 0.2},
            {"name": "Pimiento rojo", "amount": "100g", "calories": 26, "protein": 1, "carbs": 6, "fat": 0.2},
            {"name": "Cabeza de ajos entera", "amount": "50g", "calories": 70, "protein": 3, "carbs": 16, "fat": 0.2},
            {"name": "Aceite de oliva virgen extra", "amount": "40g (4 cucharadas)", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Caldo de cocción, pimentón dulce, laurel y azafrán", "amount": "Al gusto", "calories": 42, "protein": 0.9, "carbs": 11, "fat": 0.1}
        ],
        "instructions": [
            "Poner los garbanzos en remojo la víspera y cocerlos con agua, sal y la cabeza de ajos hasta que estén tiernos. Reservar caldo.",
            "Pelar las patatas y cortarlas en rodajas finas. Cortar los tomates en rodajas gruesas y los pimientos en tiras.",
            "En una cazuela de barro poner el aceite, arroz, garbanzos, pimentón, azafrán, laurel y 8 tazas de caldo caliente.",
            "Disponer encima las rodajas de patata, tomate y pimiento. Colocar en el centro la cabeza de ajos entera.",
            "Hornear a 180°C durante 30 minutos hasta que el arroz absorba el caldo."
        ],
        "per_serving": {
            "calories": 492.25,
            "protein": 12.82,
            "carbohydrates": 82.25,
            "fats": 12.40,
            "fiber": 8.5,
            "sugar": 5.8,
            "sodium": 320.0
        },
        "total": {
            "calories": 1969.0,
            "protein": 51.3,
            "carbohydrates": 329.0,
            "fats": 49.6,
            "fiber": 34.0,
            "sugar": 23.2,
            "sodium": 1280.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Plato completo", "Sin gluten", "Tradicional de La Rioja"],
        "health_verdict": "Plato completo que combina legumbre y cereal, aportando todos los aminoácidos esenciales con bajo aporte graso.",
        "healthier_alternatives": ["Añadir una ensalada fresca de escarola o tomate para sumar vitamina C que aumente la absorción del hierro."]
    },
    {
        "id": "book-rioja-garbanzos-espinacas-huevo",
        "title": "Garbanzos con Espinacas y Huevo Duro",
        "description": "Potaje casero tradicional de garbanzos guisados con espinacas frescas, sofrito de tomate al pimentón y rodajas de huevo duro.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 35,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Garbanzos secos", "amount": "240g", "calories": 840, "protein": 48, "carbs": 130, "fat": 12},
            {"name": "Espinacas frescas", "amount": "600g (2 bolsas)", "calories": 138, "protein": 17, "carbs": 21, "fat": 2.4},
            {"name": "Arroz redondo", "amount": "30g (1 puñado)", "calories": 105, "protein": 2.2, "carbs": 23, "fat": 0.3},
            {"name": "Huevos camperos medianos", "amount": "140g (2 unidades)", "calories": 190, "protein": 16.5, "carbs": 1.2, "fat": 13.2},
            {"name": "Dientes de ajo", "amount": "10g", "calories": 14, "protein": 0.6, "carbs": 3.1, "fat": 0.05},
            {"name": "Tomate triturado natural", "amount": "45g", "calories": 9, "protein": 0.4, "carbs": 1.8, "fat": 0.1},
            {"name": "Aceite de oliva virgen extra", "amount": "40g (4 cucharadas)", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Pimentón dulce y sal", "amount": "Al gusto", "calories": 6, "protein": 0.3, "carbs": 1, "fat": 0.2}
        ],
        "instructions": [
            "Poner los garbanzos a remojo la noche anterior. Cocer en cazuela con agua, aceite y sal durante 40 min (o 20 min en olla exprés).",
            "A mitad de la cocción incorporar el puñadito de arroz y las espinacas frescas.",
            "Cocer los huevos durante 10 minutos, pelar y cortar en rodajas.",
            "Hacer un sofrito con el AOVE, ajos y tomate natural. Añadir el pimentón dulce al final para que no se queme.",
            "Verter el sofrito a los garbanzos, hervir 5 minutos para unificar sabores y servir con las rodajas de huevo duro."
        ],
        "per_serving": {
            "calories": 396.5,
            "protein": 19.42,
            "carbohydrates": 41.75,
            "fats": 16.90,
            "fiber": 9.2,
            "sugar": 4.1,
            "sodium": 280.0
        },
        "total": {
            "calories": 1586.0,
            "protein": 77.7,
            "carbohydrates": 167.0,
            "fats": 67.6,
            "fiber": 36.8,
            "sugar": 16.4,
            "sodium": 1120.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Rico en hierro y folato", "Plato único", "Sin gluten"],
        "health_verdict": "Plato completo nutricionalmente equilibrado. Las espinacas y garbanzos aportan abundante fibra y magnesio, y el huevo aporta colina y vitamina B12.",
        "healthier_alternatives": ["Puede ser plato único acompañado de una fruta cítrica de postre."]
    },
    {
        "id": "book-rioja-lentejas-acelgas-bacalao",
        "title": "Lentejas Pardinas con Acelgas y Lomos de Bacalao",
        "description": "Guiso marinero de lentejas estofadas con acelga troceada, sofrito de pimentón y lomos de bacalao jugosos cocinados al microondas.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 30,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Bacalao fresco o desalado", "amount": "600g (4 lomos)", "calories": 492, "protein": 108, "carbs": 0, "fat": 6},
            {"name": "Lentejas pardinas", "amount": "200g", "calories": 700, "protein": 52, "carbs": 120, "fat": 3},
            {"name": "Hojas de acelga sin penca", "amount": "600g", "calories": 114, "protein": 10.8, "carbs": 22.2, "fat": 1.2},
            {"name": "Zanahorias grandes", "amount": "200g", "calories": 80, "protein": 1.8, "carbs": 18, "fat": 0.4},
            {"name": "Cebolla", "amount": "150g", "calories": 60, "protein": 1.8, "carbs": 14, "fat": 0.2},
            {"name": "Dientes de ajo", "amount": "15g (3 unidades)", "calories": 21, "protein": 0.9, "carbs": 4.8, "fat": 0.08},
            {"name": "Aceite de oliva virgen extra", "amount": "40g (4 cucharadas)", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Laurel, pimentón dulce y sal", "amount": "Al gusto", "calories": 8, "protein": 0.4, "carbs": 1.5, "fat": 0.2}
        ],
        "instructions": [
            "Cocer las lentejas con la cebolla, zanahoria, ajo y laurel durante 25-30 minutos en cazuela.",
            "Añadir la acelga troceada cuando falten 10 minutos para terminar la cocción.",
            "Cocinar los lomos de bacalao al microondas tapados durante 6-8 minutos.",
            "Hacer un sofrito con el AOVE, ajos picados y pimentón dulce y añadir a las lentejas.",
            "Servir colocando los lomos de bacalao en el fondo del plato y vertiendo las lentejas con acelgas por encima."
        ],
        "per_serving": {
            "calories": 394.25,
            "protein": 35.00,
            "carbohydrates": 37.00,
            "fats": 11.85,
            "fiber": 11.4,
            "sugar": 5.2,
            "sodium": 390.0
        },
        "total": {
            "calories": 1577.0,
            "protein": 140.0,
            "carbohydrates": 148.0,
            "fats": 47.4,
            "fiber": 45.6,
            "sugar": 20.8,
            "sodium": 1560.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína magra", "Rico en hierro y fibra", "Pescado y legumbre", "Sin gluten"],
        "health_verdict": "35g de proteína magra con apenas 394 kcal. La combinación de pescado blanco y legumbre proporciona un perfil nutricional insuperable.",
        "healthier_alternatives": ["Añadir unas gotas de limón al servir para potenciar la asimilación del hierro no hemo."]
    },
    {
        "id": "book-rioja-pochas-con-verduras",
        "title": "Pochas Frescas Guisadas con Verduras de la Huerta",
        "description": "Guiso tradicional riojano de alubias pochas tiernas cocinadas con calabaza, pimientos de colores, cebolla y refrito de ajo.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 45,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1547496502-affa22d38842?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pochas frescas (o congeladas)", "amount": "600g", "calories": 660, "protein": 46, "carbs": 114, "fat": 3},
            {"name": "Calabaza en dados", "amount": "150g", "calories": 39, "protein": 1.5, "carbs": 9.8, "fat": 0.2},
            {"name": "Tomate maduro", "amount": "150g", "calories": 27, "protein": 1.3, "carbs": 6, "fat": 0.3},
            {"name": "Pimiento verde", "amount": "100g", "calories": 20, "protein": 0.9, "carbs": 4.6, "fat": 0.2},
            {"name": "Pimiento rojo", "amount": "90g", "calories": 24, "protein": 0.9, "carbs": 5.4, "fat": 0.2},
            {"name": "Cebolla", "amount": "100g", "calories": 40, "protein": 1.2, "carbs": 9.2, "fat": 0.1},
            {"name": "Dientes de ajo", "amount": "20g (4 unidades)", "calories": 28, "protein": 1.2, "carbs": 6.4, "fat": 0.1},
            {"name": "Aceite de oliva virgen extra", "amount": "30g (3 cucharadas)", "calories": 270, "protein": 0, "carbs": 0, "fat": 30},
            {"name": "Pimentón dulce y sal", "amount": "Al gusto", "calories": 6, "protein": 0.3, "carbs": 1, "fat": 0.2}
        ],
        "instructions": [
            "Lavar y cortar en cuadraditos la calabaza, los pimientos, la cebolla y el tomate. Picar el ajo menudito.",
            "Poner en una cazuela las pochas frescas con todas las hortalizas excepto el ajo. Cubrir de agua y cocer 45 min (o 10 min en olla rápida).",
            "Hacer un sofrito con el AOVE y el ajo picado, añadir el pimentón e inmediatamente incorporar a la cazuela con las pochas.",
            "Dejar hervir todo junto 5 minutos para unificar sabores y servir templado."
        ],
        "per_serving": {
            "calories": 310.5,
            "protein": 14.88,
            "carbohydrates": 42.75,
            "fats": 8.85,
            "fiber": 10.6,
            "sugar": 5.8,
            "sodium": 240.0
        },
        "total": {
            "calories": 1242.0,
            "protein": 59.5,
            "carbohydrates": 171.0,
            "fats": 35.4,
            "fiber": 42.4,
            "sugar": 23.2,
            "sodium": 960.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Cocina riojana tradicional", "Rico en fibra", "Bajo en grasa", "Sin gluten"],
        "health_verdict": "Las pochas frescas son tiernas y de fácil digestión. Gran aporte de fibra soluble, antioxidantes y minerales con menos de 320 kcal.",
        "healthier_alternatives": ["Añadir piparras en vinagre como guarnición tradicional."]
    },
    {
        "id": "book-rioja-alcachofas-con-jamon",
        "title": "Alcachofas Naturales Salteadas con Jamón Serrano",
        "description": "Alcachofas cocidas al dente salteadas en sartén con tacos de jamón serrano, ajo y una salsa ligera de su propio caldo.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Alcachofas naturales limpias", "amount": "800g (2 docenas)", "calories": 376, "protein": 24, "carbs": 84, "fat": 1.6},
            {"name": "Jamón serrano magro en tiras", "amount": "120g (4 lonchas)", "calories": 250, "protein": 36, "carbs": 0.5, "fat": 11},
            {"name": "Aceite de oliva virgen extra", "amount": "40g (3 cucharadas)", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Harina de trigo (para ligar)", "amount": "17g (1 cucharada)", "calories": 60, "protein": 1.7, "carbs": 12.8, "fat": 0.2},
            {"name": "Dientes de ajo", "amount": "15g (3 unidades)", "calories": 21, "protein": 0.9, "carbs": 4.8, "fat": 0.08},
            {"name": "Sal", "amount": "Pizca", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Limpiar las alcachofas retirando hojas duras y puntas. Cocer en agua hirviendo con un poco de limón durante 20-25 minutos.",
            "Escurrir reservando medio vaso de su caldo de cocción.",
            "En una sartén calentar el AOVE, rehogar los ajos picados y añadir el jamón serrano y la harina.",
            "Remover bien, añadir un poco del caldo de las alcachofas reservado hasta crear una salsa ligera.",
            "Verter la salsa y el jamón sobre las alcachofas calientes y dar un hervor conjunto de 2 minutos."
        ],
        "per_serving": {
            "calories": 245.25,
            "protein": 14.82,
            "carbohydrates": 20.25,
            "fats": 11.68,
            "fiber": 8.8,
            "sugar": 2.5,
            "sodium": 440.0
        },
        "total": {
            "calories": 981.0,
            "protein": 59.3,
            "carbohydrates": 81.0,
            "fats": 46.7,
            "fiber": 35.2,
            "sugar": 10.0,
            "sodium": 1760.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Bajo en calorías", "Rico en cinarina", "Depurativo", "Alto en fibra"],
        "health_verdict": "Plato depurativo por excelencia. La cinarina de la alcachofa favorece la función biliar y el jamón aporta proteína magra saciante.",
        "healthier_alternatives": ["Para celíacos, sustituir la harina de trigo por harina de maíz (maicena)."]
    },
    {
        "id": "book-rioja-pastel-berenjena-jamon-queso",
        "title": "Pastel de Berenjenas al Horno con Jamón y Queso",
        "description": "Capas de berenjena al microondas intercaladas con jamón cocido, queso tierno y tomate, cuajadas al horno con huevo batido.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 20,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Berenjenas grandes", "amount": "700g (2 unidades)", "calories": 175, "protein": 7, "carbs": 42, "fat": 1.4},
            {"name": "Jamón cocido de calidad", "amount": "240g (8 lonchas)", "calories": 260, "protein": 43, "carbs": 2.4, "fat": 8.8},
            {"name": "Queso en lonchas", "amount": "240g (12 lonchas)", "calories": 780, "protein": 55, "carbs": 3.6, "fat": 62},
            {"name": "Tomate frito casero", "amount": "60g (4 cucharadas)", "calories": 48, "protein": 0.8, "carbs": 5, "fat": 2.8},
            {"name": "Huevos camperos", "amount": "120g (2 unidades)", "calories": 160, "protein": 14, "carbs": 1, "fat": 11.2},
            {"name": "Sal y pimienta", "amount": "Al gusto", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Lavar las berenjenas, cortarlas en rodajas de 0.5 cm y ablandarlas en el microondas 5 minutos para que no absorban grasa.",
            "En una fuente de horno poner una base ligera de tomate frito.",
            "Colocar una capa de berenjena, una de jamón y otra de queso. Repetir el proceso dos veces terminando con berenjena.",
            "Batir los huevos con sal y pimienta y verterlos por encima de todo el pastel para que penetren.",
            "Hornear a 180°C durante 15-20 minutos hasta que el huevo esté cuajado y dorado."
        ],
        "per_serving": {
            "calories": 431.5,
            "protein": 33.75,
            "carbohydrates": 8.78,
            "fats": 28.75,
            "fiber": 5.8,
            "sugar": 4.2,
            "sodium": 520.0
        },
        "total": {
            "calories": 1726.0,
            "protein": 135.0,
            "carbohydrates": 35.1,
            "fats": 115.0,
            "fiber": 23.2,
            "sugar": 16.8,
            "sodium": 2080.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Alta en proteína", "Baja en hidratos", "Keto friendly", "Favorito de los niños"],
        "health_verdict": "Excelente manera de que los niños coman verdura. Aporta casi 34g de proteína con bajo contenido en carbohidratos.",
        "healthier_alternatives": ["Usar queso tierno bajo en grasa para reducir calorías totales."]
    },
    {
        "id": "book-rioja-guisantes-sepia",
        "title": "Guisantes Tiernos Estofados con Sepia",
        "description": "Guiso marinero ligero de sepia fresca en dados con guisantes congelados en salsa de cebolla, ajo y tomate natural.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Sepia mediana limpia", "amount": "600g", "calories": 480, "protein": 96, "carbs": 4.8, "fat": 6},
            {"name": "Guisantes ultracongelados", "amount": "700g", "calories": 567, "protein": 37.8, "carbs": 100.8, "fat": 2.8},
            {"name": "Cebolla o cebolleta", "amount": "100g", "calories": 40, "protein": 1.2, "carbs": 9.2, "fat": 0.1},
            {"name": "Tomate triturado natural", "amount": "150g (10 cucharadas)", "calories": 30, "protein": 1.5, "carbs": 6, "fat": 0.3},
            {"name": "Dientes de ajo", "amount": "10g (2 unidades)", "calories": 14, "protein": 0.6, "carbs": 3.1, "fat": 0.05},
            {"name": "Aceite de oliva virgen extra", "amount": "40g (4 cucharadas)", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Sal y agua", "amount": "Al gusto", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "En una sartén con el AOVE caliente pochar la cebolla y los ajos picados.",
            "Cuando empiecen a dorarse añadir la sepia limpia cortada en cuadrados y rehogar 5 minutos.",
            "Añadir el tomate triturado natural y dejar hacer removiendo hasta que reduzca.",
            "Añadir los guisantes y un vaso de agua, tapar y dejar hervir suavemente 10-12 minutos.",
            "Servir caliente en plato hondo."
        ],
        "per_serving": {
            "calories": 347.5,
            "protein": 29.25,
            "carbohydrates": 20.18,
            "fats": 16.63,
            "fiber": 8.9,
            "sugar": 5.8,
            "sodium": 340.0
        },
        "total": {
            "calories": 1390.0,
            "protein": 117.0,
            "carbohydrates": 80.7,
            "fats": 66.5,
            "fiber": 35.6,
            "sugar": 23.2,
            "sodium": 1360.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína magra", "Rico en fibra", "Guiso marinero", "Sin gluten"],
        "health_verdict": "Casi 30g de proteína de altísimo valor biológico procedente de la sepia, combinada con fibra soluble de los guisantes.",
        "healthier_alternatives": ["Añadir una pizca de pimentón picante para un toque marinero más aromático."]
    },
    {
        "id": "book-rioja-salpicon-marisco",
        "title": "Salpicón Tradicional de Marisco y Pulpo",
        "description": "Ensalada fría marinera con pulpo cocido, gambas, mejillones al vapor, pimientos de colores, cebolleta y vinagreta al perejil.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Cocina sana para los peques y toda la familia (La Rioja Salud)",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pulpo cocido en rodajas", "amount": "300g", "calories": 250, "protein": 52, "carbs": 4, "fat": 2.5},
            {"name": "Gambas peladas cocidas", "amount": "100g", "calories": 85, "protein": 20, "carbs": 1, "fat": 1},
            {"name": "Mejillones cocidos sin concha", "amount": "120g", "calories": 105, "protein": 14, "carbs": 3.6, "fat": 2.5},
            {"name": "Barritas de surimi (chaca)", "amount": "100g (5 barritas)", "calories": 95, "protein": 8, "carbs": 12, "fat": 1},
            {"name": "Tomate maduro en dados", "amount": "150g", "calories": 27, "protein": 1.3, "carbs": 6, "fat": 0.3},
            {"name": "Pimiento rojo y verde en dados", "amount": "240g", "calories": 55, "protein": 2.2, "carbs": 12, "fat": 0.5},
            {"name": "Aceitunas y pepinillos en vinagre", "amount": "110g", "calories": 90, "protein": 1.2, "carbs": 4, "fat": 7.5},
            {"name": "AOVE (40ml) y vinagre de vino (14ml)", "amount": "Al gusto", "calories": 360, "protein": 0, "carbs": 0, "fat": 40}
        ],
        "instructions": [
            "Cocer los mejillones al vapor y retirar las conchas. Cocer las gambas brevemente.",
            "Cortar en rodajas el pulpo y el surimi.",
            "Lavar y cortar en daditos pequeños el tomate y los pimientos rojo y verde. Picar las cebolletas y pepinillos.",
            "En un bote con tapa preparar la vinagreta con el AOVE, vinagre, sal y perejil picado fino; agitar con fuerza.",
            "Mezclar todos los mariscos y hortalizas en un bol grande, rociar con la vinagreta y servir bien frío."
        ],
        "per_serving": {
            "calories": 231.0,
            "protein": 18.48,
            "carbohydrates": 5.28,
            "fats": 15.13,
            "fiber": 2.8,
            "sugar": 3.2,
            "sodium": 460.0
        },
        "total": {
            "calories": 924.0,
            "protein": 73.9,
            "carbohydrates": 21.1,
            "fats": 60.5,
            "fiber": 11.2,
            "sugar": 12.8,
            "sodium": 1840.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Rico en yodo y zinc", "Bajo en calorías", "Sin gluten", "Proteína marina pura"],
        "health_verdict": "Plato festivo fresco y ligero. Riqueza excepcional en minerales marinos (yodo, zinc, selenio, hierro de mejillones).",
        "healthier_alternatives": ["Añadir patata cocida en dados si se desea convertir en un plato único completo."]
    },

    # =========================================================================
    # LIBRO: "Recetas de cocina saludable" (Pier Luigi Rossi / Aboca Edizioni)
    # (Alimentación molecular consciente: control de picos glucémicos y ORAC)
    # =========================================================================
    {
        "id": "book-aboca-crema-budwig",
        "title": "Crema Budwig Funcional al Limón y Semillas",
        "description": "Desayuno funcional regenerador celular con yogur, aceite de lino prensado en frío, cereales integrales molidos y fruta fresca.",
        "servings": 1,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Yogur desnatado natural o de soja", "amount": "4 cucharaditas (60g)", "calories": 40, "protein": 3.5, "carbs": 4, "fat": 0.2},
            {"name": "Aceite de lino prensado en frío", "amount": "2 cucharaditas (10ml)", "calories": 90, "protein": 0, "carbs": 0, "fat": 10},
            {"name": "Zumo de medio limón", "amount": "20ml", "calories": 5, "protein": 0.1, "carbs": 1.5, "fat": 0.05},
            {"name": "Granos de cereales integrales molidos", "amount": "2 cucharaditas (20g)", "calories": 70, "protein": 2.2, "carbs": 14, "fat": 0.5},
            {"name": "Semillas oleaginosas (nueces, sésamo, almendras)", "amount": "2 cucharaditas (15g)", "calories": 95, "protein": 3, "carbs": 2.5, "fat": 8},
            {"name": "Plátano maduro aplastado", "amount": "1 unidad (100g)", "calories": 90, "protein": 1.2, "carbs": 23, "fat": 0.3},
            {"name": "Fruta fresca de temporada en trozos", "amount": "150g", "calories": 75, "protein": 0.9, "carbs": 18, "fat": 0.3}
        ],
        "instructions": [
            "En un bol, bate el yogur con el aceite de lino con un tenedor hasta conseguir una emulsión cremosa.",
            "Añade el zumo de limón recién exprimido y mezcla bien.",
            "Muele al momento los granos de cereales integrales y las semillas oleaginosas e incorpóralos al bol.",
            "Aplasta el plátano maduro con el tenedor hasta formar una papilla suave y mézclalo en la crema.",
            "Decora por encima con la fruta fresca de temporada pelada y cortada en trocitos."
        ],
        "per_serving": {
            "calories": 465.0,
            "protein": 6.38,
            "carbohydrates": 50.12,
            "fats": 13.68,
            "fiber": 6.28,
            "sugar": 24.5,
            "sodium": 45.0,
            "vitamins_and_minerals": ["ORAC antioxidante: 4936 u", "Omega-3 (ALA): 5.5g", "Potasio: 520mg"]
        },
        "total": {
            "calories": 465.0,
            "protein": 6.38,
            "carbohydrates": 50.12,
            "fats": 13.68,
            "fiber": 6.28,
            "sugar": 24.5,
            "sodium": 45.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Antioxidante ORAC", "Rico en Omega-3 vegetal", "Alimentación molecular", "Sin colesterol"],
        "health_verdict": "Fórmula célebre de la Dra. Kousmine adaptada por Pier Luigi Rossi. El aceite de lino emulsionado con yogur aporta ácidos grasos esenciales protectores mitocondriales.",
        "healthier_alternatives": ["Añadir arándanos silvestres para elevar el valor ORAC por encima de 6000 u."]
    },
    {
        "id": "book-aboca-lenguado-esparragos-avellanas",
        "title": "Lenguado con Crema de Espárragos y Avellanas",
        "description": "Filetes de lenguado cocinados en su propio caldo de espárragos con salsa emulsionada de tallos, mejorana y avellanas picadas.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Espárragos verdes frescos", "amount": "500g", "calories": 100, "protein": 11, "carbs": 19, "fat": 1},
            {"name": "Filetes de lenguado frescos", "amount": "4 filetes de ración", "calories": 480, "protein": 98, "carbs": 0, "fat": 6},
            {"name": "Mejorana fresca", "amount": "1 manojo", "calories": 5, "protein": 0.2, "carbs": 1, "fat": 0.05},
            {"name": "Avellanas tostadas peladas", "amount": "25g", "calories": 162, "protein": 3.7, "carbs": 4.2, "fat": 15.2},
            {"name": "Aceite de oliva virgen extra", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20},
            {"name": "Sal marina", "amount": "Pizca", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Lavar los espárragos y separar las yemas de los tallos.",
            "Hervir las yemas durante 2-3 minutos en agua con sal y enfriar en agua con hielo para fijar la clorofila.",
            "En la misma agua hervir los tallos 10 minutos; escurrir conservando el caldo y batirlos con la mejorana, AOVE y un poco de caldo.",
            "En una sartén colocar los filetes de lenguado cubiertos con el caldo de espárragos y cocer 5 minutos a fuego suave.",
            "Servir la crema de espárragos en el fondo del plato, colocar el lenguado encima y decorar con las yemas y avellanas picadas."
        ],
        "per_serving": {
            "calories": 231.75,
            "protein": 22.90,
            "carbohydrates": 8.34,
            "fats": 8.51,
            "fiber": 5.15,
            "sugar": 2.4,
            "sodium": 180.0,
            "vitamins_and_minerals": ["ORAC antioxidante: 4791 u", "Colesterol bajo: 25mg", "Asparagina depurativa"]
        },
        "total": {
            "calories": 927.0,
            "protein": 91.58,
            "carbohydrates": 33.34,
            "fats": 34.02,
            "fiber": 20.59,
            "sugar": 9.6,
            "sodium": 720.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Proteico molecular", "Bajo en carbohidratos", "Alto ORAC", "Sin gluten"],
        "health_verdict": "Valor ORAC excepcional de 19167 u por receta total. Controla perfectamente el pico glucémico postprandial y aporta proteína limpia.",
        "healthier_alternatives": ["Completar la comida con una entrada de ensalada cruda amarga (rúcula o escarola) siguiendo el método Rossi."]
    },
    {
        "id": "book-aboca-pajaritas-espelta-alcachofas",
        "title": "Pajaritas de Espelta con Alcachofas y Calabacín al Limón",
        "description": "Pasta de espelta integral de bajo índice glucémico con gajos de alcachofa, tiras de calabacín, puerro pochado y guindilla.",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 15,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pasta tipo pajaritas de espelta integral", "amount": "320g", "calories": 1120, "protein": 44.8, "carbs": 224, "fat": 6.4},
            {"name": "Calabacín en juliana", "amount": "200g", "calories": 34, "protein": 2.4, "carbs": 6.2, "fat": 0.6},
            {"name": "Alcachofas frescas en gajos", "amount": "2 unidades (150g)", "calories": 70, "protein": 4.5, "carbs": 15.7, "fat": 0.3},
            {"name": "Puerro en tiras finas", "amount": "1 unidad (80g)", "calories": 48, "protein": 1.2, "carbs": 11.2, "fat": 0.2},
            {"name": "Diente de ajo, perejil y guindilla", "amount": "Al gusto", "calories": 10, "protein": 0.4, "carbs": 2, "fat": 0.05},
            {"name": "Zumo de limón", "amount": "15ml", "calories": 4, "protein": 0.1, "carbs": 1, "fat": 0.02},
            {"name": "Aceite de oliva virgen extra", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20}
        ],
        "instructions": [
            "Cortar las alcachofas en gajos finos y frotar con zumo de limón para evitar oxidación.",
            "En una cacerola baja antiadherente cocinar el puerro con el ajo pelado y unas cucharadas de agua.",
            "Añadir las alcachofas y cocinar 5 minutos. Añadir el calabacín en juliana y cocinar 10 minutos más.",
            "Cocer las pajaritas de espelta en abundante agua con sal hasta dejarlas al dente.",
            "Escurrir la pasta e integrarla con las verduras en la cazuela.",
            "Condimentar en crudo con el AOVE, perejil picado y unas láminas de guindilla fresca."
        ],
        "per_serving": {
            "calories": 366.5,
            "protein": 14.18,
            "carbohydrates": 61.89,
            "fats": 6.91,
            "fiber": 10.09,
            "sugar": 4.5,
            "sodium": 140.0,
            "vitamins_and_minerals": ["ORAC: 3058 u", "Fibra soluble: 10g", "Cinarina hepática"]
        },
        "total": {
            "calories": 1466.0,
            "protein": 56.72,
            "carbohydrates": 247.54,
            "fats": 27.65,
            "fiber": 40.34,
            "sugar": 18.0,
            "sodium": 560.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Bajo índice glucémico", "Rico en fibra", "Alimentación consciente"],
        "health_verdict": "La espelta integral cocinada al dente junto a la gran masa de verdura minimiza el pico insulínico postprandial frente a la pasta refinada.",
        "healthier_alternatives": ["Añadir tofu desmenuzado o dados de pechuga de pavo si se busca comida proteica."]
    },
    {
        "id": "book-aboca-espaguetis-pulpo-tomatitos",
        "title": "Espaguetis Integrales con Pulpo y Tomatitos",
        "description": "Pasta integral de trigo con pulpo tierno cocido en su jugo, tomates cherry salteados y perejil fresco picado.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 40,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Espaguetis integrales", "amount": "280g", "calories": 980, "protein": 39.2, "carbs": 196, "fat": 5.6},
            {"name": "Pulpo fresco mediano cocido", "amount": "600g", "calories": 510, "protein": 106, "carbs": 8, "fat": 5.1},
            {"name": "Tomates cherry partidos", "amount": "200g", "calories": 36, "protein": 1.8, "carbs": 7.8, "fat": 0.4},
            {"name": "Manojo de perejil fresco picado", "amount": "1 unidad", "calories": 10, "protein": 0.8, "carbs": 1.8, "fat": 0.2},
            {"name": "Aceite de oliva virgen extra", "amount": "40ml", "calories": 360, "protein": 0, "carbs": 0, "fat": 40},
            {"name": "Pimienta negra y sal", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.4, "fat": 0.05}
        ],
        "instructions": [
            "Sumergir el pulpo en agua hirviendo sin sal y cocer tapado a fuego lento 40 minutos hasta tierno. Cortar en trocitos.",
            "Saltear el pulpo en una sartén con una cucharada de AOVE, los tomates cherry cortados y sal marina.",
            "Cocer los espaguetis integrales al dente en agua salada y escurrir.",
            "Mezclar la pasta con el pulpo y tomatitos en la sartén.",
            "Completar el plato con abundante perejil fresco picado y pimienta negra molida."
        ],
        "per_serving": {
            "calories": 474.5,
            "protein": 38.63,
            "carbohydrates": 50.05,
            "fats": 13.87,
            "fiber": 8.68,
            "sugar": 3.8,
            "sodium": 360.0
        },
        "total": {
            "calories": 1898.0,
            "protein": 154.52,
            "carbohydrates": 200.20,
            "fats": 55.49,
            "fiber": 34.70,
            "sugar": 15.2,
            "sodium": 1440.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína marina", "Carbohidratos complejos", "Sin grasas saturadas", "Mediterráneo"],
        "health_verdict": "Casi 39g de proteína por ración gracias al pulpo (uno de los moluscos con menor grasa y mayor concentración de taurina y zinc).",
        "healthier_alternatives": ["Añadir rúcula picada justo antes de servir para sumar nitratos cardiosaludables."]
    },
    {
        "id": "book-aboca-solomillo-pesto-perejil",
        "title": "Solomillo de Ternera con Pesto Cítrico de Perejil",
        "description": "Filetes magros de solomillo marcados a la plancha perfumados con ajo y untados con pesto fresco de perejil, limón y romero.",
        "servings": 4,
        "prep_time_minutes": 5,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Filetes de solomillo de ternera", "amount": "4 unidades (550g)", "calories": 715, "protein": 115, "carbs": 0, "fat": 27.5},
            {"name": "Zumo de limón", "amount": "30ml", "calories": 8, "protein": 0.2, "carbs": 2.6, "fat": 0.05},
            {"name": "Diente de ajo", "amount": "5g", "calories": 7, "protein": 0.3, "carbs": 1.6, "fat": 0.05},
            {"name": "Manojo de perejil fresco picado", "amount": "1 unidad (20g)", "calories": 7, "protein": 0.6, "carbs": 1.3, "fat": 0.1},
            {"name": "Romero fresco", "amount": "2 ramitas", "calories": 4, "protein": 0.1, "carbs": 0.8, "fat": 0.2},
            {"name": "Aceite de oliva virgen extra", "amount": "25ml", "calories": 225, "protein": 0, "carbs": 0, "fat": 25},
            {"name": "Sal marina y pimienta molida", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.4, "fat": 0.05}
        ],
        "instructions": [
            "En un cuenco mezcla el AOVE, zumo de limón, perejil y romero muy picados con sal marina y pimienta.",
            "Calienta muy bien la plancha o sartén de hierro.",
            "Cocina los filetes 2 minutos por lado girando con paleta (sin pinchar para conservar los jugos).",
            "Frota la carne caliente con el diente de ajo para perfumar.",
            "Baja el fuego y termina de cocinar 1 minuto untando con la salsa de perejil y limón por ambos lados. Servir de inmediato."
        ],
        "per_serving": {
            "calories": 242.0,
            "protein": 27.11,
            "carbohydrates": 0.65,
            "fats": 8.07,
            "fiber": 0.61,
            "sugar": 0.3,
            "sodium": 190.0,
            "vitamins_and_minerals": ["Hierro hemo: 3.6mg", "Zinc: 5.4mg", "Vitamina C: 35mg"]
        },
        "total": {
            "calories": 968.0,
            "protein": 108.43,
            "carbohydrates": 2.60,
            "fats": 32.27,
            "fiber": 2.44,
            "sugar": 1.2,
            "sodium": 760.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Proteico molecular", "Keto friendly", "Ultra bajo en hidratos", "Sin gluten"],
        "health_verdict": "El aliño de perejil y limón no solo aromatiza sin grasas saturadas añadidas, sino que su vitamina C triplica la absorción del hierro hemo.",
        "healthier_alternatives": ["Acompañar con ensalada de endivias amargas según la pauta del método Rossi."]
    },
    {
        "id": "book-aboca-tiras-pollo-arroz-negro",
        "title": "Tiras de Pollo con Arroz Negro Venere y Jengibre",
        "description": "Arroz negro integral aromático acompañado de tiras de pechuga selladas a la plancha con calabacines, cebolla y jengibre al limón.",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 35,
        "source_type": "libro",
        "source_reference": "Recetas de cocina saludable (Pier Luigi Rossi / Aboca)",
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pechuga de pollo en tiras", "amount": "480g", "calories": 576, "protein": 105.6, "carbs": 0, "fat": 12},
            {"name": "Arroz negro tipo Venere", "amount": "160g", "calories": 560, "protein": 14.4, "carbs": 112, "fat": 4.8},
            {"name": "Calabacines pequeños", "amount": "4 unidades (400g)", "calories": 68, "protein": 4.8, "carbs": 12.4, "fat": 1.2},
            {"name": "Cebolla", "amount": "1 unidad (100g)", "calories": 40, "protein": 1.2, "carbs": 9.2, "fat": 0.1},
            {"name": "Zumo de limón y raíz de jengibre", "amount": "30g", "calories": 15, "protein": 0.4, "carbs": 3, "fat": 0.1},
            {"name": "Aceite de oliva virgen extra", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20},
            {"name": "Sal aromática", "amount": "Pizca", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Cocer el arroz negro Venere en agua hirviendo con sal durante 35-40 minutos.",
            "Cortar la pechuga de pollo en tiras y sellarlas en sartén plancha con unas gotas de AOVE 2 minutos.",
            "Añadir la cebolla y los calabacines cortados en rodajas muy finas.",
            "Remover y, cuando el pollo empiece a dorarse, añadir el zumo de limón y el jengibre fresco en tiras finas.",
            "Servir el pollo con las verduras jugosas y montar el arroz negro en forma de cúpula con ayuda de un cuenco."
        ],
        "per_serving": {
            "calories": 359.75,
            "protein": 31.90,
            "carbohydrates": 30.23,
            "fats": 7.26,
            "fiber": 4.38,
            "sugar": 3.8,
            "sodium": 220.0,
            "vitamins_and_minerals": ["Antocianinas del arroz venere: 180mg", "Ginsenosidos del jengibre", "ORAC: 1922 u"]
        },
        "total": {
            "calories": 1439.0,
            "protein": 127.61,
            "carbohydrates": 120.91,
            "fats": 29.04,
            "fiber": 17.50,
            "sugar": 15.2,
            "sodium": 880.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Fitness friendly", "Arroz negro antioxidante", "Alta en proteína", "Sin gluten"],
        "health_verdict": "El arroz Venere contiene 3 veces más antocianinas protectoras que el arroz blanco con un índice glucémico mucho más moderado.",
        "healthier_alternatives": ["Añadir semillas de sésamo tostado sobre el arroz."]
    }
]

def main():
    print(f"Importando {len(RECIPES_TO_IMPORT)} recetas adicionales de La Rioja Salud y Aboca...")
    for recipe in RECIPES_TO_IMPORT:
        saved = save_recipe(recipe)
        print(f"-> Guardada: {saved['title']}")
    print(f"¡Importación completada! Se han añadido {len(RECIPES_TO_IMPORT)} recetas a recipes.db.")

if __name__ == "__main__":
    main()
