import { useState } from 'react';
import { FiSend, FiLoader } from 'react-icons/fi';
import PlatformSelector from './PlatformSelector';

const ContentForm = ({ config, onSubmit, loading }) => {
  console.log('📋 ContentForm config:', config); // Debug
  
  const [formData, setFormData] = useState({
    topic: '',
    platform: 'linkedin',
    audience: 'general',
    additionalContext: '',
    tone: '',
    keywords: '',
    imagePrompt: '',
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
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Topic */}
      <div>
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="topic">
          <span className="text-lg">📝</span>
          Tema del contenido
          <span className="text-red-500">*</span>
        </label>
        <textarea
          id="topic"
          value={formData.topic}
          onChange={(e) => handleChange('topic', e.target.value)}
          placeholder="Ej: Los beneficios de la inteligencia artificial en la educación moderna"
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all resize-none min-h-25 placeholder:text-gray-400"
          required
          aria-describedby="topic-desc"
        />
        <p id="topic-desc" className="text-xs text-gray-500 mt-1">
          Describe el tema principal del contenido
        </p>
      </div>

      {/* Platform */}
      <div>
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-3">
          <span className="text-lg">📱</span>
          Plataformas
          <span className="text-red-500">*</span>
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
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="audience">
            <span className="text-lg">👥</span>
            Audiencia
          </label>
          <select
            id="audience"
            value={formData.audience}
            onChange={(e) => handleChange('audience', e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all bg-white"
          >
            {config?.audiences?.map((aud) => (
              <option key={aud.id} value={aud.id}>
                {aud.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="llmProvider">
            <span className="text-lg">🤖</span>
            Modelo LLM
          </label>
          <select
            id="llmProvider"
            value={formData.llmProvider}
            onChange={(e) => handleChange('llmProvider', e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all bg-white"
          >
            <option value="groq">Groq Cloud - Llama</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>
      </div>

      {/* Language */}
      <div>
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="language">
          <span className="text-lg">🌍</span>
          Idioma
        </label>
        <select
          id="language"
          value={formData.language}
          onChange={(e) => handleChange('language', e.target.value)}
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all bg-white"
          aria-label="Seleccionar idioma de salida"
        >
          <option value="es">Español (por defecto)</option>
          <option value="en">Inglés</option>
          <option value="fr">Francés</option>
          <option value="it">Italiano</option>
        </select>
      </div>

      {/* Tone & Keywords */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="tone">
            <span className="text-lg">🎨</span>
            Tono específico
            <span className="text-xs text-gray-500 font-normal">(Opcional)</span>
          </label>
          <input
            id="tone"
            type="text"
            value={formData.tone}
            onChange={(e) => handleChange('tone', e.target.value)}
            placeholder="Ej: inspirador, humorístico, formal..."
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all placeholder:text-gray-400"
            aria-describedby="tone-desc"
          />
          <p id="tone-desc" className="text-xs text-gray-500 mt-1">Lo supongo humorístico, técnico, formal</p>
        </div>

        <div>
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="keywords">
            <span className="text-lg">🔑</span>
            Palabras clave
            <span className="text-xs text-gray-500 font-normal">(Opcional)</span>
          </label>
          <input
            id="keywords"
            type="text"
            value={formData.keywords}
            onChange={(e) => handleChange('keywords', e.target.value)}
            placeholder="Ej: innovación, educación, tecnología..."
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all placeholder:text-gray-400"
          />
          <p className="text-xs text-gray-500 mt-1">Separa con comas las keywords</p>
        </div>
      </div>

      {/* Image Description */}
      <div>
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="imagePrompt">
          <span className="text-lg">🖼️</span>
          Descripción de la imagen
          <span className="text-xs text-gray-500 font-normal">(Opcional)</span>
        </label>
        <input
          id="imagePrompt"
          type="text"
          value={formData.imagePrompt}
          onChange={(e) => handleChange('imagePrompt', e.target.value)}
          placeholder="Ej: Una ilustración moderna de inteligencia artificial en educación..."
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all placeholder:text-gray-400"
        />
        <p className="text-xs text-gray-500 mt-1">
          Describe la imagen que quieres generar para acompañar tu contenido
        </p>
      </div>

      {/* Additional Context */}
      <div>
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2" htmlFor="additionalContext">
          <span className="text-lg">💬</span>
          Contexto adicional
          <span className="text-xs text-gray-500 font-normal">(Opcional)</span>
        </label>
        <input
          id="additionalContext"
          type="text"
          value={formData.additionalContext}
          onChange={(e) => handleChange('additionalContext', e.target.value)}
          placeholder="Información extra, keywords..."
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring focus:ring-purple-100 transition-all placeholder:text-gray-400"
        />
      </div>

      {/* Tip */}
      <div className="bg-linear-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-xl p-4">
        <div className="flex gap-3">
          <span className="text-2xl">💡</span>
          <div>
            <p className="text-sm font-semibold text-purple-900">Consejo:</p>
            <p className="text-sm text-purple-700">
              Cuanto más específico seas con el tema y las palabras clave, mejor será el contenido generado.
            </p>
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || !formData.topic.trim()}
        className="w-full bg-linear-to-r from-purple-600 to-pink-600 text-white font-semibold py-4 px-6 rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
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