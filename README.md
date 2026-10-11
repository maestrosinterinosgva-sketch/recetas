# 🥗 NutriChef AI - Analizador & Comparador Nutricional de Recetas

Una aplicación web completa y moderna que analiza recetas culinarias desde **texto**, **fotos** o **vídeos de redes sociales** (TikTok, Instagram Reels, YouTube Shorts), calcula sus calorías y macronutrientes, permite comparar recetas nutricionalmente cara a cara y sugiere recetas personalizadas en base a tus metas nutricionales.

---

## 🌟 Características Principales

1. **Analizador Multimodal Inteligente (Gemini 3.8 Flash)**:
   - **✍️ Texto**: Escribe o pega cualquier receta, lista de ingredientes o pasos de preparación.
   - **📷 Foto**: Sube una foto de un plato terminado, libro de cocina o ingredientes desde tu dispositivo o cámara.
   - **🎬 Vídeo o Red Social**:
     - Pega enlaces directos de **TikTok**, **Instagram Reels**, **YouTube Shorts** o YouTube convencional (extracción automática con `yt-dlp`).
     - O sube directamente tus archivos de vídeo de cocina (`.mp4`, `.mov`, `.webm`).
   - **Desglose Nutricional Completo**:
     - Calorías totales y por porción (Kcal).
     - Nutri-Score europeo oficial (A, B, C, D, E).
     - Macronutrientes con gráfico interactivo: Proteínas, Carbohidratos, Grasas totales, Grasas saturadas, Fibra dietética, Azúcares simples y Sodio.
     - Micronutrientes destacados (vitaminas y minerales).
     - Veredicto de nutricionista IA con semáforo y consejos para hacer la receta más saludable.

2. **⚖️ Comparador Nutricional Cara a Cara**:
   - Selecciona 2 o más recetas de tu recetario.
   - Gráficos interactivos comparativos de macronutrientes y calorías.
   - Tabla comparativa lado a lado con métricas detalladas.
   - Análisis inteligente: ¿Cuál es mejor para **ganancia de masa muscular**, cuál para **déficit calórico / pérdida de grasa** y cuál para **salud general**?

3. **🎯 Sugerencias de Recetas por Metas Nutricionales**:
   - Define tus objetivos: Calorías deseadas, mínimo de proteína, límite de carbohidratos o grasas.
   - Filtra por tipo de dieta: Alta en proteína, Mediterránea, Keto, Vegetariana, Vegana, Baja en sodio, Sin gluten.
   - Indica los ingredientes que tienes en tu despensa o nevera.
   - La IA genera recetas calculadas matemáticamente que encajan en tus requerimientos y las puedes guardar con 1 clic.

4. **📖 Mi Recetario Persistente**:
   - Base de datos SQLite integrada con recetas iniciales de ejemplo listas para usar.
   - Búsqueda en tiempo real, filtros, visualizador de detalles y opción de añadir a la comparativa.

---

## 🚀 Cómo Iniciar la Aplicación

### Método 1: Doble clic en Windows (Más rápido)
Simplemente haz doble clic sobre el archivo:
```
iniciar_app.bat
```
Esto levantará el servidor automáticamente y abrirá tu navegador web en `http://127.0.0.1:8000`.

### Método 2: Desde la terminal (PowerShell)
```powershell
.\venv\Scripts\uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Abre en tu navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔑 Configuración de Google Gemini API

La app funciona inmediatamente en modo de prueba / demo sin clave. Para activar el análisis de visión multimodal y vídeo en tiempo real con **Gemini 3.8 Flash**:

1. Obtén tu clave gratuita en [Google AI Studio](https://aistudio.google.com/apikey).
2. Haz clic en el botón superior derecho de la app (**"Gemini / Ajustes"**) o agrégala en el archivo `.env`:
   ```env
   GEMINI_API_KEY=tu_clave_aqui
   ```

---

## 📁 Estructura del Proyecto

```
recetas/
├── app/
│   ├── config.py           # Configuración y gestión de GEMINI_API_KEY
│   ├── models.py           # Modelos Pydantic para recetas, nutrientes y comparador
│   ├── database.py         # Base de datos SQLite y recetas iniciales
│   ├── gemini_service.py   # Servicio multimodal con Google GenAI SDK (Gemini 3.8)
│   └── media_service.py    # Extracción y descarga con yt-dlp para TikTok/Instagram/YouTube
├── static/
│   ├── css/custom.css      # Estilos personalizados y Nutri-Score
│   └── js/app.js           # Lógica frontend interactiva con Chart.js
├── templates/
│   └── index.html          # Interfaz web responsiva moderna con Tailwind CSS
├── uploads/                # Directorio temporal para archivos subidos y procesados
├── iniciar_app.bat         # Lanzador rápido para Windows
├── requirements.txt        # Dependencias Python
└── main.py                 # Servidor backend FastAPI y rutas REST
```
