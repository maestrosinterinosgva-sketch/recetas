import json
import sqlite3
from app.database import save_recipe

BOTICARIA_RECIPES = [
    {
        "id": "book-boticaria-chips-kale",
        "title": "Chips de Kale al Horno",
        "description": "Snack crujiente y ultraligero elaborado con col rizada horneada con AOVE y especias antioxidantes. Menos de 1€ por ración.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1524179091875-bf99a9a6fa57?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Col kale limpia", "amount": "300g", "calories": 172.8, "protein": 12.75, "carbs": 12.36, "fat": 8.04},
            {"name": "Aceite de oliva virgen extra (AOVE)", "amount": "5ml", "calories": 45, "protein": 0, "carbs": 0, "fat": 5},
            {"name": "Especias al gusto (cúrcuma, pimentón, ajo en polvo)", "amount": "Al gusto", "calories": 5, "protein": 0.25, "carbs": 0.24, "fat": 0.16},
            {"name": "Sal", "amount": "Pizca", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Precalienta el horno a 200°C (calor arriba y abajo).",
            "Corta el kale en trozos de unos 4 cm.",
            "Ponlos en un bol y mezcla con el AOVE (puedes usar un pulverizador para repartir bien).",
            "En una bandeja cubierta con papel de hornear dispón los trozos de kale sin amontonar.",
            "Hornea unos 10 minutos vigilando al final para que no se quemen.",
            "Deja enfriar y añade sal, cúrcuma, pimentón o ajo en polvo."
        ],
        "per_serving": {
            "calories": 88.1,
            "protein": 6.5,
            "carbohydrates": 6.3,
            "fats": 4.1,
            "fiber": 4.0,
            "sugar": 3.39,
            "saturated_fat": 0.56,
            "sodium": 120.0,
            "vitamins_and_minerals": ["Vitamina C: 120mg", "Vitamina K: 400mcg", "Calcio: 150mg"]
        },
        "total": {
            "calories": 176.2,
            "protein": 13.0,
            "carbohydrates": 12.6,
            "fats": 8.2,
            "fiber": 8.0,
            "sugar": 6.78,
            "saturated_fat": 1.12,
            "sodium": 240.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Snack saludable", "Bajo en calorías", "Vegano", "Sin gluten", "Menos de 1€"],
        "health_verdict": "El kale pertenece a la familia de las crucíferas y contiene valiosos glucosinolatos y antioxidantes. Snack ideal saciante y bajo en hidratos.",
        "healthier_alternatives": ["Añadir a ensaladas para dar un toque crujiente sin sumar calorías."]
    },
    {
        "id": "book-boticaria-guacamole-zanahoria",
        "title": "Guacamole con Palitos de Zanahoria",
        "description": "Dip casero de aguacate fresco machacado con cebolleta, tomate y cilantro acompañado de bastoncillos de zanahoria cruda.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Zanahorias frescas", "amount": "200g (2 unidades)", "calories": 80, "protein": 1.8, "carbs": 18, "fat": 0.4},
            {"name": "Aguacates maduros", "amount": "300g (2 unidades)", "calories": 480, "protein": 6, "carbs": 25.5, "fat": 44.1},
            {"name": "Cebolleta", "amount": "50g (media)", "calories": 16, "protein": 0.6, "carbs": 3.7, "fat": 0.1},
            {"name": "Tomate maduro", "amount": "80g (1 unidad)", "calories": 14, "protein": 0.7, "carbs": 3.1, "fat": 0.2},
            {"name": "Zumo de limón o lima", "amount": "10ml", "calories": 3, "protein": 0.05, "carbs": 0.9, "fat": 0.03},
            {"name": "Cilantro fresco y sal", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.3, "fat": 0.05}
        ],
        "instructions": [
            "Lava la zanahoria, retira la piel con un pelador y corta bastones de 10 x 1 cm.",
            "Lava el tomate y córtalo en dados pequeños.",
            "Limpia y pica la cebolla fina junto a las hojas de cilantro.",
            "Extrae la pulpa del aguacate y machaca con un tenedor o prensador de patatas.",
            "Riega con el zumo de limón o lima.",
            "Vuelca el tomate, cebolla y cilantro sobre el puré de aguacate, sazona y mezcla bien."
        ],
        "per_serving": {
            "calories": 244.3,
            "protein": 3.22,
            "carbohydrates": 10.02,
            "fats": 21.26,
            "fiber": 9.8,
            "sugar": 7.90,
            "saturated_fat": 4.66,
            "sodium": 180.0,
            "vitamins_and_minerals": ["Vitamina E: 4.1mg", "Potasio: 780mg", "Folato: 95mcg"]
        },
        "total": {
            "calories": 488.6,
            "protein": 6.44,
            "carbohydrates": 20.04,
            "fats": 42.52,
            "fiber": 19.6,
            "sugar": 15.80,
            "saturated_fat": 9.32,
            "sodium": 360.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Grasas saludables", "Cardiosaludable", "Vegano", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Gran aporte de ácido oleico monoinsaturado, vitamina E y fibra. Sustituye nachos fritos por zanahoria reduciendo acrilamidas y sodio.",
        "healthier_alternatives": ["Completar con una tosta de pan integral y caballa en conserva para sumar proteína y Omega-3."]
    },
    {
        "id": "book-boticaria-zanahorias-encurtidas",
        "title": "Zanahorias Encurtidas 'Para Mañana'",
        "description": "Zanahorias laminadas encurtidas en frío con AOVE, vinagre, ajo, perejil y hierbabuena fresca. Snack refrescante y probiótico.",
        "servings": 2,
        "prep_time_minutes": 15,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Zanahorias", "amount": "200g", "calories": 80, "protein": 1.8, "carbs": 18, "fat": 0.4},
            {"name": "Perejil fresco", "amount": "10g", "calories": 4, "protein": 0.3, "carbs": 0.6, "fat": 0.1},
            {"name": "Dientes de ajo", "amount": "5g", "calories": 7, "protein": 0.3, "carbs": 1.6, "fat": 0.05},
            {"name": "Hierbabuena o menta fresca", "amount": "10g", "calories": 4, "protein": 0.3, "carbs": 0.8, "fat": 0.1},
            {"name": "Aceite de oliva virgen extra", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20},
            {"name": "Vinagre de manzana o vino", "amount": "30ml", "calories": 6, "protein": 0, "carbs": 0.3, "fat": 0},
            {"name": "Pimienta negra y sal", "amount": "Pizca", "calories": 2, "protein": 0.1, "carbs": 0.4, "fat": 0.05}
        ],
        "instructions": [
            "Corta las zanahorias en tiras longitudinales con una mandolina o pelador. Reserva.",
            "Pica el ajo fino, ponle sal y pimienta y deja reposar 15 minutos para que se mezclen los sabores.",
            "Pica las hierbas frescas y añádelas a las tiras de zanahoria.",
            "Mezcla el AOVE y el vinagre e intégralo con el ajo y las hierbas.",
            "Vierte el aliño sobre las zanahorias, mezcla bien y deja reposar 24 h en la nevera antes de consumir."
        ],
        "per_serving": {
            "calories": 131.51,
            "protein": 1.15,
            "carbohydrates": 9.07,
            "fats": 10.07,
            "fiber": 3.5,
            "sugar": 6.21,
            "saturated_fat": 1.54,
            "sodium": 140.0,
            "vitamins_and_minerals": ["Betacaroteno: 16000mcg", "Vitamina C: 35mg"]
        },
        "total": {
            "calories": 263.02,
            "protein": 2.30,
            "carbohydrates": 18.14,
            "fats": 20.14,
            "fiber": 7.0,
            "sugar": 12.42,
            "saturated_fat": 3.08,
            "sodium": 280.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Antioxidante", "Bajo en calorías", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Rico en betacarotenos protectores celulares y flavonoides del perejil. Excelente alternativa a aperitivos ultraprocesados salados.",
        "healthier_alternatives": ["Acompañar con queso fresco de cabra o tofu marinado para aportar proteína."]
    },
    {
        "id": "book-boticaria-patatitas-dos-salsas",
        "title": "Patatitas al Vapor con Dos Salsas de Yogur",
        "description": "Patatas baby cocinadas al microondas en 8 minutos con salsa de yogur a la hierbabuena y salsa de yogur al curry.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 8,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Patatas baby", "amount": "400g", "calories": 308, "protein": 8, "carbs": 68, "fat": 0.4},
            {"name": "Yogures griegos naturales", "amount": "250g (2 unidades)", "calories": 275, "protein": 12.5, "carbs": 10, "fat": 22.5},
            {"name": "Diente de ajo picado", "amount": "3g (medio diente)", "calories": 4, "protein": 0.2, "carbs": 0.9, "fat": 0.02},
            {"name": "Curry en polvo", "amount": "8g (1 cucharadita)", "calories": 26, "protein": 1, "carbs": 4.5, "fat": 1.1},
            {"name": "Hojas de hierbabuena fresca", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.3, "fat": 0.05},
            {"name": "AOVE, zumo de limón, pimienta y sal", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Lava las patatas baby, pínchalas con un tenedor y cocínalas al microondas con tapa durante 6-8 minutos a máxima potencia.",
            "En un bol, mezcla medio yogur griego con la hierbabuena picada, medio diente de ajo, un hilo de AOVE, zumo de limón y sal.",
            "En otro bol, mezcla el resto del yogur griego con el curry, pimienta negra y un hilo de AOVE.",
            "Sirve las patatas calientes acompañadas de las dos salsas frías."
        ],
        "per_serving": {
            "calories": 336.08,
            "protein": 10.86,
            "carbohydrates": 41.12,
            "fats": 14.24,
            "fiber": 4.8,
            "sugar": 8.19,
            "saturated_fat": 3.70,
            "sodium": 220.0,
            "vitamins_and_minerals": ["Potasio: 890mg", "Calcio: 180mg", "Vitamina B6: 0.6mg"]
        },
        "total": {
            "calories": 672.16,
            "protein": 21.72,
            "carbohydrates": 82.24,
            "fats": 28.48,
            "fiber": 9.6,
            "sugar": 16.38,
            "saturated_fat": 7.40,
            "sodium": 440.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Sin gluten", "Sustituto de patatas bravas", "Menos de 1€"],
        "health_verdict": "Sustituto brillante de las patatas fritas de bolsa o bravas con mayonesa. Al cocerse al microondas conservan el potasio sin generar acrilamidas.",
        "healthier_alternatives": ["Usar yogur griego 0% desnatado para recortar las grasas saturadas a la mitad."]
    },
    {
        "id": "book-boticaria-falso-sushi-pepino",
        "title": "Falso Sushi de Pepino, Yogur y Feta",
        "description": "Rollitos frescos de pepino rellenos de crema de yogur, queso feta, cebolla morada y pimiento amarillo en dados.",
        "servings": 2,
        "prep_time_minutes": 15,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pepino holandés", "amount": "270g (1 unidad)", "calories": 40.5, "protein": 1.9, "carbs": 9.7, "fat": 0.3},
            {"name": "Yogur griego natural", "amount": "125g (1 unidad)", "calories": 137.5, "protein": 6.25, "carbs": 5, "fat": 11.25},
            {"name": "Pimiento amarillo", "amount": "100g (medio)", "calories": 27, "protein": 1, "carbs": 6.3, "fat": 0.2},
            {"name": "Cebolla morada", "amount": "40g (media)", "calories": 16, "protein": 0.5, "carbs": 3.7, "fat": 0.1},
            {"name": "Queso feta", "amount": "50g", "calories": 132, "protein": 7.1, "carbs": 2, "fat": 10.7},
            {"name": "Diente de ajo, ralladura de limón y pimienta", "amount": "Al gusto", "calories": 5, "protein": 0.2, "carbs": 1, "fat": 0.05},
            {"name": "Aceite de oliva virgen extra", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Corta tiras finas longitudinales de pepino con una mandolina o pelador.",
            "Corta el pimiento amarillo y la cebolla morada en cuadraditos muy pequeños.",
            "Seca bien las tiras de pepino con papel absorbente de cocina.",
            "Prepara una crema batiendo el yogur griego, queso feta desmigado, el ajo picado fino, piel de limón y un chorrito de AOVE.",
            "Sobre cada tira de pepino pon una cucharada de la crema y un poco de pimiento y cebolla.",
            "Enrolla formando los bocaditos de falso sushi y sirve bien frío."
        ],
        "per_serving": {
            "calories": 185.78,
            "protein": 8.29,
            "carbohydrates": 10.66,
            "fats": 12.22,
            "fiber": 3.2,
            "sugar": 8.25,
            "saturated_fat": 5.51,
            "sodium": 310.0,
            "vitamins_and_minerals": ["Vitamina C: 85mg", "Calcio: 190mg", "Agua: 92%"]
        },
        "total": {
            "calories": 371.56,
            "protein": 16.58,
            "carbohydrates": 21.32,
            "fats": 24.44,
            "fiber": 6.4,
            "sugar": 16.50,
            "saturated_fat": 11.02,
            "sodium": 620.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Bajo en hidratos", "Keto friendly", "Vegetariano", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Plato muy hidratante y saciante gracias a la combinación de agua del pepino y la proteína de alto valor biológico del queso y yogur.",
        "healthier_alternatives": ["Añadir tiras de salmón ahumado o semillas de sésamo negro encima."]
    },
    {
        "id": "book-boticaria-gazpacho-sandia-feta",
        "title": "Gazpacho de Sandía y Queso Feta",
        "description": "Gazpacho refrescante elaborado con tomates pera, sandía dulce, albahaca escaldada y dados de queso feta.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Tomates pera maduros", "amount": "250g (3 unidades)", "calories": 45, "protein": 2.2, "carbs": 9.8, "fat": 0.5},
            {"name": "Sandía sin pepitas", "amount": "250g", "calories": 75, "protein": 1.5, "carbs": 18.8, "fat": 0.4},
            {"name": "Pimiento rojo", "amount": "150g (medio)", "calories": 39, "protein": 1.5, "carbs": 9, "fat": 0.3},
            {"name": "Cebolleta", "amount": "40g (media)", "calories": 16, "protein": 0.6, "carbs": 3.7, "fat": 0.1},
            {"name": "Queso feta", "amount": "50g", "calories": 132, "protein": 7.1, "carbs": 2, "fat": 10.7},
            {"name": "Diente de ajo y albahaca fresca escaldada", "amount": "5g", "calories": 7, "protein": 0.3, "carbs": 1.5, "fat": 0.05},
            {"name": "Aceite de oliva virgen extra y vinagre", "amount": "30ml", "calories": 270, "protein": 0, "carbs": 0, "fat": 30}
        ],
        "instructions": [
            "En el vaso de la batidora pon los tomates cortados en dos, la sandía sin corteza (reserva un poco para decorar), cebolleta y pimiento rojo.",
            "Escalda las hojas de albahaca unos segundos en agua hirviendo y añádelas.",
            "Añade 3 cucharadas de AOVE, 2 de vinagre y una pizca de sal.",
            "Tritura a máxima potencia hasta lograr una crema fina y homogénea.",
            "Sirve en copas o platos hondos decorado con trocitos de sandía y dados de queso feta."
        ],
        "per_serving": {
            "calories": 310.40,
            "protein": 8.39,
            "carbohydrates": 22.14,
            "fats": 20.92,
            "fiber": 4.2,
            "sugar": 17.43,
            "saturated_fat": 6.05,
            "sodium": 340.0,
            "vitamins_and_minerals": ["Licopeno: 14mg", "Vitamina C: 110mg", "Potasio: 620mg"]
        },
        "total": {
            "calories": 620.80,
            "protein": 16.78,
            "carbohydrates": 44.28,
            "fats": 41.84,
            "fiber": 8.4,
            "sugar": 34.86,
            "saturated_fat": 12.10,
            "sodium": 680.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Rico en licopeno", "Antioxidante", "Vegetariano", "Sin gluten", "Menos de 2€"],
        "health_verdict": "La combinación de triturar tomate con AOVE multiplica la absorción intestinal del licopeno, potente antioxidante cardiosaludable.",
        "healthier_alternatives": ["Sustituir el queso feta por queso de Burgos 0% para reducir grasas saturadas."]
    },
    {
        "id": "book-boticaria-carpaccio-remolacha",
        "title": "Carpaccio de Remolacha y Champiñón con Manchego",
        "description": "Finas láminas de remolacha cocida y champiñón crudo sobre cama de rúcula, lascas de queso manchego y vinagreta de avellanas.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Remolacha cocida y pelada", "amount": "250g (1 paquete)", "calories": 107.5, "protein": 4, "carbs": 24, "fat": 0.5},
            {"name": "Champiñones frescos limpios", "amount": "150g (10 unidades)", "calories": 33, "protein": 4.6, "carbs": 4.9, "fat": 0.5},
            {"name": "Rúcula fresca", "amount": "100g", "calories": 25, "protein": 2.6, "carbs": 3.6, "fat": 0.7},
            {"name": "Queso manchego curado en lascas", "amount": "30g", "calories": 140, "protein": 9.6, "carbs": 0.5, "fat": 11.5},
            {"name": "Avellanas tostadas picadas", "amount": "30g (10 unidades)", "calories": 195, "protein": 4.5, "carbs": 5, "fat": 18.2},
            {"name": "AOVE, vinagre de manzana y sal", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20}
        ],
        "instructions": [
            "Corta la remolacha en láminas muy finas con una mandolina o cuchillo afilado y disponla cubriendo la base del plato.",
            "Lava los champiñones, sécalos y córtalos en láminas finas colocándolos sobre la remolacha.",
            "Pon un puñado de rúcula fresca en el centro del plato y reparte las lascas de queso manchego.",
            "En un bote de cristal mezcla el AOVE, vinagre, las avellanas picadas y sal. Agita y vierte sobre el carpaccio."
        ],
        "per_serving": {
            "calories": 361.92,
            "protein": 11.04,
            "carbohydrates": 13.83,
            "fats": 29.16,
            "fiber": 5.8,
            "sugar": 11.37,
            "saturated_fat": 6.31,
            "sodium": 280.0,
            "vitamins_and_minerals": ["Folatos: 110mcg", "Vitamina K: 70mcg", "Calcio: 210mg"]
        },
        "total": {
            "calories": 723.84,
            "protein": 22.08,
            "carbohydrates": 27.66,
            "fats": 58.32,
            "fiber": 11.6,
            "sugar": 22.74,
            "saturated_fat": 12.62,
            "sodium": 560.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Vegetariano", "Gourmet rápido", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Plato rico en nitratos inorgánicos que favorecen la vasodilatación y el rendimiento cardiovascular. El queso manchego aporta calcio de alta biodisponibilidad.",
        "healthier_alternatives": ["Reducir el queso a 15g por persona si se busca menor contenido en grasas saturadas."]
    },
    {
        "id": "book-boticaria-dip-guisantes-totopos",
        "title": "Dip de Guisantes con Hierbabuena y Totopos Caseros",
        "description": "Puré templado de guisantes tiernos con queso fresco, pistachos y hierbabuena servido con totopos de trigo integral horneados.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Guisantes ultracongelados", "amount": "300g", "calories": 243, "protein": 16.2, "carbs": 43.2, "fat": 1.2},
            {"name": "Queso fresco de Burgos", "amount": "250g", "calories": 250, "protein": 25, "carbs": 7.5, "fat": 13.5},
            {"name": "Tortillas de trigo integral", "amount": "50g (1 tortilla)", "calories": 150, "protein": 4.5, "carbs": 26, "fat": 3},
            {"name": "Pistachos pelados tostados", "amount": "15g", "calories": 85, "protein": 3, "carbs": 4.2, "fat": 6.8},
            {"name": "1/2 diente de ajo picado", "amount": "3g", "calories": 4, "protein": 0.2, "carbs": 0.9, "fat": 0.02},
            {"name": "Hierbabuena, pimentón dulce, AOVE y sal", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Precalienta el horno a 180°C. Corta la tortilla de trigo en 8 triángulos, ponlos sobre papel vegetal, pincela con AOVE y hornea 10 minutos.",
            "Coloca los guisantes con 2 cucharadas de agua en un bol apto para microondas y cocina 4 minutos a máxima potencia.",
            "Tritura los guisantes templados con un tenedor.",
            "Mezcla el queso fresco con el ajo picado, pistachos picados, hojas de hierbabuena, sal, pimienta y el puré de guisantes.",
            "Espolvorea los totopos crujientes con pimentón y sirve junto al dip."
        ],
        "per_serving": {
            "calories": 366.0,
            "protein": 19.65,
            "carbohydrates": 21.45,
            "fats": 22.40,
            "fiber": 8.1,
            "sugar": 11.35,
            "saturated_fat": 9.73,
            "sodium": 290.0,
            "vitamins_and_minerals": ["Vitamina C: 40mg", "Hierro: 3.2mg", "Fósforo: 290mg"]
        },
        "total": {
            "calories": 732.0,
            "protein": 39.30,
            "carbohydrates": 42.90,
            "fats": 44.80,
            "fiber": 16.2,
            "sugar": 22.70,
            "saturated_fat": 19.46,
            "sodium": 580.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína vegetal", "Rico en fibra", "Vegetariano", "Menos de 3€"],
        "health_verdict": "Los guisantes ultracongelados conservan el 95% de sus vitaminas originales. Plato excelente en fibra fermentable y proteína saciante.",
        "healthier_alternatives": ["Sustituir el queso fresco tradicional por queso fresco batido 0% para recortar grasas."]
    },
    {
        "id": "book-boticaria-escarola-granada",
        "title": "Ensalada de Escarola con Granada y Aliño de Comino",
        "description": "Ensalada tradicional de invierno con escarola rizada, granada fresca crujiente y majado de comino tostado y ajo.",
        "servings": 2,
        "prep_time_minutes": 8,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Escarola fresca limpia", "amount": "300g", "calories": 54, "protein": 4.5, "carbs": 9, "fat": 0.6},
            {"name": "Granada fresca (granos)", "amount": "275g (1 pieza)", "calories": 228, "protein": 4.6, "carbs": 51.4, "fat": 3.3},
            {"name": "Diente de ajo", "amount": "8g (1 unidad)", "calories": 11, "protein": 0.5, "carbs": 2.6, "fat": 0.05},
            {"name": "Comino en grano tostado", "amount": "1 cucharadita", "calories": 8, "protein": 0.4, "carbs": 0.9, "fat": 0.4},
            {"name": "AOVE, vinagre de Jerez y sal", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Para desgranar la granada, corta la pieza por la mitad y golpea la piel con una cuchara o mortero sobre un bol.",
            "Lava, escurre y trocea la escarola en trozos medianos.",
            "En una sartén pequeña tuesta los granos de comino 1 minuto cuidando que no se quemen. Tritúralos en el mortero con el ajo y una pizca de sal.",
            "Añade vinagre y AOVE al mortero y mezcla.",
            "Vuelca el aliño y los granos de granada sobre la escarola y sirve de inmediato."
        ],
        "per_serving": {
            "calories": 181.99,
            "protein": 4.63,
            "carbohydrates": 24.51,
            "fats": 7.27,
            "fiber": 7.5,
            "sugar": 20.51,
            "saturated_fat": 0.93,
            "sodium": 110.0,
            "vitamins_and_minerals": ["Antocianinas: 45mg", "Folato: 140mcg", "Vitamina C: 30mg"]
        },
        "total": {
            "calories": 363.98,
            "protein": 9.26,
            "carbohydrates": 49.02,
            "fats": 14.54,
            "fiber": 15.0,
            "sugar": 41.02,
            "saturated_fat": 1.86,
            "sodium": 220.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Antioxidante", "Bajo en grasa", "Sin gluten", "Menos de 1€"],
        "health_verdict": "La granada es una de las mayores fuentes de punicalaginas y polifenoles. Combate la inflamación y aporta fibra saciante.",
        "healthier_alternatives": ["Añadir dados de queso de cabra o nueces picadas para convertirlo en plato principal."]
    },
    {
        "id": "book-boticaria-tosta-aguacate-requeson",
        "title": "Tosta de Aguacate con Requesón y Cherry",
        "description": "Desayuno o cena exprés sobre pan 100% integral con requesón artesano, láminas de aguacate y tomates cherry.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Requesón bajo en sal", "amount": "125g (1 tarrina)", "calories": 125, "protein": 15, "carbs": 3.7, "fat": 5.6},
            {"name": "Aguacate maduro", "amount": "150g (1 unidad)", "calories": 240, "protein": 3, "carbs": 12.7, "fat": 22},
            {"name": "Tomates cherry", "amount": "80g", "calories": 14, "protein": 0.7, "carbs": 3.1, "fat": 0.2},
            {"name": "Pan 100% integral", "amount": "90g (2 rebanadas)", "calories": 216, "protein": 8.1, "carbs": 39.6, "fat": 2.2},
            {"name": "AOVE y sal", "amount": "5ml", "calories": 45, "protein": 0, "carbs": 0, "fat": 5}
        ],
        "instructions": [
            "Tuesta las rebanadas de pan integral en tostadora o sartén antiadherente.",
            "Corta el aguacate en láminas finas y los tomates cherry por la mitad.",
            "Extiende el requesón sobre cada una de las rebanadas tostadas.",
            "Coloca el tomate y el aguacate sobre el requesón.",
            "Añade una pizca de sal marina y un hilo ligero de AOVE."
        ],
        "per_serving": {
            "calories": 350.61,
            "protein": 11.52,
            "carbohydrates": 30.30,
            "fats": 20.37,
            "fiber": 7.2,
            "sugar": 3.75,
            "saturated_fat": 7.79,
            "sodium": 240.0,
            "vitamins_and_minerals": ["Calcio: 230mg", "Vitamina E: 3.5mg", "Magnesio: 68mg"]
        },
        "total": {
            "calories": 701.22,
            "protein": 23.04,
            "carbohydrates": 60.60,
            "fats": 40.74,
            "fiber": 14.4,
            "sugar": 7.50,
            "saturated_fat": 15.58,
            "sodium": 480.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Rico en fibra", "Desayuno saludable", "Menos de 2€"],
        "health_verdict": "El requesón ofrece proteínas de suero lácteo de altísimo valor biológico con menor contenido en sodio que los quesos curados.",
        "healthier_alternatives": ["Añadir pistachos triturados y semillas de chía para sumar Omega-3 vegetal."]
    },
    {
        "id": "book-boticaria-barquitas-berenjena",
        "title": "Barquitas de Berenjena con Yogur y Manzana Verde",
        "description": "Berenjenas asadas al microondas en 10 minutos rellenas de su propia pulpa aliñada con yogur, cebolla marinada y manzana ácida.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Berenjena fresca", "amount": "300g (1 pieza)", "calories": 75, "protein": 3, "carbs": 18, "fat": 0.6},
            {"name": "Yogur natural entero", "amount": "125g (1 unidad)", "calories": 76, "protein": 4.4, "carbs": 5.9, "fat": 4.1},
            {"name": "Cebolla roja", "amount": "80g (1 unidad)", "calories": 32, "protein": 0.9, "carbs": 7.4, "fat": 0.1},
            {"name": "Manzana verde ácida (Granny Smith)", "amount": "200g (1 unidad)", "calories": 104, "protein": 0.6, "carbs": 27.6, "fat": 0.3},
            {"name": "Diente de ajo", "amount": "8g (1 unidad)", "calories": 11, "protein": 0.5, "carbs": 2.6, "fat": 0.05},
            {"name": "Zumo de limón", "amount": "80ml", "calories": 20, "protein": 0.4, "carbs": 6.8, "fat": 0.2},
            {"name": "AOVE, pimienta y sal", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Pica la cebolla fina y ponla a marinar en el zumo de limón durante 10 minutos.",
            "Corta la berenjena en dos mitades y ásala en un estuche de vapor o recipiente tapado al microondas durante 10 minutos a máxima potencia.",
            "Deja templar, extrae la carne con una cuchara y reserva la piel intacta.",
            "Pica el ajo y media manzana y mezcla con la carne de la berenjena, el yogur y la cebolla marinada escurrida.",
            "Rellena la piel de la berenjena con la mezcla y decora con la otra media manzana cortada en gajos finos."
        ],
        "per_serving": {
            "calories": 191.88,
            "protein": 6.02,
            "carbohydrates": 25.66,
            "fats": 7.24,
            "fiber": 8.5,
            "sugar": 18.07,
            "saturated_fat": 1.84,
            "sodium": 180.0,
            "vitamins_and_minerals": ["Antocianinas: 35mg", "Vitamina C: 45mg", "Potasio: 580mg"]
        },
        "total": {
            "calories": 383.76,
            "protein": 12.04,
            "carbohydrates": 51.32,
            "fats": 14.48,
            "fiber": 17.0,
            "sugar": 36.14,
            "saturated_fat": 3.68,
            "sodium": 360.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Bajo en calorías", "Rico en fibra", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Cocinar la berenjena al microondas evita que absorba la enorme cantidad de aceite habitual de las frituras tradicionales.",
        "healthier_alternatives": ["Añadir dados de pechuga de pavo braseada o atún para sumar 20g de proteína magra."]
    },
    {
        "id": "book-boticaria-escabeche-sardinas",
        "title": "Escabeche Casero Exprés de Sardinas",
        "description": "Sardinas frescas cocinadas en sartén en suave escabeche tradicional con AOVE, vinagre, laurel y pimentón. Ricas en Omega-3.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 15,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Sardinas frescas limpias sin cabezas ni vísceras", "amount": "500g (6-9 piezas)", "calories": 675, "protein": 90, "carbs": 0, "fat": 35},
            {"name": "Aceite de oliva virgen extra", "amount": "60ml", "calories": 540, "protein": 0, "carbs": 0, "fat": 60},
            {"name": "Vinagre de vino blanco o manzana", "amount": "30ml", "calories": 6, "protein": 0, "carbs": 0.3, "fat": 0},
            {"name": "Diente de ajo aplastado", "amount": "8g", "calories": 11, "protein": 0.5, "carbs": 2.6, "fat": 0.05},
            {"name": "Pimentón dulce de la Vera", "amount": "6g", "calories": 18, "protein": 0.8, "carbs": 3.2, "fat": 0.6},
            {"name": "Hoja de laurel, pimienta en grano y sal", "amount": "Al gusto", "calories": 3, "protein": 0.1, "carbs": 0.6, "fat": 0.05}
        ],
        "instructions": [
            "Pide en la pescadería que te limpien las sardinas retirando cabezas, vísceras y escamas.",
            "En una sartén con dos cucharadas de AOVE dora el diente de ajo aplastado con piel.",
            "Añade el pimentón con cuidado para que no se queme, el resto del aceite y el vinagre, cociendo 5 minutos.",
            "Añade el laurel, los granos de pimienta y las sardinas limpias. Cuece 10 minutos a fuego suave.",
            "Deja enfriar y consume templado o al día siguiente (el sabor se intensifica)."
        ],
        "per_serving": {
            "calories": 542.33,
            "protein": 30.59,
            "carbohydrates": 4.08,
            "fats": 44.85,
            "fiber": 0.8,
            "sugar": 0.90,
            "saturated_fat": 8.31,
            "sodium": 320.0,
            "vitamins_and_minerals": ["Omega-3 (EPA/DHA): 2.8g", "Vitamina D: 12mcg", "Vitamina B12: 8.5mcg"]
        },
        "total": {
            "calories": 1084.66,
            "protein": 61.18,
            "carbohydrates": 8.16,
            "fats": 89.70,
            "fiber": 1.6,
            "sugar": 1.80,
            "saturated_fat": 16.62,
            "sodium": 640.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Rico en Omega-3", "Cardiosaludable", "Keto friendly", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Pescado azul de tamaño pequeño libre de metales pesados (mercurio). Aporte excepcional de ácidos grasos EPA/DHA y vitamina D.",
        "healthier_alternatives": ["Acompañar con ensalada verde o patata cocida para equilibrar el aporte calórico del escabeche."]
    },
    {
        "id": "book-boticaria-crema-calabaza-queso-azul",
        "title": "Crema de Calabaza con Queso Azul y Pipas",
        "description": "Crema sedosa de calabaza cacahuete y puerro al pimentón coronada con dados de queso azul fundente y semillas tostadas.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Calabaza cacahuete en dados", "amount": "500g", "calories": 130, "protein": 5, "carbs": 32.5, "fat": 0.5},
            {"name": "Puerro en rodajas", "amount": "80g", "calories": 48, "protein": 1.2, "carbs": 11.2, "fat": 0.2},
            {"name": "Queso azul en dados", "amount": "80g", "calories": 280, "protein": 16.8, "carbs": 1.8, "fat": 23.2},
            {"name": "Semillas de calabaza", "amount": "10g", "calories": 55, "protein": 3, "carbs": 1.5, "fat": 4.6},
            {"name": "Caldo de verduras o agua", "amount": "250ml", "calories": 15, "protein": 0.5, "carbs": 3, "fat": 0.2},
            {"name": "Pimentón dulce", "amount": "10g", "calories": 30, "protein": 1.4, "carbs": 5.4, "fat": 1.3},
            {"name": "Aceite de oliva virgen extra y sal", "amount": "30ml", "calories": 270, "protein": 0, "carbs": 0, "fat": 30}
        ],
        "instructions": [
            "Pela la calabaza y córtala en dados. Limpia el puerro y córtalo en rodajas.",
            "Calienta el AOVE en una olla, añade el puerro y saltea con cuidado.",
            "Separa la olla del fuego, añade el pimentón, remueve y vuelve a poner al fuego.",
            "Añade la calabaza, vierte el caldo de verduras y sal y cuece 10 minutos a fuego medio.",
            "En los platos hondos pon los dados de queso azul.",
            "Tritura la crema con batidora hasta textura muy fina y viértela sobre el queso. Decora con las semillas de calabaza."
        ],
        "per_serving": {
            "calories": 375.74,
            "protein": 14.04,
            "carbohydrates": 12.62,
            "fats": 29.90,
            "fiber": 5.2,
            "sugar": 5.46,
            "saturated_fat": 10.25,
            "sodium": 420.0,
            "vitamins_and_minerals": ["Betacarotenos: 4500mcg", "Calcio: 310mg", "Zinc: 2.8mg"]
        },
        "total": {
            "calories": 751.48,
            "protein": 28.08,
            "carbohydrates": 25.24,
            "fats": 59.80,
            "fiber": 10.4,
            "sugar": 10.92,
            "saturated_fat": 20.50,
            "sodium": 840.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Vegetariano", "Confort food", "Rico en antioxidantes", "Sin gluten", "Menos de 2€"],
        "health_verdict": "La calabaza aporta vitamina A y carotenoides con muy baja densidad calórica, combinada con el contraste proteico del queso azul.",
        "healthier_alternatives": ["Reducir el queso azul a 40g (20g por ración) o usar queso fresco de cabra para aligerar la grasa saturada."]
    },
    {
        "id": "book-boticaria-alubia-confetti",
        "title": "Alubia Confetti con Arroz Integral y Maíz",
        "description": "Ensalada completa vegetal y colorida con alubias rojas, arroz integral de vasito, maíz tierno, pimiento y cilantro.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1547496502-affa22d38842?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Alubias rojas cocidas en conserva", "amount": "400g (1 bote)", "calories": 360, "protein": 24, "carbs": 60, "fat": 2},
            {"name": "Arroz integral precocido", "amount": "125g (1 vasito)", "calories": 160, "protein": 3.5, "carbs": 33, "fat": 1.2},
            {"name": "Maíz dulce en conserva", "amount": "140g (1 lata pequeña)", "calories": 112, "protein": 3.6, "carbs": 24, "fat": 1.4},
            {"name": "Pimiento rojo en dados", "amount": "150g (medio)", "calories": 39, "protein": 1.5, "carbs": 9, "fat": 0.3},
            {"name": "Tallos verdes de cebolleta", "amount": "30g", "calories": 10, "protein": 0.5, "carbs": 2.2, "fat": 0.1},
            {"name": "Zumo de limón", "amount": "20ml", "calories": 5, "protein": 0.1, "carbs": 1.5, "fat": 0.05},
            {"name": "AOVE, cilantro fresco y sal", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20}
        ],
        "instructions": [
            "Corta los tallos de cebolleta en aros y déjalos macerar con el zumo de medio limón.",
            "Cocina el arroz en el microondas según las instrucciones (1 min) y deja enfriar.",
            "Escurre las alubias rojas y el maíz y viértelos en un bol.",
            "Añade el pimiento rojo cortado en dados, el arroz integral y los tallos de cebolleta macerados.",
            "Aliña con el AOVE y sal, pica el cilantro fresco y mezcla todo bien."
        ],
        "per_serving": {
            "calories": 403.95,
            "protein": 18.15,
            "carbohydrates": 59.82,
            "fats": 10.23,
            "fiber": 13.5,
            "sugar": 7.60,
            "saturated_fat": 1.76,
            "sodium": 310.0,
            "vitamins_and_minerals": ["Hierro: 5.4mg", "Magnesio: 115mg", "Vitamina C: 95mg"]
        },
        "total": {
            "calories": 807.90,
            "protein": 36.30,
            "carbohydrates": 119.64,
            "fats": 20.46,
            "fiber": 27.0,
            "sugar": 15.20,
            "saturated_fat": 3.52,
            "sodium": 620.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Proteína completa vegetal", "Alto en fibra", "Sin gluten", "Menos de 1€"],
        "health_verdict": "La combinación de legumbre (alubia) con cereal integral (arroz) aporta todos los aminoácidos esenciales, con más de 13g de fibra por ración.",
        "healthier_alternatives": ["Añadir aguacate o huevo cocido para elevar el contenido en ácidos grasos monoinsaturados."]
    },
    {
        "id": "book-boticaria-salmon-expres-micro",
        "title": "Salmón Exprés al Microondas con Basmati y Pepino",
        "description": "Lomos de salmón jugosos cocinados en 5 minutos al microondas acompañados de arroz basmati y ensalada japonesa de pepino y sésamo.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Lomos de salmón fresco", "amount": "400g (2 porciones)", "calories": 760, "protein": 80, "carbs": 0, "fat": 48},
            {"name": "Arroz basmati precocido", "amount": "125g (1 vasito)", "calories": 160, "protein": 3.5, "carbs": 33, "fat": 1.2},
            {"name": "Pepino", "amount": "300g (1 unidad)", "calories": 45, "protein": 2.1, "carbs": 10.8, "fat": 0.3},
            {"name": "Cebolleta", "amount": "50g", "calories": 16, "protein": 0.6, "carbs": 3.7, "fat": 0.1},
            {"name": "Salsa de soja baja en sal", "amount": "15ml (1 cucharada)", "calories": 12, "protein": 1.2, "carbs": 1.5, "fat": 0.1},
            {"name": "Semillas de sésamo y jengibre rallado", "amount": "1 cucharadita", "calories": 30, "protein": 1, "carbs": 1.2, "fat": 2.5},
            {"name": "Eneldo seco, vinagre y AOVE", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10}
        ],
        "instructions": [
            "Corta el pepino en tiras con mandolina, sala y deja escurrir. Pica la cebolleta.",
            "Cocina el arroz basmati en microondas según instrucciones del fabricante (1 min).",
            "Unta el salmón con AOVE, sazona y espolvorea con eneldo. Coloca en plato apto tapado y cocina 5 minutos a potencia máxima.",
            "Mezcla el pepino escurrido con la cebolleta, soja, vinagre, jengibre y sésamo.",
            "Sirve el salmón caliente con el arroz basmati y la ensalada de pepino."
        ],
        "per_serving": {
            "calories": 561.81,
            "protein": 44.90,
            "carbohydrates": 24.25,
            "fats": 31.69,
            "fiber": 3.5,
            "sugar": 3.73,
            "saturated_fat": 5.36,
            "sodium": 460.0,
            "vitamins_and_minerals": ["Omega-3: 3.2g", "Vitamina D: 16mcg", "Vitamina B12: 5.6mcg"]
        },
        "total": {
            "calories": 1123.62,
            "protein": 89.80,
            "carbohydrates": 48.50,
            "fats": 63.38,
            "fiber": 7.0,
            "sugar": 7.46,
            "saturated_fat": 10.72,
            "sodium": 920.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alto en proteína", "Rico en Omega-3", "Sin gluten", "Menos de 3€"],
        "health_verdict": "Aporte descomunal de casi 45g de proteína magra y ácidos grasos Omega-3 de cadena larga (DHA y EPA) en tan solo 10 minutos de preparación.",
        "healthier_alternatives": ["Sustituir el arroz basmati por arroz de coliflor para reducir hidratos de carbono."]
    },
    {
        "id": "book-boticaria-tallarines-calabacin-nueces",
        "title": "Tallarines de Calabacín y Zanahoria con Vinagreta de Nueces",
        "description": "Falsos tallarines espiralizados de verduras salteados al dente con vinagreta de mostaza de Dijon, sésamo y nueces crujientes.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Calabacín fresco", "amount": "200g (1 unidad)", "calories": 34, "protein": 2.4, "carbs": 6.2, "fat": 0.6},
            {"name": "Zanahorias frescas", "amount": "200g (2 unidades)", "calories": 80, "protein": 1.8, "carbs": 18, "fat": 0.4},
            {"name": "Diente de ajo picado", "amount": "5g", "calories": 7, "protein": 0.3, "carbs": 1.6, "fat": 0.05},
            {"name": "Nueces peladas troceadas", "amount": "25g (2-3 nueces)", "calories": 165, "protein": 3.8, "carbs": 3.4, "fat": 16.3},
            {"name": "Semillas de sésamo", "amount": "12g", "calories": 68, "protein": 2.2, "carbs": 2.8, "fat": 5.9},
            {"name": "Mostaza de Dijon", "amount": "3g", "calories": 4, "protein": 0.2, "carbs": 0.2, "fat": 0.3},
            {"name": "AOVE, vinagre y sal", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20}
        ],
        "instructions": [
            "Lava el calabacín y las zanahorias y forma los tallarines vegetales con un espiralizador o pelador dentado.",
            "Saltéalos a fuego vivo en sartén antiadherente con un hilo de AOVE y el ajo picado durante 3 minutos (deben quedar al dente).",
            "Prepara la vinagreta mezclando el resto de AOVE con el vinagre y la mostaza de Dijon.",
            "Mezcla en un bol los tallarines salteados con la vinagreta.",
            "Espolvorea con las nueces picadas y las semillas de sésamo por encima antes de servir."
        ],
        "per_serving": {
            "calories": 222.14,
            "protein": 4.76,
            "carbohydrates": 10.77,
            "fats": 17.78,
            "fiber": 4.9,
            "sugar": 6.94,
            "saturated_fat": 2.41,
            "sodium": 140.0,
            "vitamins_and_minerals": ["Vitamina A: 1200mcg", "Omega-3 vegetal (ALA): 1.4g", "Magnesio: 45mg"]
        },
        "total": {
            "calories": 444.28,
            "protein": 9.52,
            "carbohydrates": 21.54,
            "fats": 35.56,
            "fiber": 9.8,
            "sugar": 13.88,
            "saturated_fat": 4.82,
            "sodium": 280.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Bajo en carbohidratos", "Keto friendly", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Plato de mínimo índice glucémico con gran aporte de fibra y grasas poliinsaturadas cardiosaludables de las nueces.",
        "healthier_alternatives": ["Añadir gambas salteadas o dados de tofu para sumarle 20g de proteína."]
    },
    {
        "id": "book-boticaria-brocheta-pollo-especiado",
        "title": "Brocheta de Pollo Especiado con Nectarina y Rúcula",
        "description": "Brochetas jugosas a la plancha de pechuga marinada en pimentón y limón intercalada con nectarina fresca y ensalada de rúcula con nueces.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pechuga de pollo limpia", "amount": "300g (media pechuga)", "calories": 360, "protein": 66, "carbs": 0, "fat": 7.5},
            {"name": "Nectarina o melocotón", "amount": "150g (1 unidad)", "calories": 66, "protein": 1.5, "carbs": 15, "fat": 0.4},
            {"name": "Pimiento verde", "amount": "100g (1 unidad)", "calories": 20, "protein": 0.9, "carbs": 4.6, "fat": 0.2},
            {"name": "Cebolla", "amount": "40g", "calories": 16, "protein": 0.5, "carbs": 3.7, "fat": 0.1},
            {"name": "Tomates cherry", "amount": "60g", "calories": 11, "protein": 0.5, "carbs": 2.4, "fat": 0.1},
            {"name": "Rúcula y nueces", "amount": "125g", "calories": 190, "protein": 6, "carbs": 6, "fat": 17},
            {"name": "Pimentón dulce, limón, pimienta, AOVE (10ml) y sal", "amount": "Al gusto", "calories": 95, "protein": 0.5, "carbs": 2, "fat": 10}
        ],
        "instructions": [
            "Corta la pechuga en dados, salpimenta y pon en un bol con cebolla rallada, pimentón, zumo de limón y AOVE. Deja marinar 5 min.",
            "Lava y corta el pimiento verde y la nectarina en dados de tamaño similar.",
            "Ensarta en las brochetas alternando el pollo marinado, la nectarina, pimiento y tomates cherry.",
            "Cocina las brochetas en una plancha o sartén bien caliente con unas gotas de AOVE hasta dorar por todos los lados.",
            "Sirve con una ensalada de rúcula y nueces aliñada con AOVE, limón y sal."
        ],
        "per_serving": {
            "calories": 316.08,
            "protein": 38.69,
            "carbohydrates": 12.34,
            "fats": 12.44,
            "fiber": 4.5,
            "sugar": 9.62,
            "saturated_fat": 2.15,
            "sodium": 260.0,
            "vitamins_and_minerals": ["Vitamina C: 75mg", "Niacina: 12mg", "Hierro: 2.8mg"]
        },
        "total": {
            "calories": 632.16,
            "protein": 77.38,
            "carbohydrates": 24.68,
            "fats": 24.88,
            "fiber": 9.0,
            "sugar": 19.24,
            "saturated_fat": 4.30,
            "sodium": 520.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína", "Baja en grasas", "Fitness friendly", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Casi 40g de proteína magra con apenas 300 kcal por ración. El toque de fruta aporta antioxidantes y jugosidad natural sin salsas comerciales.",
        "healthier_alternatives": ["Opción veggie: sustituir el pollo por dados de tofu firme marinado o champiñones Portobello."]
    },
    {
        "id": "book-boticaria-miniburger-alubias-atun",
        "title": "Miniburger de Alubias Blancas y Atún",
        "description": "Hamburguesas caseras rápidas elaboradas con alubias aplastadas, atún en conserva, huevo y mostaza de Dijon sobre cama de brotes.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Alubias blancas cocidas", "amount": "240g (bote pequeño)", "calories": 216, "protein": 14.4, "carbs": 36, "fat": 1.2},
            {"name": "Atún en conserva al natural o AOVE", "amount": "185g (1 lata grande)", "calories": 240, "protein": 48, "carbs": 0, "fat": 4},
            {"name": "Huevo entero", "amount": "60g (1 unidad)", "calories": 75, "protein": 6.5, "carbs": 0.5, "fat": 5.2},
            {"name": "Pan rallado integral", "amount": "30g", "calories": 105, "protein": 3.6, "carbs": 21, "fat": 0.9},
            {"name": "Hojas verdes variadas y cherry", "amount": "200g", "calories": 40, "protein": 2.5, "carbs": 7, "fat": 0.5},
            {"name": "Mostaza de Dijon, orégano, ralladura de limón, AOVE (5ml) y sal", "amount": "Al gusto", "calories": 55, "protein": 1.5, "carbs": 2.5, "fat": 5}
        ],
        "instructions": [
            "Escurre las alubias y aplástalas con un tenedor hasta formar una pasta.",
            "Incorpora el atún bien escurrido, el huevo entero y el pan rallado.",
            "Aliña con una cucharada de mostaza de Dijon, orégano, ralladura de limón y sal marina.",
            "Con la masa resultante forma 4 mini hamburguesas.",
            "Márcalas en una sartén antiadherente con unas gotas de AOVE 2-3 minutos por lado hasta dorar.",
            "Sirve con las hojas verdes y tomates cherry aliñados con AOVE y limón."
        ],
        "per_serving": {
            "calories": 402.38,
            "protein": 38.61,
            "carbohydrates": 24.59,
            "fats": 16.62,
            "fiber": 9.2,
            "sugar": 3.53,
            "saturated_fat": 2.90,
            "sodium": 380.0,
            "vitamins_and_minerals": ["Hierro: 4.6mg", "Fósforo: 380mg", "Selenio: 55mcg"]
        },
        "total": {
            "calories": 804.76,
            "protein": 77.22,
            "carbohydrates": 49.18,
            "fats": 33.24,
            "fiber": 18.4,
            "sugar": 7.06,
            "saturated_fat": 5.80,
            "sodium": 760.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína", "Rico en fibra", "Sustituto de fast food", "Menos de 2€"],
        "health_verdict": "Aporta casi 40g de proteína combinando legumbre y pescado azul. Contiene solo 2.9g de grasas saturadas frente a los 15-20g de una hamburguesa industrial.",
        "healthier_alternatives": ["Servir en panecillo 100% integral con rodajas de tomate y aguacate."]
    },
    {
        "id": "book-boticaria-mini-green-pizza",
        "title": "Mini Green Pizza en Pan de Pita",
        "description": "Base de pita integral con pesto casero de rúcula y nueces, ramilletes de brócoli al vapor y mozzarella fresca fundida al grill.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 7,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pitas 100% integrales", "amount": "180g (2 unidades)", "calories": 432, "protein": 16, "carbs": 80, "fat": 3.6},
            {"name": "Brócoli en ramilletes", "amount": "150g", "calories": 51, "protein": 4.2, "carbs": 10.2, "fat": 0.6},
            {"name": "Mozzarella fresca", "amount": "100g", "calories": 250, "protein": 18, "carbs": 2, "fat": 19},
            {"name": "Rúcula fresca", "amount": "100g", "calories": 25, "protein": 2.6, "carbs": 3.6, "fat": 0.7},
            {"name": "Nueces peladas crudas", "amount": "25g", "calories": 165, "protein": 3.8, "carbs": 3.4, "fat": 16.3},
            {"name": "Queso parmesano rallado", "amount": "30g", "calories": 120, "protein": 10.5, "carbs": 1, "fat": 8.5},
            {"name": "Medio ajo, AOVE (15ml), pimienta y sal", "amount": "Al gusto", "calories": 140, "protein": 0.3, "carbs": 1, "fat": 15}
        ],
        "instructions": [
            "Corta las pitas transversalmente para abrir las bases.",
            "Lava el brócoli, córtalo en ramilletes y cocínalo al microondas tapado durante 4 minutos.",
            "En batidora prepara el pesto triturando la rúcula, ajo, parmesano, nueces, AOVE y sal.",
            "Coloca sobre cada media pita rodajas de mozzarella, los ramilletes de brócoli y cubre con el pesto.",
            "Gratina en el horno en modo grill (o microondas con grill) durante 3 minutos hasta que el queso se funda."
        ],
        "per_serving": {
            "calories": 408.48,
            "protein": 17.48,
            "carbohydrates": 5.53,
            "fats": 35.16,
            "fiber": 5.4,
            "sugar": 1.88,
            "saturated_fat": 13.31,
            "sodium": 420.0,
            "vitamins_and_minerals": ["Calcio: 380mg", "Vitamina C: 70mg", "Omega-3 (ALA): 1.3g"]
        },
        "total": {
            "calories": 816.96,
            "protein": 34.96,
            "carbohydrates": 11.06,
            "fats": 70.32,
            "fiber": 10.8,
            "sugar": 3.76,
            "saturated_fat": 26.62,
            "sodium": 840.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Vegetariano", "Sustituto de pizza delivery", "Rico en antioxidantes", "Menos de 2€"],
        "health_verdict": "Sustituto idóneo de pizzas ultraprocesadas. Al cocinar el brócoli al vapor o microondas conserva el 85% del sulforafano anticanceroso.",
        "healthier_alternatives": ["Sustituir la mozzarella por mozzarella light para reducir grasas saturadas."]
    },
    {
        "id": "book-boticaria-ensalada-frutos-rojos-setas",
        "title": "Ensalada de Frutos Rojos, Setas y Cuscús con Rulo de Cabra",
        "description": "Cuscús integral con setas ostra salteadas al ajo, queso rulo de cabra dorado y frutos rojos antioxidantes.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Cuscús integral", "amount": "50g", "calories": 180, "protein": 6.5, "carbs": 36, "fat": 1},
            {"name": "Brotes de lechuga", "amount": "150g", "calories": 25, "protein": 2, "carbs": 3.5, "fat": 0.4},
            {"name": "Queso rulo de cabra", "amount": "100g", "calories": 290, "protein": 18, "carbs": 1.5, "fat": 24},
            {"name": "Setas ostra frescas", "amount": "200g", "calories": 66, "protein": 6.6, "carbs": 13, "fat": 0.8},
            {"name": "Frutos rojos (fresas, arándanos, moras)", "amount": "200g", "calories": 80, "protein": 1.6, "carbs": 18, "fat": 0.6},
            {"name": "Diente de ajo, cebollino, AOVE (15ml), vinagre y sal", "amount": "Al gusto", "calories": 140, "protein": 0.4, "carbs": 1.5, "fat": 15}
        ],
        "instructions": [
            "Hidrata el cuscús integral con agua hirviendo según el fabricante (5 minutos).",
            "Limpia las setas, córtalas en tiras y saltéalas en sartén con medio ajo picado y AOVE.",
            "Tuesta ligeramente en la sartén las rodajas de queso rulo de cabra.",
            "Monta el plato con base de lechuga y cuscús, coloca las setas, el queso templado y los frutos rojos.",
            "Aliña con AOVE y vinagre y espolvorea con cebollino fresco picado."
        ],
        "per_serving": {
            "calories": 387.62,
            "protein": 16.54,
            "carbohydrates": 31.27,
            "fats": 21.82,
            "fiber": 6.8,
            "sugar": 10.75,
            "saturated_fat": 8.53,
            "sodium": 290.0,
            "vitamins_and_minerals": ["Antocianinas: 80mg", "Vitamina C: 65mg", "Calcio: 210mg"]
        },
        "total": {
            "calories": 775.24,
            "protein": 33.08,
            "carbohydrates": 62.54,
            "fats": 43.64,
            "fiber": 13.6,
            "sugar": 21.50,
            "saturated_fat": 17.06,
            "sodium": 580.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Rico en antioxidantes", "Menos de 2€"],
        "health_verdict": "Gran balance entre fibra fermentable de los frutos rojos y setas y proteína de alto valor biológico del queso.",
        "healthier_alternatives": ["Comprar frutos rojos congelados para abaratar el coste a menos de 1.20€ por ración."]
    },
    {
        "id": "book-boticaria-espaguetis-estudiante",
        "title": "Espaguetis Integrales del Estudiante con Sardinas",
        "description": "Pasta integral saciante con salsa rápida de tomate natural, sardinas en conserva desmenuzadas y aceitunas negras.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Espaguetis 100% integrales", "amount": "160g", "calories": 560, "protein": 22.4, "carbs": 112, "fat": 3.2},
            {"name": "Tomate natural triturado en conserva", "amount": "290g (1 lata pequeña)", "calories": 58, "protein": 2.9, "carbs": 11.6, "fat": 0.6},
            {"name": "Sardinas en conserva escurridas", "amount": "88g (1 lata)", "calories": 180, "protein": 21, "carbs": 0, "fat": 11},
            {"name": "Aceitunas negras laminadas", "amount": "25g", "calories": 35, "protein": 0.3, "carbs": 1.5, "fat": 3.7},
            {"name": "Dientes de ajo", "amount": "10g (2 unidades)", "calories": 14, "protein": 0.6, "carbs": 3.1, "fat": 0.05},
            {"name": "AOVE (15ml), orégano seco y sal", "amount": "Al gusto", "calories": 135, "protein": 0.2, "carbs": 0.5, "fat": 15}
        ],
        "instructions": [
            "Cuece la pasta integral en abundante agua hirviendo con sal hasta que esté al dente.",
            "En un bol apto para microondas pon el AOVE y los ajos partidos. Calienta 1 minuto a máxima potencia.",
            "Añade la lata de tomate triturado y orégano y cocina en microondas 10 minutos tapado a máxima potencia.",
            "Mezcla la pasta escurrida con la salsa de tomate caliente, las sardinas escurridas y desmenuzadas y las aceitunas negras.",
            "Espolvorea con orégano y sirve caliente."
        ],
        "per_serving": {
            "calories": 515.62,
            "protein": 23.19,
            "carbohydrates": 61.84,
            "fats": 19.50,
            "fiber": 8.2,
            "sugar": 4.59,
            "saturated_fat": 3.62,
            "sodium": 390.0,
            "vitamins_and_minerals": ["Omega-3: 1.6g", "Calcio: 240mg", "Hierro: 4.1mg"]
        },
        "total": {
            "calories": 1031.24,
            "protein": 46.38,
            "carbohydrates": 123.68,
            "fats": 39.00,
            "fiber": 16.4,
            "sugar": 9.18,
            "saturated_fat": 7.24,
            "sodium": 780.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Rico en Omega-3", "Carbohidratos complejos", "Receta de despensa", "Menos de 2€"],
        "health_verdict": "Plato de despensa económico y bromatológicamente sobresaliente: sustituye carnes procesadas por sardinas (fuente insustituible de EPA/DHA y calcio de espinas).",
        "healthier_alternatives": ["Opción veggie: sustituir las sardinas por soja texturizada fina hidratada en el tomate."]
    },
    {
        "id": "book-boticaria-tortilla-patata-calabacin-micro",
        "title": "Tortilla de Patata y Calabacín al Microondas",
        "description": "Tortilla española jugosa cocinando patata, cebolla y calabacín en 10 minutos al microondas con solo una cucharada de aceite.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Patatas medianas", "amount": "300g (2 unidades)", "calories": 231, "protein": 6, "carbs": 51, "fat": 0.3},
            {"name": "Calabacín pequeño", "amount": "150g (1 unidad)", "calories": 25, "protein": 1.8, "carbs": 4.6, "fat": 0.4},
            {"name": "Cebolla", "amount": "40g", "calories": 16, "protein": 0.5, "carbs": 3.7, "fat": 0.1},
            {"name": "Huevos camperos", "amount": "300g (4 unidades)", "calories": 375, "protein": 32.5, "carbs": 2.5, "fat": 26},
            {"name": "Aceite de oliva virgen extra", "amount": "22ml (1.5 cucharadas)", "calories": 198, "protein": 0, "carbs": 0, "fat": 22},
            {"name": "Sal", "amount": "Pizca", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Corta la cebolla en aros, ponla en un bol apto para microondas con media cucharada de AOVE, tapa y cocina 5 min a máxima potencia.",
            "Corta las patatas en láminas finas, añade al bol de la cebolla y cocina tapado 6 minutos a máxima potencia.",
            "Corta el calabacín en rodajas finas, añade a la mezcla y cocina 4 minutos más.",
            "Bate los huevos con sal en un bol amplio, incorpora la patata, calabacín y cebolla tiernos.",
            "Cuaja la tortilla en sartén antiadherente con una cucharada de AOVE a fuego medio 2 minutos por lado hasta que quede jugosa."
        ],
        "per_serving": {
            "calories": 229.34,
            "protein": 4.38,
            "carbohydrates": 26.90,
            "fats": 11.58,
            "fiber": 3.2,
            "sugar": 3.47,
            "saturated_fat": 1.81,
            "sodium": 210.0,
            "vitamins_and_minerals": ["Colina: 220mg", "Vitamina B12: 1.6mcg", "Potasio: 540mg"]
        },
        "total": {
            "calories": 458.68,
            "protein": 8.76,
            "carbohydrates": 53.80,
            "fats": 23.16,
            "fiber": 6.4,
            "sugar": 6.94,
            "saturated_fat": 3.62,
            "sodium": 420.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Bajo en calorías", "Tortilla ligera", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Reduce en un 70% las calorías y grasas respecto a la tortilla tradicional frita en sartén, manteniendo toda la jugosidad.",
        "healthier_alternatives": ["Acompañar con ensalada de tomate y pimentón para añadir licopeno."]
    },
    {
        "id": "book-boticaria-pitas-huevo-espinacas",
        "title": "Pitas Integrales con Huevo Revuelto, Espinacas y Rulo",
        "description": "Bocadillo caliente en pan de pita integral relleno de huevos revueltos, espinacas tiernas, queso de cabra y tomates secos.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Pitas 100% integrales", "amount": "180g (2 unidades)", "calories": 432, "protein": 16, "carbs": 80, "fat": 3.6},
            {"name": "Huevos camperos", "amount": "180g (3 unidades)", "calories": 225, "protein": 19.5, "carbs": 1.5, "fat": 15.6},
            {"name": "Espinacas crudas", "amount": "150g", "calories": 34, "protein": 4.3, "carbs": 5.4, "fat": 0.6},
            {"name": "Tomates secos hidratados", "amount": "15g (4-5 unidades)", "calories": 38, "protein": 2.1, "carbs": 8.4, "fat": 0.4},
            {"name": "Mini rulo de cabra", "amount": "180g", "calories": 520, "protein": 32, "carbs": 2.7, "fat": 43},
            {"name": "AOVE, pimienta y sal", "amount": "5ml", "calories": 45, "protein": 0, "carbs": 0, "fat": 5}
        ],
        "instructions": [
            "Hidrata los tomates secos en agua muy caliente durante 15 minutos y pícalos en trozos.",
            "Lava y corta las espinacas en tiras.",
            "Bate los huevos y cuájalos en sartén antiadherente con unas gotas de AOVE hasta tener un revuelto cremoso.",
            "Calienta las pitas en la tostadora.",
            "Rellena las pitas con el revuelto templado, las espinacas frescas, medallones de rulo de cabra y los tomates secos."
        ],
        "per_serving": {
            "calories": 302.68,
            "protein": 17.33,
            "carbohydrates": 5.51,
            "fats": 23.48,
            "fiber": 3.8,
            "sugar": 3.99,
            "saturated_fat": 12.90,
            "sodium": 460.0,
            "vitamins_and_minerals": ["Hierro: 3.8mg", "Calcio: 310mg", "Vitamina A: 480mcg"]
        },
        "total": {
            "calories": 605.36,
            "protein": 34.66,
            "carbohydrates": 11.02,
            "fats": 46.96,
            "fiber": 7.6,
            "sugar": 7.98,
            "saturated_fat": 25.80,
            "sodium": 920.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Vegetariano", "Saciante", "Comida para llevar", "Menos de 2€"],
        "health_verdict": "Excelente fuente de hierro vegetal optimizado por la colina y proteínas del huevo, con aporte de calcio.",
        "healthier_alternatives": ["Reducir el queso de cabra a la mitad o sustituir por queso fresco para bajar las grasas saturadas."]
    },
    {
        "id": "book-boticaria-alcachofas-langostinos",
        "title": "Salteado de Alcachofas con Langostinos al Ajo",
        "description": "Corazones de alcachofa tiernos cocinados al microondas y salteados con cebolla y langostinos en aceite de oliva virgen.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 5,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Langostinos congelados pelados", "amount": "250g", "calories": 215, "protein": 50, "carbs": 2.5, "fat": 2.5},
            {"name": "Corazones de alcachofa congelados", "amount": "250g", "calories": 117, "protein": 7.5, "carbs": 26, "fat": 0.5},
            {"name": "Cebolla", "amount": "80g (1 unidad)", "calories": 32, "protein": 0.9, "carbs": 7.4, "fat": 0.1},
            {"name": "Diente de ajo picado", "amount": "8g (1 unidad)", "calories": 11, "protein": 0.5, "carbs": 2.6, "fat": 0.05},
            {"name": "Aceite de oliva virgen extra", "amount": "10ml", "calories": 90, "protein": 0, "carbs": 0, "fat": 10},
            {"name": "Sal marina", "amount": "Pizca", "calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        ],
        "instructions": [
            "Descongela previamente los langostinos en el estante inferior de la nevera.",
            "Pon los corazones de alcachofa congelados en un recipiente para microondas con un chorro de AOVE y sal. Tapa y cocina 5 minutos a máxima potencia.",
            "Sofríe la cebolla picada y el ajo en una sartén con dos cucharadas de AOVE.",
            "Cuando la cebolla esté transparente, añade las alcachofas cocidas y los langostinos pelados.",
            "Saltea a fuego fuerte durante 3 minutos y sirve caliente."
        ],
        "per_serving": {
            "calories": 242.59,
            "protein": 31.50,
            "carbohydrates": 13.15,
            "fats": 7.11,
            "fiber": 7.4,
            "sugar": 3.90,
            "saturated_fat": 1.12,
            "sodium": 340.0,
            "vitamins_and_minerals": ["Cinarina depurativa: 25mg", "Yodo: 45mcg", "Magnesio: 60mg"]
        },
        "total": {
            "calories": 485.18,
            "protein": 63.00,
            "carbohydrates": 26.30,
            "fats": 14.22,
            "fiber": 14.8,
            "sugar": 7.80,
            "saturated_fat": 2.24,
            "sodium": 680.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Alta en proteína magra", "Muy baja en calorías", "Keto friendly", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Plato de alta densidad nutricional: más de 31g de proteína marina con apenas 240 kcal y una dosis muy alta de cinarina hepática.",
        "healthier_alternatives": ["Añadir taquitos de jamón ibérico magro para potenciar el sabor tradicional."]
    },
    {
        "id": "book-boticaria-lentejas-arroz-curcuma",
        "title": "Crema de Lentejas con Arroz Integral y Cúrcuma",
        "description": "Potaje aromático y digestivo triturado con lentejas de bote, sofrito de zanahoria, tomate, cúrcuma y guarnición de arroz integral.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1547496502-affa22d38842?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Lentejas cocidas en conserva", "amount": "400g (1 bote)", "calories": 360, "protein": 28, "carbs": 60, "fat": 2},
            {"name": "Arroz integral precocido", "amount": "125g (1 vasito)", "calories": 160, "protein": 3.5, "carbs": 33, "fat": 1.2},
            {"name": "Cebolla", "amount": "80g (1 unidad)", "calories": 32, "protein": 0.9, "carbs": 7.4, "fat": 0.1},
            {"name": "Zanahoria", "amount": "100g (1 unidad)", "calories": 40, "protein": 0.9, "carbs": 9, "fat": 0.2},
            {"name": "Tomate maduro", "amount": "80g (1 unidad)", "calories": 14, "protein": 0.7, "carbs": 3.1, "fat": 0.2},
            {"name": "Cúrcuma en polvo", "amount": "1 cucharada", "calories": 24, "protein": 0.6, "carbs": 4.5, "fat": 0.7},
            {"name": "AOVE (20ml) y sal", "amount": "Al gusto", "calories": 180, "protein": 0, "carbs": 0, "fat": 20}
        ],
        "instructions": [
            "Pica en daditos la cebolla y el tomate. Ralla la zanahoria.",
            "En una cazuela con el AOVE sofríe la cebolla hasta transparente y añade la zanahoria y el tomate.",
            "Cuando tome color naranja, añade las lentejas escurridas, cubre con agua y hierve 5 minutos.",
            "Añade la cúrcuma y tritura con batidora hasta una textura sedosa.",
            "Calienta el vasito de arroz en microondas (1 min).",
            "Sirve la crema en cuencos con 2 cucharadas de arroz integral cocido encima y espolvorea con cúrcuma."
        ],
        "per_serving": {
            "calories": 593.0,
            "protein": 24.67,
            "carbohydrates": 82.54,
            "fats": 18.24,
            "fiber": 16.2,
            "sugar": 10.26,
            "saturated_fat": 3.07,
            "sodium": 320.0,
            "vitamins_and_minerals": ["Hierro no hemo: 7.2mg", "Curcumina: 150mg", "Folato: 240mcg"]
        },
        "total": {
            "calories": 1186.0,
            "protein": 49.34,
            "carbohydrates": 165.08,
            "fats": 36.48,
            "fiber": 32.4,
            "sugar": 20.52,
            "saturated_fat": 6.14,
            "sodium": 640.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Antiinflamatorio", "Proteína vegetal completa", "Menos de 1€"],
        "health_verdict": "Plato completo vegetal antiinflamatorio. La cúrcuma aporta polifenoles y la combinación cereal-legumbre maximiza el aminograma.",
        "healthier_alternatives": ["Añadir unas gotas de zumo de limón para que la vitamina C potencie la absorción del hierro."]
    },
    {
        "id": "book-boticaria-garbanzos-pisto-ras-hanout",
        "title": "Garbanzos con Pisto y Especias Ras el Hanout",
        "description": "Guiso exprés de 10 minutos con garbanzos de bote cocinados en pisto de verduras y especias marroquíes ras el hanout.",
        "servings": 2,
        "prep_time_minutes": 2,
        "cook_time_minutes": 8,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Garbanzos cocidos en conserva escurridos", "amount": "400g (1 bote)", "calories": 420, "protein": 28, "carbs": 64, "fat": 6},
            {"name": "Pisto tradicional en conserva", "amount": "400g (1 bote)", "calories": 200, "protein": 4, "carbs": 24, "fat": 10},
            {"name": "Especias Ras el Hanout", "amount": "1 cucharada", "calories": 20, "protein": 0.8, "carbs": 3.5, "fat": 0.6},
            {"name": "Hojas de cilantro o hierbabuena fresca", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.3, "fat": 0.05}
        ],
        "instructions": [
            "Escurre los garbanzos, enjuágalos y colócalos en una cazuela cubiertos ligeramente con agua.",
            "Añade el bote de pisto y cuece a fuego medio durante 5 minutos desde que empiece a hervir.",
            "Incorpora la cucharada de Ras el Hanout (añade más agua si te gusta más caldoso).",
            "Hierve 2 minutos más para que se integren los aromas especiados.",
            "Sirve bien caliente espolvoreado con hojas frescas de cilantro o hierbabuena."
        ],
        "per_serving": {
            "calories": 297.95,
            "protein": 18.68,
            "carbohydrates": 41.88,
            "fats": 6.19,
            "fiber": 12.8,
            "sugar": 6.38,
            "saturated_fat": 0.92,
            "sodium": 460.0,
            "vitamins_and_minerals": ["Magnesio: 95mg", "Hierro: 4.8mg", "Potasio: 710mg"]
        },
        "total": {
            "calories": 595.90,
            "protein": 37.36,
            "carbohydrates": 83.76,
            "fats": 12.38,
            "fiber": 25.6,
            "sugar": 12.76,
            "saturated_fat": 1.84,
            "sodium": 920.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Plato de despensa", "Bajo en grasa", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Plato de cuchara 100% cardiosaludable preparado con conservas de calidad en menos de 10 minutos. Gran riqueza en fibra soluble.",
        "healthier_alternatives": ["Añadir un huevo poché escalfado encima para sumar 6.5g de proteína extra."]
    },
    {
        "id": "book-boticaria-escalivada-germinados-bacalao",
        "title": "Escalivada con Bacalao Desmigado, Huevo y Germinados",
        "description": "Ensalada templada de berenjena y pimientos asados con bacalao desalado, huevo duro rallado y brotes germinados vivos.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Escalivada asada en conserva", "amount": "300g (1 bote)", "calories": 90, "protein": 3, "carbs": 18, "fat": 0.6},
            {"name": "Bacalao desalado y desmigado", "amount": "250g", "calories": 205, "protein": 45, "carbs": 0, "fat": 2.5},
            {"name": "Cebolla morada en juliana", "amount": "80g", "calories": 32, "protein": 0.9, "carbs": 7.4, "fat": 0.1},
            {"name": "Huevos camperos cocidos", "amount": "150g (2 unidades)", "calories": 190, "protein": 16.5, "carbs": 1.2, "fat": 13.2},
            {"name": "Brotes germinados frescos (alfalfa o rábano)", "amount": "15g", "calories": 5, "protein": 0.6, "carbs": 0.8, "fat": 0.1},
            {"name": "AOVE (20ml), vinagre y sal", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20}
        ],
        "instructions": [
            "Cuece los huevos 10 minutos en agua, enfríalos en agua con hielo, pélalos y rállalos.",
            "Escurre las verduras de la escalivada y móntalas en la base de un plato hondo.",
            "Escurre las migas de bacalao desalado y colócalas sobre las verduras.",
            "Reparte la cebolla morada en juliana, añade el huevo rallado y remata con los germinados frescos.",
            "Aliña con el AOVE, vinagre de jerez y una pizca de sal marina."
        ],
        "per_serving": {
            "calories": 395.86,
            "protein": 61.67,
            "carbohydrates": 9.08,
            "fats": 12.54,
            "fiber": 5.1,
            "sugar": 7.33,
            "saturated_fat": 2.04,
            "sodium": 480.0,
            "vitamins_and_minerals": ["Proteína pura: 61g", "Yodo: 160mcg", "Vitamina B12: 4.8mcg"]
        },
        "total": {
            "calories": 791.72,
            "protein": 123.34,
            "carbohydrates": 18.16,
            "fats": 25.08,
            "fiber": 10.2,
            "sugar": 14.66,
            "saturated_fat": 4.08,
            "sodium": 960.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Ultra alta en proteína", "Keto friendly", "Baja en grasas", "Sin gluten", "Menos de 3€"],
        "health_verdict": "Impresionante perfil hiperproteico con más de 60g de proteína magra por plato. Muy bajo en calorías y saciedad máxima.",
        "healthier_alternatives": ["Añadir aceitunas negras aragonesas para enriquecer el perfil lipídico."]
    },
    {
        "id": "book-boticaria-copazo-ensaladilla",
        "title": "Copazo de Ensaladilla Rusa Ligera con Salsa de Huevo",
        "description": "Ensaladilla tradicional al microondas con patata, zanahoria y atún ligada con una salsa ligera batida de huevo cocido y AOVE.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Patatas medianas", "amount": "300g (2 unidades)", "calories": 231, "protein": 6, "carbs": 51, "fat": 0.3},
            {"name": "Huevos camperos cocidos", "amount": "100g (2 unidades)", "calories": 130, "protein": 11, "carbs": 0.8, "fat": 8.8},
            {"name": "Zanahoria", "amount": "100g (1 unidad)", "calories": 40, "protein": 0.9, "carbs": 9, "fat": 0.2},
            {"name": "Atún en conserva al natural", "amount": "185g (1 lata grande)", "calories": 160, "protein": 37, "carbs": 0, "fat": 1.2},
            {"name": "Aceite de oliva virgen extra", "amount": "20ml", "calories": 180, "protein": 0, "carbs": 0, "fat": 20},
            {"name": "Zumo de limón y sal", "amount": "Al gusto", "calories": 4, "protein": 0.1, "carbs": 1, "fat": 0.05}
        ],
        "instructions": [
            "Cuece los huevos 10 minutos en agua.",
            "Lava y pincha las patatas, y ponlas en un recipiente para microondas con agua. Tapa y cuece 10 min a máxima potencia. Deja enfriar.",
            "Corta las zanahorias en rodajas y cuécelas en el microondas con un poco de agua 5 minutos.",
            "Pela las patatas y córtalas en dados pequeños junto con la zanahoria y el atún escurrido.",
            "Para la 'falsa mayonesa': bate los huevos duros con el AOVE, zumo de limón y sal hasta crear una crema sedosa.",
            "Mezcla la salsa de huevo con las patatas y atún y sirve en copas frías."
        ],
        "per_serving": {
            "calories": 247.28,
            "protein": 10.26,
            "carbohydrates": 28.25,
            "fats": 10.36,
            "fiber": 3.9,
            "sugar": 4.25,
            "saturated_fat": 1.60,
            "sodium": 280.0,
            "vitamins_and_minerals": ["Vitamina A: 850mcg", "Colina: 180mg", "Potasio: 640mg"]
        },
        "total": {
            "calories": 494.56,
            "protein": 20.52,
            "carbohydrates": 56.50,
            "fats": 20.72,
            "fiber": 7.8,
            "sugar": 8.50,
            "saturated_fat": 3.20,
            "sodium": 560.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Sustituto de mayonesa", "Bajo en calorías", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Sustituye la mayonesa industrial (70% grasa) por huevo batido con AOVE, recortando más de 400 kcal por plato con excelente aporte de colina.",
        "healthier_alternatives": ["Añadir guisantes al vapor o pepinillos en vinagre picados para sumar fibra."]
    },
    {
        "id": "book-boticaria-tortilla-setas-espinacas",
        "title": "Tortilla Francesa Cremosa de Setas y Espinacas",
        "description": "Tortilla extra jugosa elaborada con espinacas y setas salteadas al ajo integradas en huevos batidos con opción de queso tierno.",
        "servings": 2,
        "prep_time_minutes": 3,
        "cook_time_minutes": 7,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Espinacas congeladas", "amount": "250g", "calories": 55, "protein": 7, "carbs": 9, "fat": 1},
            {"name": "Setas de temporada frescas", "amount": "250g", "calories": 75, "protein": 7.5, "carbs": 15, "fat": 1},
            {"name": "Huevos camperos", "amount": "300g (4 unidades)", "calories": 375, "protein": 32.5, "carbs": 2.5, "fat": 26},
            {"name": "Diente de ajo laminado", "amount": "8g (1 unidad)", "calories": 11, "protein": 0.5, "carbs": 2.6, "fat": 0.05},
            {"name": "Aceite de oliva virgen extra y sal", "amount": "15ml", "calories": 135, "protein": 0, "carbs": 0, "fat": 15}
        ],
        "instructions": [
            "En una sartén con unas gotas de AOVE saltea las espinacas congeladas según las instrucciones.",
            "En otra sartén dora el diente de ajo laminado con AOVE y saltea las setas troceadas hasta que pierdan el agua.",
            "Bate los huevos en un bol con una pizca de sal marina.",
            "Añade las espinacas y las setas calientes a los huevos batidos.",
            "Cuaja la tortilla en sartén antiadherente a fuego medio-bajo dejando el interior muy cremoso."
        ],
        "per_serving": {
            "calories": 210.73,
            "protein": 7.22,
            "carbohydrates": 9.26,
            "fats": 16.09,
            "fiber": 4.6,
            "sugar": 3.62,
            "saturated_fat": 2.45,
            "sodium": 240.0,
            "vitamins_and_minerals": ["Luteína: 12mg", "Hierro: 3.4mg", "Selenio: 30mcg"]
        },
        "total": {
            "calories": 421.46,
            "protein": 14.44,
            "carbohydrates": 18.52,
            "fats": 32.18,
            "fiber": 9.2,
            "sugar": 7.24,
            "saturated_fat": 4.90,
            "sodium": 480.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegetariano", "Keto friendly", "Muy bajo en hidratos", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Cena perfecta rápida y digestiva. Las espinacas y setas aportan abundante fibra prebiótica y carotenoides protectores de la vista.",
        "healthier_alternatives": ["Añadir una lasca de queso emmental o manchego tierno para un extra de textura."]
    },
    {
        "id": "book-boticaria-olleta-arroz-integral",
        "title": "Olleta de Arroz Integral, Alubias y Verduras al Azafrán",
        "description": "Plato de cuchara tradicional levantino con arroz integral, alubias blancas, acelgas, judías verdes, nabo y hebras de azafrán.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 15,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Arroz integral precocido", "amount": "60g (medio vaso)", "calories": 78, "protein": 1.7, "carbs": 16, "fat": 0.6},
            {"name": "Alubias blancas cocidas", "amount": "60g", "calories": 54, "protein": 3.6, "carbs": 9, "fat": 0.3},
            {"name": "Acelgas frescas troceadas", "amount": "40g", "calories": 8, "protein": 0.7, "carbs": 1.5, "fat": 0.1},
            {"name": "Judías verdes", "amount": "100g", "calories": 31, "protein": 1.8, "carbs": 7, "fat": 0.2},
            {"name": "Nabo troceado", "amount": "100g", "calories": 28, "protein": 0.9, "carbs": 6.4, "fat": 0.1},
            {"name": "Patata en trozos", "amount": "80g (1 unidad pequeña)", "calories": 62, "protein": 1.6, "carbs": 13.6, "fat": 0.1},
            {"name": "Azafrán en hebras, comino, agua (500ml), AOVE (20ml) y sal", "amount": "Al gusto", "calories": 185, "protein": 0.2, "carbs": 1, "fat": 20}
        ],
        "instructions": [
            "Corta la patata en trozos y ponla a cocer en una olla con el agua, sal, comino y azafrán molido.",
            "Trocea las acelgas, nabos y judías verdes y añádelas a la olla cuando comience a hervir.",
            "Cuece el vaso de arroz en el microondas y añade la mitad a la olla.",
            "Añade las alubias blancas cocidas.",
            "Deja cocer la olla durante 15 minutos a fuego medio.",
            "Apaga el fuego, añade un hilo de AOVE en crudo y sirve bien caliente."
        ],
        "per_serving": {
            "calories": 424.80,
            "protein": 10.50,
            "carbohydrates": 46.20,
            "fats": 22.00,
            "fiber": 8.8,
            "sugar": 4.01,
            "saturated_fat": 3.36,
            "sodium": 280.0,
            "vitamins_and_minerals": ["Azafranal antioxidante", "Vitamina K: 180mcg", "Potasio: 750mg"]
        },
        "total": {
            "calories": 849.60,
            "protein": 21.00,
            "carbohydrates": 92.40,
            "fats": 44.00,
            "fiber": 17.6,
            "sugar": 8.02,
            "saturated_fat": 6.72,
            "sodium": 560.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Plato de cuchara", "Dieta mediterránea", "Sin gluten", "Menos de 2€"],
        "health_verdict": "Guiso tradicional adaptado en versión ultrarrápida. Rico en fibra dietética, con gran densidad de fitonutrientes y azafrán.",
        "healthier_alternatives": ["Añadir un huevo duro picado por encima si se desea mayor carga proteica."]
    },
    {
        "id": "book-boticaria-ramen-casero",
        "title": "Ramen Casero en 10 Minutos",
        "description": "Sopa reconfortante japonesa exprés con caldo vegetal, fideos de arroz integrales, huevo cocido mollet, brotes de soja, zanahoria y nori.",
        "servings": 2,
        "prep_time_minutes": 4,
        "cook_time_minutes": 6,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Caldo vegetal ecológico", "amount": "1 litro", "calories": 50, "protein": 2, "carbs": 8, "fat": 1},
            {"name": "Fideos de arroz integrales", "amount": "50g", "calories": 180, "protein": 3.5, "carbs": 38, "fat": 0.8},
            {"name": "Huevos camperos", "amount": "150g (2 unidades)", "calories": 190, "protein": 16.5, "carbs": 1.2, "fat": 13.2},
            {"name": "Zanahoria rallada", "amount": "80g", "calories": 32, "protein": 0.7, "carbs": 7.2, "fat": 0.2},
            {"name": "Brotes de soja frescos", "amount": "40g", "calories": 12, "protein": 1.2, "carbs": 1.6, "fat": 0.1},
            {"name": "Tallos verdes de cebolleta en aros", "amount": "20g", "calories": 7, "protein": 0.4, "carbs": 1.5, "fat": 0.05},
            {"name": "Semillas de sésamo y lámina de alga nori", "amount": "10g", "calories": 58, "protein": 2.2, "carbs": 2.8, "fat": 5.1}
        ],
        "instructions": [
            "Cuece los huevos exactamente 6 minutos para conseguir la yema cremosa, enfría con agua con hielo para cortar cocción y pela.",
            "Cuece los fideos de arroz según instrucciones del fabricante (3-4 min) y escúrrelos en un bol.",
            "Calienta el caldo vegetal en el microondas o cazuela hasta que hierva y viértelo sobre los fideos.",
            "Corta los tallos de la cebolleta en aros finos.",
            "Añade sobre el caldo la zanahoria rallada, los brotes de soja, la cebolleta y el huevo cocido cortado en dos mitades.",
            "Decora con la lámina de alga nori y sésamo tostado y sirve bien caliente."
        ],
        "per_serving": {
            "calories": 311.15,
            "protein": 18.42,
            "carbohydrates": 30.41,
            "fats": 12.87,
            "fiber": 4.2,
            "sugar": 5.45,
            "saturated_fat": 3.11,
            "sodium": 480.0,
            "vitamins_and_minerals": ["Yodo del alga nori: 95mcg", "Vitamina A: 780mcg", "Colina: 150mg"]
        },
        "total": {
            "calories": 622.30,
            "protein": 36.84,
            "carbohydrates": 60.82,
            "fats": 25.74,
            "fiber": 8.4,
            "sugar": 10.90,
            "saturated_fat": 6.22,
            "sodium": 960.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Sustituto de ramen instantáneo", "Vegetariano", "Sin gluten", "Menos de 3€"],
        "health_verdict": "Sustituto saludable de los fideos instantáneos ultraprocesados cargados de glutamato monosódico (E-621) y grasas de palma. Gran aporte de micronutrientes marinos.",
        "healthier_alternatives": ["Añadir tiras de pechuga de pollo asada o langostinos para aumentar la proteína."]
    },
    {
        "id": "book-boticaria-helado-yogur-platano",
        "title": "Helado Casero de Yogur, Chocolate y Plátano",
        "description": "Helado cremoso 100% natural sin azúcares añadidos elaborado con plátano maduro machacado, yogur natural y cacao puro.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1587314168485-3236d6710814?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Yogur natural entero", "amount": "125g (1 unidad)", "calories": 76, "protein": 4.4, "carbs": 5.9, "fat": 4.1},
            {"name": "Plátano maduro sin piel", "amount": "80g (1 unidad)", "calories": 72, "protein": 0.9, "carbs": 18.5, "fat": 0.2},
            {"name": "Cacao puro 100% desgrasado", "amount": "15g (1 cucharada)", "calories": 48, "protein": 3.7, "carbs": 2.2, "fat": 3}
        ],
        "instructions": [
            "Machaca el plátano con un tenedor hasta formar una papilla suave.",
            "Mezcla en un bol el plátano con el yogur natural y el cacao puro en polvo.",
            "Coloca la mezcla en moldes para helado o moldes de magdalenas.",
            "Introduce un palito de helado y congela al menos 2 horas.",
            "(Truco de chef: si tienes el plátano congelado previamente, bátelo directamente con el yogur y cacao para tomar al instante tipo 'soft')."
        ],
        "per_serving": {
            "calories": 121.59,
            "protein": 3.34,
            "carbohydrates": 17.90,
            "fats": 4.07,
            "fiber": 2.8,
            "sugar": 5.67,
            "saturated_fat": 2.66,
            "sodium": 50.0,
            "vitamins_and_minerals": ["Polifenoles del cacao: 240mg", "Potasio: 380mg", "Magnesio: 45mg"]
        },
        "total": {
            "calories": 243.18,
            "protein": 6.68,
            "carbohydrates": 35.80,
            "fats": 8.14,
            "fiber": 5.6,
            "sugar": 11.34,
            "saturated_fat": 5.32,
            "sodium": 100.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Postre saludable", "Sin azúcar añadido", "Vegetariano", "Sin gluten", "Menos de 1€"],
        "health_verdict": "Sustituto ideal de los helados ultraprocesados industriales (que suelen tener 25-30g de azúcares libres y grasas hidrogenadas).",
        "healthier_alternatives": ["Sustituir el plátano por fresas congeladas o mango maduro para variar sabores."]
    },
    {
        "id": "book-boticaria-batido-arandanos-avena",
        "title": "Batido Saciente de Plátano, Arándanos y Avena",
        "description": "Smoothie energizante con arándanos frescos, medio plátano, avena molida rica en betaglucanos y leche fría con canela.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Arándanos frescos o congelados", "amount": "100g", "calories": 57, "protein": 0.7, "carbs": 14.5, "fat": 0.3},
            {"name": "Plátano maduro", "amount": "40g (medio plátano)", "calories": 36, "protein": 0.5, "carbs": 9.2, "fat": 0.1},
            {"name": "Avena molida integral", "amount": "60g", "calories": 225, "protein": 8.4, "carbs": 40.2, "fat": 4.2},
            {"name": "Leche entera o bebida de soja", "amount": "250ml (1 taza)", "calories": 150, "protein": 8, "carbs": 12, "fat": 8},
            {"name": "Hielo picado, canela en polvo o nuez moscada", "amount": "Al gusto", "calories": 5, "protein": 0.1, "carbs": 1, "fat": 0.05}
        ],
        "instructions": [
            "En el vaso de la batidora pon los arándanos, el medio plátano, la avena molida y la leche o bebida vegetal.",
            "Tritura a máxima potencia durante 1 minuto hasta obtener una textura sedosa.",
            "Añade hielo picado al gusto y bate unos segundos más.",
            "Sirve en vasos altos y espolvorea canela de Ceylán molida por encima."
        ],
        "per_serving": {
            "calories": 232.60,
            "protein": 8.77,
            "carbohydrates": 34.08,
            "fats": 6.80,
            "fiber": 4.5,
            "sugar": 10.01,
            "saturated_fat": 3.39,
            "sodium": 80.0,
            "vitamins_and_minerals": ["Betaglucano: 1.6g", "Antocianinas: 120mg", "Calcio: 190mg"]
        },
        "total": {
            "calories": 465.20,
            "protein": 17.54,
            "carbohydrates": 68.16,
            "fats": 13.60,
            "fiber": 9.0,
            "sugar": 20.02,
            "saturated_fat": 6.78,
            "sodium": 160.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Cardioprotector", "Rico en betaglucano", "Desayuno o merienda", "Menos de 1€"],
        "health_verdict": "La EFSA reconoce que 3g diarios de betaglucano de avena reducen el colesterol LDL. Los arándanos aportan pterostilbeno antioxidante.",
        "healthier_alternatives": ["Personas con celiaquía deben verificar que la avena tenga sello Espiga Barrada sin gluten."]
    },
    {
        "id": "book-boticaria-pudding-chia-mango",
        "title": "Pudding de Chía con Mango y Leche de Coco",
        "description": "Vaso en capas de semillas de chía gelificadas en leche de coco con puré natural de mango y daditos frescos.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Semillas de chía", "amount": "50g", "calories": 240, "protein": 8.5, "carbs": 21, "fat": 15.5},
            {"name": "Leche de coco cremosa", "amount": "400ml", "calories": 200, "protein": 4, "carbs": 12, "fat": 18},
            {"name": "Mango maduro", "amount": "300g (medio mango)", "calories": 180, "protein": 2.4, "carbs": 45, "fat": 1.2}
        ],
        "instructions": [
            "Mezcla las semillas de chía con la leche de coco en un tarro y deja reposar en nevera al menos 2 horas (o toda la noche) hasta que gelifique.",
            "Pela el mango y corta un cuarto en daditos pequeños para decorar.",
            "Tritura el resto del mango con la batidora hasta obtener un puré suave y dulce.",
            "Monta los vasos alternando una capa del pudding de chía gelificado con otra capa de puré de mango.",
            "Decora con los dados de mango frescos reservados."
        ],
        "per_serving": {
            "calories": 277.76,
            "protein": 8.61,
            "carbohydrates": 30.18,
            "fats": 44.47,
            "fiber": 10.2,
            "sugar": 23.55,
            "saturated_fat": 33.38,
            "sodium": 40.0,
            "vitamins_and_minerals": ["Omega-3 vegetal (ALA): 4.8g", "Vitamina C: 55mg", "Calcio: 190mg"]
        },
        "total": {
            "calories": 555.52,
            "protein": 17.22,
            "carbohydrates": 60.36,
            "fats": 88.94,
            "fiber": 20.4,
            "sugar": 47.10,
            "saturated_fat": 66.76,
            "sodium": 80.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Vegano", "Sin gluten", "Rico en Omega-3", "Postre saludable", "Menos de 2€"],
        "health_verdict": "Las semillas de chía aportan una cantidad descomunal de fibra soluble mucilaginosa que nutre la microbiota y regula el tránsito intestinal.",
        "healthier_alternatives": ["Usar leche de almendra o avena sin azúcar para reducir las grasas saturadas de la leche de coco."]
    },
    {
        "id": "book-boticaria-pina-plancha-cardamomo",
        "title": "Piña a la Plancha con Cardamomo y Hierbabuena",
        "description": "Cuñas de piña fresca caramelizadas en su propio jugo a la plancha con cardamomo verde molido y ralladura de lima.",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 3,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Piña natural fresca", "amount": "500g (media piña)", "calories": 250, "protein": 2.5, "carbs": 65, "fat": 0.5},
            {"name": "Vaina de cardamomo verde", "amount": "1 unidad", "calories": 4, "protein": 0.1, "carbs": 0.8, "fat": 0.05},
            {"name": "Piel de lima o limón rallada", "amount": "Al gusto", "calories": 2, "protein": 0.05, "carbs": 0.5, "fat": 0.02},
            {"name": "Hojas de hierbabuena fresca", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.3, "fat": 0.05}
        ],
        "instructions": [
            "Pela la piña, retira el centro leñoso y corta en cuñas triangulares.",
            "Asa las cuñas en sartén antiadherente bien caliente sin aceite hasta que se doren por ambos lados caramelizando su jugo natural.",
            "Muele las semillas interiores de la vaina de cardamomo en un mortero.",
            "Sirve la piña caliente en copas espolvoreada con el cardamomo molido, ralladura de lima y hojas de hierbabuena."
        ],
        "per_serving": {
            "calories": 131.68,
            "protein": 0.65,
            "carbohydrates": 31.46,
            "fats": 0.36,
            "fiber": 3.6,
            "sugar": 26.43,
            "saturated_fat": 0.01,
            "sodium": 5.0,
            "vitamins_and_minerals": ["Bromelina digestiva: 120mg", "Vitamina C: 78mg", "Manganeso: 1.5mg"]
        },
        "total": {
            "calories": 263.36,
            "protein": 1.30,
            "carbohydrates": 62.92,
            "fats": 0.72,
            "fiber": 7.2,
            "sugar": 52.86,
            "saturated_fat": 0.02,
            "sodium": 10.0
        },
        "nutri_score": "A",
        "dietary_tags": ["Vegano", "Digestivo", "Ultra bajo en grasa", "Sin gluten", "Menos de 2€"],
        "health_verdict": "La piña contiene bromelina, enzima proteolítica que facilita la digestión de comidas copiosas. Postre dulce y ligero sin azúcar refinado.",
        "healthier_alternatives": ["Acompañar con una quenelle de yogur griego desnatado para sumar proteína."]
    },
    {
        "id": "book-boticaria-naranjas-menta-chocolate",
        "title": "Gajos de Naranja con Menta y Chocolate Negro 85%",
        "description": "Gajos jugosos de naranja fresca bañados a la mitad en chocolate negro puro 85% fundido y hojas de menta picadas.",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 2,
        "source_type": "libro",
        "source_reference": "Comida rápida, barata y saludable (Boticaria García)",
        "image_url": "https://images.unsplash.com/photo-1587314168485-3236d6710814?w=700&auto=format&fit=crop&q=80",
        "ingredients": [
            {"name": "Naranjas dulces de mesa", "amount": "300g (2 unidades)", "calories": 141, "protein": 2.7, "carbs": 35.4, "fat": 0.3},
            {"name": "Chocolate negro 85-90% cacao", "amount": "100g", "calories": 590, "protein": 9.5, "carbs": 24, "fat": 48},
            {"name": "Hojas de menta fresca", "amount": "Al gusto", "calories": 2, "protein": 0.1, "carbs": 0.3, "fat": 0.05}
        ],
        "instructions": [
            "Pela las naranjas a lo vivo, separa los gajos y sécalos con papel de cocina.",
            "Funde el chocolate negro en el microondas en intervalos de 30 segundos removiendo para que no se queme.",
            "Sumerge cada gajo hasta la mitad en el chocolate fundido.",
            "Colócalos en un plato cubierto con papel vegetal separados entre sí durante 5 minutos para que enfríen.",
            "Guárdalos 10 minutos en la nevera para que el chocolate quede crujiente y sirve con hojas de menta picadas."
        ],
        "per_serving": {
            "calories": 318.09,
            "protein": 6.13,
            "carbohydrates": 27.20,
            "fats": 20.53,
            "fiber": 6.8,
            "sugar": 25.06,
            "saturated_fat": 13.01,
            "sodium": 15.0,
            "vitamins_and_minerals": ["Vitamina C: 92mg", "Flavonoides del cacao: 320mg", "Magnesio: 95mg"]
        },
        "total": {
            "calories": 636.18,
            "protein": 12.26,
            "carbohydrates": 54.40,
            "fats": 41.06,
            "fiber": 13.6,
            "sugar": 50.12,
            "saturated_fat": 26.02,
            "sodium": 30.0
        },
        "nutri_score": "B",
        "dietary_tags": ["Postre antioxidante", "Vegano", "Sin gluten", "Menos de 2€"],
        "health_verdict": "El cacao con más de 85% aporta teobromina estimulante y flavonoides cardiosaludables. Combinado con la vitamina C de la naranja, optimiza la asimilación del hierro.",
        "healthier_alternatives": ["Usar 50g de chocolate para rebajar las calorías y grasas a la mitad si estás en definición."]
    }
]

def main():
    print(f"Importando {len(BOTICARIA_RECIPES)} recetas oficiales de 'Comida rápida, barata y saludable'...")
    for recipe in BOTICARIA_RECIPES:
        saved = save_recipe(recipe)
        print(f"-> Guardada: {saved['title']}")
    print(f"¡Completado con éxito! Se han añadido {len(BOTICARIA_RECIPES)} recetas.")

if __name__ == "__main__":
    main()
