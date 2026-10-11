import os
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import requests
import yt_dlp

logger = logging.getLogger(__name__)
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

def save_thumbnail_locally(thumbnail_url: Optional[str], file_id: str) -> Optional[str]:
    """Descarga la miniatura de la red social para almacenarla localmente y evitar expiración o bloqueos de hotlinking (CORS/403)."""
    if not thumbnail_url:
        return None
    try:
        thumb_filename = f"thumb_{file_id}.jpg"
        thumb_path = UPLOADS_DIR / thumb_filename
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.instagram.com/"
        }
        resp = requests.get(thumbnail_url, headers=headers, timeout=10)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(thumb_path, "wb") as f:
                f.write(resp.content)
            return f"/uploads/{thumb_filename}"
    except Exception as e:
        logger.warning(f"No se pudo descargar miniatura localmente: {e}")
    return thumbnail_url

def download_social_video_or_info(url: str) -> Dict[str, Any]:
    """
    Descarga el vídeo o extrae información textual y metadatos de TikTok, Instagram, YouTube, etc.
    """
    file_id = str(uuid.uuid4())
    output_template = str(UPLOADS_DIR / f"{file_id}.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'max_filesize': 60 * 1024 * 1024,  # Máx 60 MB
        'socket_timeout': 20,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                title = info.get('title', 'Vídeo de red social')
                description = info.get('description', '')
                duration = info.get('duration', 0)
                
                # Encontrar archivo descargado en uploads
                video_path = None
                for ext in ['mp4', 'mkv', 'webm', 'mov']:
                    candidate = UPLOADS_DIR / f"{file_id}.{ext}"
                    if candidate.exists():
                        video_path = str(candidate)
                        break
                
                raw_thumbnail = info.get('thumbnail')
                if not raw_thumbnail and info.get('thumbnails'):
                    raw_thumbnail = info['thumbnails'][-1].get('url')
                
                local_thumb = save_thumbnail_locally(raw_thumbnail, file_id)
                
                return {
                    "success": True,
                    "video_path": video_path,
                    "title": title,
                    "description": description,
                    "duration": duration,
                    "url": url,
                    "source": info.get('extractor_key', 'Social Media'),
                    "thumbnail": local_thumb
                }
    except Exception as e:
        logger.warning(f"Error descargando vídeo con yt-dlp: {e}. Intentando solo extraer metadatos...")
        # Intento de respaldo: extraer sólo metadatos sin descargar el archivo de vídeo
        try:
            ydl_opts_meta = {
                'skip_download': True,
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 15,
            }
            with yt_dlp.YoutubeDL(ydl_opts_meta) as ydl_meta:
                info = ydl_meta.extract_info(url, download=False)
                if info:
                    raw_thumbnail = info.get('thumbnail')
                    if not raw_thumbnail and info.get('thumbnails'):
                        raw_thumbnail = info['thumbnails'][-1].get('url')
                    local_thumb = save_thumbnail_locally(raw_thumbnail, file_id)
                    return {
                        "success": True,
                        "video_path": None,
                        "title": info.get('title', 'Vídeo de red social'),
                        "description": info.get('description', ''),
                        "duration": info.get('duration', 0),
                        "url": url,
                        "source": info.get('extractor_key', 'Social Media'),
                        "thumbnail": local_thumb,
                        "note": "Descarga de vídeo restringida por la plataforma, analizando metadatos y descripción."
                    }
        except Exception as e_meta:
            logger.error(f"Fallo completo extrayendo enlace: {e_meta}")
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
            
    return {"success": False, "error": "No se pudo procesar el enlace de red social."}

def cleanup_file(filepath: Optional[str]):
    """Elimina archivos temporales."""
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo temporal {filepath}: {e}")
