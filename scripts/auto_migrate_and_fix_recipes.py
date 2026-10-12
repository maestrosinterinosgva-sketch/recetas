"""
Script de migración y corrección automática de recetas:
1. Reclasifica las categorías al nuevo sistema de 5 momentos:
   - Desayuno
   - Comida
   - Merienda
   - Cena
   - Postre
2. Corrige automáticamente todas las fotos que no correspondan al plato,
   estén rotas (404/hotlink Rechupete), provengan de miniaturas temporales de Google,
   o tengan placeholders genéricos.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import list_recipes, save_recipe
from app.gemini_service import get_culinary_image_for_title

def classify_recipe(title: str, current_cat: str) -> str:
    t = (title or "").lower()
    
    # 1. Postres claros
    if any(k in t for k in ['mousse', 'tarta', 'pastel', 'bizcocho', 'brownie', 'flan', 'helado', 'sorbete', 'polo', 'galleta', 'cookie', 'bombón', 'bombon', 'ferrero', 'cake', 'dulce', 'pudding', 'natillas', 'chocolate']):
        if 'tartar' not in t and 'pastel de verdura' not in t and 'pastel de berenjena' not in t and 'pastel de coliflor' not in t and 'pastel de carne' not in t:
            return 'postre'

    # 2. Desayunos claros
    if any(k in t for k in ['tortita', 'pancake', 'panqueque', 'crepe', 'gofre', 'waffle', 'banana bread', 'porridge', 'budwig', 'avena']):
        if 'verdura' not in t and 'espinaca' not in t and 'salada' not in t:
            return 'desayuno'
        return 'comida' # Tortitas saladas / crepes saladas

    # 3. Meriendas claras
    if any(k in t for k in ['batido', 'smoothie', 'sándwich', 'sandwich', 'tosta', 'magdalena', 'muffin', 'dip', 'chips', 'gajos de naranja', 'piña a la plancha']):
        return 'merienda'

    # 4. Cenas ligeras
    if any(k in t for k in ['ensalada', 'crema', 'sopa', 'gazpacho', 'salmorejo', 'tortilla', 'revuelto', 'wrap', 'fajita', 'pizza', 'pita', 'carpaccio', 'tartar', 'berenjena', 'san jacobo', 'quiche', 'guacamole', 'chips de kale']):
        return 'cena'

    # 5. Comidas principales
    return 'comida'

def run():
    recipes = list_recipes()
    total = len(recipes)
    print(f"Iniciando actualización automática sobre {total} recetas en Neon PostgreSQL...")
    
    photos_fixed = 0
    categories_fixed = 0
    
    for r in recipes:
        rid = r["id"]
        title = r.get("title", "")
        old_cat = str(r.get("category") or "").strip().lower()
        old_img = str(r.get("image_url") or "").strip()
        
        # 1. Clasificación de categoría
        new_cat = classify_recipe(title, old_cat)
        cat_changed = False
        if old_cat != new_cat:
            r["category"] = new_cat
            cat_changed = True
            categories_fixed += 1
            
        # 2. Corrección automática de foto
        img_changed = False
        if not old_img.startswith("/uploads/"):
            suggested_img = get_culinary_image_for_title(title)
            
            # Criterios para actualizar la imagen
            should_replace = (
                "recetasderechupete.com" in old_img or
                "encrypted-tbn0.gstatic.com" in old_img or
                "google.com" in old_img or
                "photo-1498837167922-ddd27525d352" in old_img or  # Generic salad bowl
                old_img == "" or
                (old_img != suggested_img and not old_img.startswith("/uploads/"))
            )
            
            if should_replace and suggested_img and suggested_img != old_img:
                r["image_url"] = suggested_img
                img_changed = True
                photos_fixed += 1
                print(f"[FOTO] {title} -> {suggested_img[:50]}...")
                
        if cat_changed or img_changed:
            save_recipe(r)
            
    print("\n" + "="*50)
    print(f"Resumen de actualización:")
    print(f" - Recetas analizadas: {total}")
    print(f" - Fotos gastronómicas corregidas y actualizadas: {photos_fixed}")
    print(f" - Categorías actualizadas al nuevo sistema de 5 momentos: {categories_fixed}")
    print("="*50)

if __name__ == "__main__":
    run()
