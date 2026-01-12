import { useState } from 'react';
import { FiSend, FiLoader } from 'react-icons/fi';
import PlatformSelector from './PlatformSelector';

const ContentForm = ({ config, onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    topic: '',
    platform: 'linkedin',
    audience: 'general',
    additionalContext: '',
    tone: '',
    llmProvider: 'groq',
    language: 'es', // Español por defecto
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.topic.trim()) return;
    onSubmit(formData); // formData incluye language
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Topic */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="topic">
          📌 Tema del contenido *
        </label>
        <textarea
          id="topic"
          value={formData.topic}
          onChange={(e) => handleChange('topic', e.target.value)}
          placeholder="Ej: Los beneficios de la inteligencia artificial en la educación moderna"
          className="input-field min-h-[100px] resize-none"
          required
          aria-describedby="topic-desc"
        />
        <div id="topic-desc" className="sr-only">
          Describe el tema principal del contenido.
        </div>
      </div>

      {/* Platform */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          📱 Plataforma
        </label>
        <PlatformSelector
          platforms={config?.platforms}
          selected={formData.platform}
          onChange={(value) => handleChange('platform', value)}
        />
      </div>

      {/* Audience & LLM Provider */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="audience">
            👥 Audiencia
          </label>
          <select
            id="audience"
            value={formData.audience}
            onChange={(e) => handleChange('audience', e.target.value)}
            className="input-field"
          >
            {config?.audiences?.map((aud) => (
              <option key={aud.id} value={aud.id}>
                {aud.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="llmProvider">
            🤖 Modelo LLM
          </label>
          <select
            id="llmProvider"
            value={formData.llmProvider}
            onChange={(e) => handleChange('llmProvider', e.target.value)}
            className="input-field"
          >
            <option value="groq">Groq (Cloud - Rápido)</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>
      </div>

      {/* Language selector added */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="language">
          🌐 Idioma
        </label>
        <select
          id="language"
          value={formData.language}
          onChange={(e) => handleChange('language', e.target.value)}
          className="input-field"
          aria-label="Seleccionar idioma de salida"
        >
          <option value="es">Español (por defecto)</option>
          <option value="en">Inglés</option>
          <option value="fr">Francés</option>
          <option value="it">Italiano</option>
        </select>
      </div>

      {/* Additional Options */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="tone">
            🎨 Tono específico (opcional)
          </label>
          <input
            id="tone"
            type="text"
            value={formData.tone}
            onChange={(e) => handleChange('tone', e.target.value)}
            placeholder="Ej: inspirador, humorístico, formal..."
            className="input-field"
            aria-describedby="tone-desc"
          />
          <div id="tone-desc" className="sr-only">Opcional: especifica el tono deseado.</div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="additionalContext">
            📝 Contexto adicional (opcional)
          </label>
          <input
            id="additionalContext"
            type="text"
            value={formData.additionalContext}
            onChange={(e) => handleChange('additionalContext', e.target.value)}
            placeholder="Información extra, keywords..."
            className="input-field"
          />
        </div>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || !formData.topic.trim()}
        className="btn-primary w-full"
        aria-disabled={loading || !formData.topic.trim()}
      >
        {loading ? (
          <>
            <FiLoader className="animate-spin h-5 w-5" />
            Generando contenido...
          </>
        ) : (
          <>
            <FiSend className="h-5 w-5" />
            Generar Contenido
          </>
        )}
      </button>
    </form>
  );
};

export default ContentForm;