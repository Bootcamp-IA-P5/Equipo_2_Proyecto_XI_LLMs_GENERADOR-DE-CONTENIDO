import { useEffect, useState } from 'react';
import { FiLoader, FiZap } from 'react-icons/fi';

const CURIOSIDADES_IA = [
  'RAG combina un motor de búsqueda con un LLM para reducir alucinaciones en respuestas.',
  'Transformers usan self-attention para procesar palabras en paralelo, no secuencialmente.',
  'Fine-tuning con LoRA ajusta solo un 1% de los parámetros del modelo, ahorrando recursos.',
  'GPT-4 usa Mixture of Experts (MoE), activando solo ciertos expertos por consulta.',
  'AlphaFold resolvió el plegamiento de proteínas con redes neuronales geométricas.',
  'Stable Diffusion genera imágenes a partir de ruido gaussiano guiado por texto.',
  'CUDA permite entrenar redes neuronales miles de veces más rápido que en CPU.',
  'LangChain permite crear agentes de IA que usan herramientas externas.',
  'Los embeddings convierten texto en vectores con significado semántico.',
  'Prompt engineering es clave para obtener respuestas precisas.',
  'Chain-of-Thought mejora el razonamiento paso a paso.',
  'Vision Transformers procesan imágenes como secuencias de parches.',
];

const GeneratingModal = ({ show }) => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (!show) return;

    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % CURIOSIDADES_IA.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [show]);

  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div className="bg-white/90 rounded-2xl shadow-2xl border border-purple-200 max-w-lg w-full mx-4 p-8 text-center animate-fade-in">
        
        {/* ICON */}
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-linear-to-br from-purple-100 to-pink-100 flex items-center justify-center">
          <FiZap className="h-8 w-8 text-purple-600" />
        </div>

        {/* TITLE */}
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          Generando contenido...
        </h3>

        {/* LOADER */}
        <div className="flex justify-center mb-4">
          <FiLoader className="h-6 w-6 animate-spin text-purple-600" />
        </div>

        {/* CURIOSITY */}
        <div className="bg-purple-50 border border-purple-200 rounded-xl px-4 py-3 min-h-[80px] flex items-center justify-center transition-all duration-500">
          <p className="text-sm text-purple-800 font-medium">
            💡 <span className="font-semibold">¿Sabías que?</span><br />
            {CURIOSIDADES_IA[index]}
          </p>
        </div>
      </div>
    </div>
  );
};

export default GeneratingModal;
