import { useState, useEffect } from 'react';
import { contentService } from '../services/api';
import toast from 'react-hot-toast';

// Mapeo de códigos de idioma a nombres completos
const LANGUAGE_MAP = {
  es: 'Spanish',
  en: 'English',
  fr: 'French',
  it:  'Italian',
};

export const useContentGenerator = () => {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(false);
  const [configLoading, setConfigLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Cargar configuración al montar
  useEffect(() => {
    const loadConfig = async () => {
      try {
        const data = await contentService.getConfig();
        console.log('✅ Config loaded:', data); // Debug
        setConfig(data);
      } catch (err) {
        console.error('❌ Error loading config:', err);
        // Fallback con configuración por defecto si el backend no responde
        const fallbackConfig = {
          platforms: [
            { id: 'blog', name: 'Blog', max_length: '1500-2000 palabras', description: 'informativo y detallado' },
            { id: 'twitter', name: 'Twitter/X', max_length: '280 caracteres', description: 'conciso e impactante' },
            { id: 'instagram', name: 'Instagram', max_length: '2200 caracteres', description: 'visual y emotivo' },
            { id: 'linkedin', name: 'LinkedIn', max_length: '700-1300 caracteres', description: 'profesional' }
          ],
          audiences: [
            { id: 'general', name: 'Público General', description: 'audiencia general' },
            { id: 'professional', name: 'Profesionales', description: 'profesionales del sector' },
            { id: 'technical', name: 'Técnicos/Expertos', description: 'expertos técnicos' },
            { id: 'young', name: 'Jóvenes (18-25)', description: 'audiencia joven' },
            { id: 'children', name: 'Infantil (8-12)', description: 'niños en edad escolar' },
            { id: 'business', name: 'Empresarial', description: 'directivos empresariales' }
          ],
          llm_providers: ['groq', 'ollama'],
          content_types: ['general', 'financial', 'science']
        };
        console.log('⚠️ Using fallback config');
        setConfig(fallbackConfig);
        toast.error('Backend no disponible. Usando configuración por defecto.');
      } finally {
        setConfigLoading(false);
      }
    };
    loadConfig();
  }, []);

  const generateContent = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await contentService.generateContent({
        topic: formData.topic,
        platform: formData.platform,
        audience: formData.audience,
        additional_context: formData.additionalContext || '',
        tone: formData.tone || '',
        keywords: formData.keywords || '',
        // image_prompt: formData.imagePrompt || formData.topic, // ⚠️ COMENTADO temporalmente - Esperar a que backend lo agregue
        llm_provider: formData.llmProvider,
        language:  LANGUAGE_MAP[formData.language] || 'Spanish',
      });
      
      setResult(data);
      toast.success('¡Contenido generado exitosamente! 🎉');
      return data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error al generar contenido';
      setError(errorMessage);
      toast.error(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearResult = () => {
    setResult(null);
    setError(null);
  };

  return {
    config,
    configLoading,
    loading,
    result,
    error,
    generateContent,
    clearResult,
  };
};