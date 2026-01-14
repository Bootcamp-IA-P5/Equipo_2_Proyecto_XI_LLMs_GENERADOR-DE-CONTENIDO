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
    
    BASE_URL = "https://image.pollinations.ai/prompt"
    
    @classmethod
    async def generate_image(cls, prompt: str, width: int = 1200, height: int = 630) -> Optional[str]:
        """Genera una imagen usando Pollinations API"""
        
        if not settings.POLLINATIONS_API_KEY:
            return cls._get_fallback_image(prompt, width, height)
        
        try:
            enhanced_prompt = f"{prompt}, professional photo, high quality, 4k, detailed"
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            image_url = f"{cls.BASE_URL}/{encoded_prompt}"
            
            params = {
                "width": width,
                "height": height,
                "nologo": "true",
                "enhance": "true"
            }
            
            headers = {
                "Authorization": f"Bearer {settings.POLLINATIONS_API_KEY}"
            }
            
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                response = await client.get(image_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        return str(response.url)
                    else:
                        return f"{image_url}?width={width}&height={height}&nologo=true&token={settings.POLLINATIONS_API_KEY}"
                else:
                    return f"{image_url}?width={width}&height={height}&nologo=true&token={settings.POLLINATIONS_API_KEY}"
                    
        except Exception:
            return cls._get_fallback_image(prompt, width, height)
    
    @classmethod
    def _get_fallback_image(cls, prompt: str, width: int, height: int) -> str:
        """Genera imagen placeholder como fallback"""
        safe_text = urllib.parse.quote(prompt[:30])
        return f"https://placehold.co/{width}x{height}/4A90A4/ffffff?text={safe_text}"
    
    @classmethod
    def get_platform_image(cls, topic: str, platform: str) -> str:
        """Genera URL placeholder (para uso síncrono)"""
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
    def get_themed_image(cls, topic: str, platform: str) -> str:
        """Alias para compatibilidad"""
        return cls.get_platform_image(topic, platform)