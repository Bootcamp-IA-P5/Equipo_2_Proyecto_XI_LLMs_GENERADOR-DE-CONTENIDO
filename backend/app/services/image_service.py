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
        """
        Genera una imagen usando Pollinations API
        
        Returns:
            URL de la imagen generada o None si falla
        """
        # Verificar que existe API key
        if not settings.POLLINATIONS_API_KEY:
            print("⚠️ POLLINATIONS_API_KEY no configurada")
            return cls._get_fallback_image(prompt, width, height)
        
        try:
            # Mejorar el prompt
            enhanced_prompt = f"{prompt}, professional photo, high quality, 4k, detailed"
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # Construir URL
            image_url = f"{cls.BASE_URL}/{encoded_prompt}"
            
            # Headers con API key
            headers = {
                "Authorization": f"Bearer {settings.POLLINATIONS_API_KEY}"
            }
            
            # Parámetros
            params = {
                "width": width,
                "height": height,
                "nologo": "true",
                "enhance": "true"
            }
            
            print(f"🌐 Solicitando imagen: {image_url}")
            print(f"🔑 Usando API key: {settings.POLLINATIONS_API_KEY[:15]}...")
            
            # Hacer petición con headers
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(
                    image_url,
                    headers=headers,
                    params=params
                )
                
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    # La URL final después de redirects
                    final_url = str(response.url)
                    print(f"✅ Imagen generada: {final_url}")
                    return final_url
                else:
                    print(f"❌ Error: {response.status_code} - {response.text[:200]}")
                    return cls._get_fallback_image(prompt, width, height)
                    
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return cls._get_fallback_image(prompt, width, height)
    
    @classmethod
    def _get_fallback_image(cls, prompt: str, width: int, height: int) -> str:
        """Genera imagen placeholder como fallback"""
        safe_text = urllib.parse.quote(prompt[:30])
        return f"https://placehold.co/{width}x{height}/4A90A4/ffffff?text={safe_text}"
    
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
    def get_themed_image(cls, topic: str, platform: str) -> str:
        """Alias para compatibilidad"""
        return cls.get_platform_image(topic, platform)