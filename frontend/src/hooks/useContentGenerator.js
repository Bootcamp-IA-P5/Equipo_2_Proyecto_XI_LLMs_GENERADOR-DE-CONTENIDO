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
        setConfig(data);
      } catch (err) {
        console.error('Error loading config:', err);
        toast.error('Error al cargar la configuración');
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
        llm_provider: formData.llmProvider,
        language:  LANGUAGE_MAP[formData.language] || 'Spanish', // ✅ AÑADIDO:  Mapear idioma
      });
      
      setResult(data);
      toast.success('¡Contenido generado exitosamente!');
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