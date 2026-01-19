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
    language: 'es',
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.topic.trim()) return;
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 text-sm">

      {/* TEMA */}
      <div>
        <label className="font-semibold text-gray-700 mb-1 block">
          📝 Tema del contenido <span className="text-red-500">*</span>
        </label>
        <textarea
          value={formData.topic}
          onChange={(e) => handleChange('topic', e.target.value)}
          placeholder="Ej: Beneficios de la IA en educación"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-200 resize-none min-h-[80px]"
          required
        />
      </div>

      {/* GRID 3 COLUMNAS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">

        {/* AUDIENCIA */}
        <div>
          <label className="font-semibold text-gray-700 mb-1 block">
            👥 Audiencia
          </label>
          <select
            value={formData.audience}
            onChange={(e) => handleChange('audience', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white"
          >
            {config?.audiences?.map((aud) => (
              <option key={aud.id} value={aud.id}>
                {aud.name}
              </option>
            ))}
          </select>
        </div>

        {/* MODELO */}
        <div>
          <label className="font-semibold text-gray-700 mb-1 block">
            🤖 Modelo
          </label>
          <select
            value={formData.llmProvider}
            onChange={(e) => handleChange('llmProvider', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white"
          >
            <option value="groq">Groq - Llama</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>

        {/* IDIOMA */}
        <div>
          <label className="font-semibold text-gray-700 mb-1 block">
            🌍 Idioma
          </label>
          <select
            value={formData.language}
            onChange={(e) => handleChange('language', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white"
          >
            <option value="es">Español</option>
            <option value="en">Inglés</option>
            <option value="fr">Francés</option>
            <option value="it">Italiano</option>
          </select>
        </div>
      </div>

      {/* PLATAFORMAS */}
      <div>
        <label className="font-semibold text-gray-700 mb-2 block">
          📱 Plataformas <span className="text-red-500">*</span>
        </label>
        <PlatformSelector
          platforms={config?.platforms}
          selected={formData.platform}
          onChange={(value) => handleChange('platform', value)}
          compact
        />
      </div>

      {/* TONO + CONTEXTO */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <input
          type="text"
          value={formData.tone}
          onChange={(e) => handleChange('tone', e.target.value)}
          placeholder="🎨 Tono (opcional)"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
        />
        <input
          type="text"
          value={formData.additionalContext}
          onChange={(e) => handleChange('additionalContext', e.target.value)}
          placeholder="💬 Contexto adicional"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
        />
      </div>

      {/* TIP */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 text-xs text-purple-800">
        💡 Cuanto más específico seas, mejor será el resultado.
      </div>

      {/* BOTÓN */}
      <button
        type="submit"
        disabled={loading || !formData.topic.trim()}
        className="w-full py-3 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
      >
        {loading ? (
          <>
            <FiLoader className="animate-spin" />
            Generando...
          </>
        ) : (
          <>
            <FiSend />
            Generar contenido
          </>
        )}
      </button>
    </form>
  );
};

export default ContentForm;
