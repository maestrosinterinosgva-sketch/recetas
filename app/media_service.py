import os
import re
import html
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import requests
import yt_dlp

logger = logging.getLogger(__name__)
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}

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
        resp = requests.get(thumbnail_url, headers=headers, timeout=8)
        if resp.status_code == 200 and len(resp.content) > 500:
            with open(thumb_path, "wb") as f:
                f.write(resp.content)
            return f"/uploads/{thumb_filename}"
    except Exception as e:
        logger.warning(f"No se pudo descargar miniatura localmente: {e}")
    return thumbnail_url

def extract_social_fallback(url: str, file_id: str) -> Optional[Dict[str, Any]]:
    """
    Extractor directo y resiliente para TikTok, YouTube e Instagram.
    Utiliza APIs oficiales oEmbed y metadatos públicos que nunca sufren bloqueos de bot.
    """
    url_lower = url.lower()

    # --- 1. TIKTOK ---
    if 'tiktok.com' in url_lower:
        try:
            # Resolver enlaces cortos como vm.tiktok.com o vt.tiktok.com
            resp = requests.head(url, headers=DEFAULT_HEADERS, allow_redirects=True, timeout=8)
            final_url = resp.url or url
            clean_url = final_url.split('?')[0]
            
            oembed_url = f"https://www.tiktok.com/oembed?url={clean_url}"
            r = requests.get(oembed_url, headers=DEFAULT_HEADERS, timeout=8)
            if r.status_code == 200:
                data = r.json()
                caption = data.get("title", "")
                author = data.get("author_name", "TikTok")
                raw_thumb = data.get("thumbnail_url", "")
                
                # En TikTok el texto del creador contiene todos los ingredientes y pasos
                first_line = caption.split('\n')[0].strip() if '\n' in caption else caption[:80]
                title = first_line if len(first_line) > 5 else f"Receta de TikTok por {author}"
                
                local_thumb = save_thumbnail_locally(raw_thumb, file_id) or raw_thumb
                
                return {
                    "success": True,
                    "title": title,
                    "description": caption,
                    "source": "TikTok",
                    "thumbnail": local_thumb,
                    "url": url,
                    "video_path": None,
                    "author": author
                }
        except Exception as e:
            logger.warning(f"Error en fallback de TikTok: {e}")

    # --- 2. YOUTUBE / YOUTUBE SHORTS ---
    if any(k in url_lower for k in ['youtube.com', 'youtu.be']):
        try:
            oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
            r = requests.get(oembed_url, headers=DEFAULT_HEADERS, timeout=8)
            if r.status_code == 200:
                data = r.json()
                title = data.get("title", "Receta en YouTube")
                author = data.get("author_name", "YouTube")
                raw_thumb = data.get("thumbnail_url", "")
                
                # Intentar obtener descripción completa o de la página
                desc = ""
                try:
                    page_resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=8)
                    if page_resp.status_code == 200:
                        m_desc = re.search(r'"shortDescription":"(.*?)"', page_resp.text)
                        if m_desc:
                            desc = m_desc.group(1).encode('utf-8').decode('unicode_escape')
                        else:
                            m_og = re.search(r'<meta property="og:description" content="(.*?)"', page_resp.text)
                            if m_og:
                                desc = html.unescape(m_og.group(1))
                except Exception:
                    pass
                
                full_desc = f"{title}\n\nCanal: {author}\n\n{desc}".strip()
                local_thumb = save_thumbnail_locally(raw_thumb, file_id) or raw_thumb
                
                return {
                    "success": True,
                    "title": title,
                    "description": full_desc,
                    "source": "YouTube",
                    "thumbnail": local_thumb,
                    "url": url,
                    "video_path": None,
                    "author": author
                }
        except Exception as e:
            logger.warning(f"Error en fallback de YouTube: {e}")

    # --- 3. INSTAGRAM REELS / POSTS ---
    if 'instagram.com' in url_lower:
        try:
            m = re.search(r'instagram\.com/(?:reel|p)/([^/?#&]+)', url)
            shortcode = m.group(1) if m else None
            if shortcode:
                embed_url = f"https://www.instagram.com/p/{shortcode}/embed/captioned/"
                r = requests.get(embed_url, headers=DEFAULT_HEADERS, timeout=8)
                if r.status_code == 200:
                    text_html = r.text
                    m_cap = re.search(r'class="Caption"[^>]*>(.*?)</div>', text_html, re.DOTALL)
                    caption = ""
                    if m_cap:
                        raw_caption = re.sub(r'<[^>]+>', ' ', m_cap.group(1))
                        caption = html.unescape(raw_caption).strip()
                    
                    m_img = re.search(r'class="EmbeddedMediaImage"[^>]*src="([^"]+)"', text_html)
                    raw_thumb = html.unescape(m_img.group(1)) if m_img else ""
                    
                    first_line = caption.split('\n')[0].strip() if '\n' in caption else caption[:80]
                    title = first_line if len(first_line) > 5 else "Receta de Instagram"
                    local_thumb = save_thumbnail_locally(raw_thumb, file_id) or raw_thumb
                    
                    return {
                        "success": True,
                        "title": title,
                        "description": caption or "Receta compartida en Instagram Reel",
                        "source": "Instagram",
                        "thumbnail": local_thumb,
                        "url": url,
                        "video_path": None
                    }
        except Exception as e:
            logger.warning(f"Error en fallback de Instagram: {e}")

    # --- 4. FALLBACK GENÉRICO OPENGRAPH ---
    try:
        r = requests.get(url, headers=DEFAULT_HEADERS, timeout=8)
        if r.status_code == 200:
            html_text = r.text
            m_title = re.search(r'<meta property="og:title" content="(.*?)"', html_text) or re.search(r'<title>(.*?)</title>', html_text)
            m_desc = re.search(r'<meta property="og:description" content="(.*?)"', html_text) or re.search(r'<meta name="description" content="(.*?)"', html_text)
            m_img = re.search(r'<meta property="og:image" content="(.*?)"', html_text)
            
            title = html.unescape(m_title.group(1)).strip() if m_title else "Receta de Red Social"
            desc = html.unescape(m_desc.group(1)).strip() if m_desc else ""
            raw_thumb = html.unescape(m_img.group(1)).strip() if m_img else ""
            local_thumb = save_thumbnail_locally(raw_thumb, file_id) if raw_thumb else ""
            
            if title or desc:
                return {
                    "success": True,
                    "title": title,
                    "description": desc or title,
                    "source": "Web",
                    "thumbnail": local_thumb or raw_thumb,
                    "url": url,
                    "video_path": None
                }
    except Exception as e:
        logger.warning(f"Error en fallback genérico OpenGraph: {e}")

    return None

