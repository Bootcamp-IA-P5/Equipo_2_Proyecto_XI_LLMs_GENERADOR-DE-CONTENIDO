"""
Servicio para generación de imágenes con Pollinations API
"""
import httpx
import urllib.parse
from typing import Optional
from app.core.config import get_settings

settings = get_settings()


class ImageService:
    """Servicio de imágenes con Pollinations API"""
    
    API_URL = "https://gen.pollinations.ai/api/image"
    
    @classmethod
    async def generate_image(cls, prompt: str, width: int = 1200, height: int = 630) -> Optional[str]:
        """
        Genera una imagen usando Pollinations API
        
        Returns:
            URL de la imagen generada o None si falla
        """
        if not settings.POLLINATIONS_API_KEY:
            # Fallback a placeholder si no hay API key
            safe_text = urllib.parse.quote(prompt[: 20])
            return f"https://placehold.co/{width}x{height}/4A90A4/ffffff? text={safe_text}"
        
        headers = {
            "Authorization": f"Bearer {settings.POLLINATIONS_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": f"{prompt}, professional photo, high quality, 4k",
            "width":  width,
            "height": height
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    cls.API_URL,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("url") or data.get("image_url")
                else:
                    print(f"Pollinations API error: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    @classmethod
    def get_platform_image(cls, topic: str, platform: str) -> str:
        """
        Genera URL placeholder (para uso síncrono)
        """
        sizes = {
            "twitter": (1200, 675),
            "instagram": (1080, 1080),
            "linkedin": (1200, 627),
            "blog": (1200, 630)
        }
        
        width, height = sizes.get(platform, (1200, 630))
        safe_text = urllib.parse.quote(topic[:30])
        return f"https://placehold.co/{width}x{height}/4A90A4/ffffff?text={safe_text}"
    
    @classmethod
    def get_themed_image(cls, topic: str, platform:  str) -> str:
        """Alias para compatibilidad"""
        return cls.get_platform_image(topic, platform)