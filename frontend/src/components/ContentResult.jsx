import { useState } from 'react';
import { FiCopy, FiCheck, FiRefreshCw, FiTwitter, FiInstagram, FiLinkedin, FiFileText } from 'react-icons/fi';
import toast from 'react-hot-toast';

const platformConfig = {
  blog: { icon: FiFileText, color:  'text-purple-600', bg: 'bg-purple-50' },
  twitter: { icon: FiTwitter, color: 'text-blue-500', bg: 'bg-blue-50' },
  instagram:  { icon: FiInstagram, color: 'text-pink-600', bg: 'bg-pink-50' },
  linkedin: { icon: FiLinkedin, color: 'text-sky-700', bg: 'bg-sky-50' },
};

const ContentResult = ({ result, onClear }) => {
  const [copied, setCopied] = useState(false);
  
  const config = platformConfig[result.platform] || platformConfig.blog;
  const Icon = config.icon;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      toast.success('¡Copiado al portapapeles!');
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Error al copiar');
    }
  };

  return (
    <div className="card">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${config.bg}`}>
            <Icon className={`h-5 w-5 ${config.color}`} />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">Contenido Generado</h3>
            <p className="text-sm text-gray-500">
              {result.platform} • {result.audience} • {result.model_used}
            </p>
          </div>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Copiar contenido"
          >
            {copied ? (
              <FiCheck className="h-5 w-5 text-green-600" />
            ) : (
              <FiCopy className="h-5 w-5 text-gray-600" />
            )}
          </button>
          <button
            onClick={onClear}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Nueva generación"
          >
            <FiRefreshCw className="h-5 w-5 text-gray-600" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className={`${config.bg} rounded-lg p-4 border border-gray-200`}>
        <div className="prose prose-sm max-w-none whitespace-pre-wrap text-gray-800">
          {result.content}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-4 pt-4 border-t border-gray-100">
        <p className="text-xs text-gray-400">
          Tema: {result.topic}
        </p>
      </div>
    </div>
  );
};

export default ContentResult;