import re
import json
import sqlite3
import unicodedata
from pypdf import PdfReader
from bs4 import BeautifulSoup
from app.database import save_recipe
from app.gemini_service import get_culinary_image_for_title

def normalize_title(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

# Base nutritional reference per 100g (kcal, protein, carbs, fat, fiber)
FOOD_DB = {
    'aceite': (884, 0, 0, 100, 0),
    'arroz': (350, 7.5, 78, 1, 1.5),
    'pasta': (350, 12, 72, 1.5, 3),
    'espagueti': (350, 12, 72, 1.5, 3),
    'macarron': (350, 12, 72, 1.5, 3),
    'fideo': (350, 12, 72, 1.5, 3),
    'pollo': (120, 23, 0, 2.5, 0),
    'pavo': (110, 24, 0, 1.5, 0),
    'ternera': (180, 22, 0, 10, 0),
    'cerdo': (200, 20, 0, 13, 0),
    'lomo': (160, 22, 0, 8, 0),
    'conejo': (135, 21, 0, 5, 0),
    'salmon': (208, 20, 0, 13.5, 0),
    'merluza': (80, 16.5, 0, 1.5, 0),
    'bacalao': (82, 17.5, 0, 0.7, 0),
    'atun': (105, 24, 0, 1, 0),
    'bonito': (130, 23, 0, 4, 0),
    'dorada': (95, 19, 0, 2, 0),
    'lubina': (98, 19, 0, 2.5, 0),
    'pescado': (90, 18, 0, 2, 0),
    'gamba': (90, 20, 0.5, 1, 0),
    'langostino': (90, 20, 0.5, 1, 0),
    'huevo': (143, 12.8, 0.7, 9.9, 0),
    'garbanzo': (125, 8.5, 18, 2.5, 6),
    'lenteja': (116, 9, 18, 0.5, 7.5),
    'alubia': (115, 8.5, 17, 0.6, 7),
    'judia': (115, 8.5, 17, 0.6, 7),
    'guisante': (80, 5.5, 12, 0.5, 5),
    'tofu': (80, 8.5, 1.8, 4.5, 0.5),
    'patata': (77, 2, 17, 0.1, 2.2),
    'boniato': (86, 1.6, 20, 0.1, 3),
    'calabacin': (17, 1.2, 3.1, 0.3, 1),
    'berenjena': (25, 1, 5.7, 0.2, 3),
    'tomate': (18, 0.9, 3.9, 0.2, 1.2),
    'cebolla': (40, 1.1, 9, 0.1, 1.7),
    'cebolleta': (32, 1.8, 7.3, 0.2, 2.6),
    'pimiento': (26, 1, 5.3, 0.3, 1.7),
    'zanahoria': (41, 0.9, 9.6, 0.2, 2.8),
    'espinaca': (23, 2.9, 3.6, 0.4, 2.2),
    'brocoli': (34, 2.8, 6.6, 0.4, 2.6),
    'coliflor': (25, 1.9, 5, 0.3, 2),
    'alcachofa': (47, 3.3, 10.5, 0.2, 5.4),
    'esparrago': (20, 2.2, 3.9, 0.1, 2.1),
    'champinon': (22, 3.1, 3.3, 0.3, 1),
    'seta': (25, 3, 4, 0.3, 1.5),
    'puerro': (61, 1.5, 14.2, 0.3, 1.8),
    'aguacate': (160, 2, 8.5, 14.7, 6.7),
    'queso': (250, 18, 2, 19, 0),
    'mozzarella': (280, 22, 2, 21, 0),
    'leche': (45, 3.2, 4.8, 1.5, 0),
    'yogur': (60, 4, 5, 3, 0),
    'avena': (375, 13.5, 58.7, 7, 10),
    'harina': (360, 10, 75, 1.2, 3),
    'pan': (260, 8.5, 52, 1.5, 3.5),
    'platano': (89, 1.1, 22.8, 0.3, 2.6),
    'manzana': (52, 0.3, 13.8, 0.2, 2.4),
    'pera': (57, 0.4, 15.2, 0.1, 3.1),
    'fresa': (32, 0.7, 7.7, 0.3, 2),
    'naranja': (47, 0.9, 11.8, 0.1, 2.4),
    'limon': (29, 1.1, 9.3, 0.3, 2.8),
    'sandia': (30, 0.6, 7.6, 0.2, 0.4),
    'melon': (34, 0.8, 8.2, 0.2, 0.9),
    'pina': (50, 0.5, 13.1, 0.1, 1.4),
    'fruto seco': (600, 18, 15, 54, 7),
    'almendra': (579, 21, 21.6, 49.9, 12.5),
    'nuez': (654, 15.2, 13.7, 65.2, 6.7),
    'chocolate': (545, 5.5, 60, 31, 7),
    'datil': (282, 2.5, 75, 0.4, 8),
    'jamon': (210, 30, 0.5, 10, 0)
}

def estimate_line_nutrition(line):
    line_clean = line.strip()
    lower = line_clean.lower()
    
    # Estimate grams or units
    grams = 100.0  # default
    
    # Grams pattern (e.g. 200 g, 200g, 200 gramos)
    g_match = re.search(r'(\d+)\s*(g|gr|gramos)\b', lower)
    if g_match:
        grams = float(g_match.group(1))
    elif 'cucharada' in lower or 'cucharadita' in lower:
        if 'cucharadita' in lower:
            grams = 5.0
        else:
            grams = 15.0
        # check number of spoons
        sp_match = re.search(r'(\d+)\s*cucharad', lower)
        if sp_match:
            grams *= float(sp_match.group(1))
    elif 'taza' in lower or 'vaso' in lower:
        grams = 180.0
        tz_match = re.search(r'(\d+)\s*(taza|vaso)', lower)
        if tz_match:
            grams *= float(tz_match.group(1))
    elif 'huevo' in lower:
        h_match = re.search(r'(\d+)\s*huevo', lower)
        count = float(h_match.group(1)) if h_match else 2.0
        grams = count * 60.0
    elif 'pizca' in lower or 'sal' in lower or 'pimienta' in lower or 'canela' in lower:
        grams = 3.0
    else:
        # Check simple number at beginning e.g. "2 cebollas", "1 patata"
        unit_match = re.search(r'^(\d+)\s+([a-záéíóúñ]+)', lower)
        if unit_match:
            num = float(unit_match.group(1))
            grams = num * 120.0
            
    # Find matching food in FOOD_DB
    matched_profile = None
    for k, profile in FOOD_DB.items():
        if k in lower:
            matched_profile = profile
            break
            
    if not matched_profile:
        # generic healthy food fallback: 70 kcal/100g
        matched_profile = (70.0, 3.0, 10.0, 1.5, 2.0)
        
    factor = grams / 100.0
    cal = round(matched_profile[0] * factor, 1)
    prot = round(matched_profile[1] * factor, 1)
    carbs = round(matched_profile[2] * factor, 1)
    fat = round(matched_profile[3] * factor, 1)
    
    # Clean ingredient name
    name_clean = line_clean
    if name_clean.endswith('.'):
        name_clean = name_clean[:-1]
    name_clean = re.sub(r'^[•\-\*]\s*', '', name_clean)
    
    return {
        'name': name_clean,
        'amount': f"{int(grams)}g" if grams >= 10 else line_clean[:20],
        'calories': cal,
        'protein': prot,
        'carbs': carbs,
        'fat': fat
    }

def categorize_recipe(title, desc="", ingredients_text=""):
    combined = f"{title} {desc} {ingredients_text}".lower()
    if any(k in combined for k in ['desayuno', 'pancake', 'porridge', 'tostada']):
        return 'desayuno'
    elif any(k in combined for k in ['postre', 'merienda', 'bizcocho', 'tarta', 'galleta', 'mousse', 'helado', 'batido', 'smoothie', 'donut', 'bombone', 'sorbete', 'dulce', 'pudin', 'crepe']):
        return 'merienda-postre'
    elif any(k in combined for k in ['cena', 'crema', 'sopa', 'tortilla', 'ensalada', 'wrap', 'ligero', 'verdura al vapor']):
        return 'cena'
    else:
        return 'comida'

def determine_nutri_score(cal_per_serv, sat_fat, fiber):
    if cal_per_serv < 450 and fiber >= 4:
        return 'A'
    elif cal_per_serv < 600:
        return 'B'
    elif cal_per_serv < 750:
        return 'C'
    return 'B'

print("Helper module loaded successfully.")
