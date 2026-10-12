import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# Load environment variables from .env
load_dotenv(ENV_FILE)

UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

def get_gemini_api_key() -> str:
    """Obtiene la clave de API de Gemini configurada."""
    return os.environ.get("GEMINI_API_KEY", "").strip()

def set_gemini_api_key(api_key: str) -> None:
    """Guarda la clave de API en el archivo .env y en el entorno."""
    api_key = api_key.strip()
    os.environ["GEMINI_API_KEY"] = api_key
    
    # Escribir o actualizar el archivo .env
    lines = []
    found = False
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    lines.append(f"GEMINI_API_KEY={api_key}\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"GEMINI_API_KEY={api_key}\n")
    
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)
