import os
import uvicorn
from app.database import init_db

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Database init note: {e}")

    port = int(os.environ.get("PORT", 8000))
    print(f"Iniciando NutriChef Recetas en el puerto {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