def download_social_video_or_info(url: str) -> Dict[str, Any]:
    """
    Descarga el vídeo o extrae información textual y metadatos de TikTok, Instagram, YouTube, etc.
    Incluye fallback inteligente directo para servidores cloud donde las plataformas bloquean yt-dlp.
    """
    file_id = str(uuid.uuid4())
    output_template = str(UPLOADS_DIR / f"{file_id}.%(ext)s")
    
    # 1. Intentar descarga completa con yt-dlp si es posible
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'max_filesize': 50 * 1024 * 1024,
        'socket_timeout': 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                title = info.get('title', 'Vídeo de red social')
                description = info.get('description', '')
                duration = info.get('duration', 0)
                
                video_path = None
                for ext in ['mp4', 'mkv', 'webm', 'mov']:
                    candidate = UPLOADS_DIR / f"{file_id}.{ext}"
                    if candidate.exists():
                        video_path = str(candidate)
                        break
                
                raw_thumbnail = info.get('thumbnail')
                if not raw_thumbnail and info.get('thumbnails'):
                    raw_thumbnail = info['thumbnails'][-1].get('url')
                
                local_thumb = save_thumbnail_locally(raw_thumbnail, file_id) or raw_thumbnail
                
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
        logger.warning(f"yt-dlp no pudo descargar el vídeo ({e}). Activando extractor inteligente de metadatos...")

    # 2. Extractor inteligente y directo de metadatos
    fallback_res = extract_social_fallback(url, file_id)
    if fallback_res and fallback_res.get("success"):
        logger.info(f"Extractor social exitoso para {url}: {fallback_res.get('title')}")
        return fallback_res

    return {
        "success": False,
        "error": "No se pudo extraer la información del vídeo. Prueba a copiar el texto de la publicación o compartir la receta por texto.",
        "url": url
    }

def cleanup_file(filepath: Optional[str]):
    """Elimina archivos temporales."""
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo temporal {filepath}: {e}")
