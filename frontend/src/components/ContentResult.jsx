import { useState } from 'react';
import { FiCopy, FiCheck, FiRefreshCw, FiTwitter, FiInstagram, FiLinkedin, FiFileText } from 'react-icons/fi';
import toast from 'react-hot-toast';

const platformConfig = {
  blog: { icon: FiFileText, color: 'text-purple-600', bg: 'bg-purple-50', badge: 'bg-purple-500' },
  twitter: { icon: FiTwitter, color: 'text-blue-500', bg: 'bg-blue-50', badge: 'bg-blue-400' },
  instagram: { icon: FiInstagram, color: 'text-pink-600', bg: 'bg-pink-50', badge: 'bg-gradient-to-r from-purple-500 to-pink-500' },
  linkedin: { icon: FiLinkedin, color: 'text-blue-700', bg: 'bg-blue-50', badge: 'bg-blue-600' },
};

const ContentResult = ({ result, onClear }) => {
  const [copied, setCopied] = useState(false);
  
  const config = platformConfig[result.platform] || platformConfig.blog;
  const Icon = config.icon;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      toast.success('¡Copiado al portapapeles!', {
        icon: '✅',
        style: {
          borderRadius: '12px',
          background: '#10b981',
          color: '#fff',
        },
      });
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Error al copiar', {
        icon: '❌',
        style: {
          borderRadius: '12px',
        },
      });
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-purple-100 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-50 to-purple-50 px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-2.5 rounded-xl ${config.badge} shadow-sm`}>
              <Icon className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-gray-900 text-lg">Contenido Generado</h3>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-xs font-semibold text-purple-600 bg-purple-100 px-2 py-1 rounded-full">
                  {result.platform}
                </span>
                <span className="text-xs text-gray-500">•</span>
                <span className="text-xs text-gray-600">{result.audience}</span>
                <span className="text-xs text-gray-500">•</span>
                <span className="text-xs text-gray-600">{result.model_used}</span>
              </div>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="p-2.5 hover:bg-white rounded-xl transition-all duration-200 group border border-transparent hover:border-gray-200 hover:shadow-sm"
              title="Copiar contenido"
            >
              {copied ? (
                <FiCheck className="h-5 w-5 text-green-600" />
              ) : (
                <FiCopy className="h-5 w-5 text-gray-600 group-hover:text-purple-600" />
              )}
            </button>
            <button
              onClick={onClear}
              className="p-2.5 hover:bg-white rounded-xl transition-all duration-200 group border border-transparent hover:border-gray-200 hover:shadow-sm"
              title="Nueva generación"
            >
              <FiRefreshCw className="h-5 w-5 text-gray-600 group-hover:text-purple-600 group-hover:rotate-180 transition-transform duration-300" />
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <div className={`${config.bg} rounded-xl p-5 border-2 border-${result.platform === 'instagram' ? 'pink' : result.platform === 'twitter' ? 'blue' : result.platform === 'linkedin' ? 'blue' : 'purple'}-100`}>
          <div className="prose prose-sm max-w-none whitespace-pre-wrap text-gray-800 leading-relaxed">
            {result.content}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="px-6 pb-4">
        <div className="bg-gray-50 rounded-xl p-3 border border-gray-200">
          <p className="text-xs text-gray-600">
            <span className="font-semibold text-gray-700">Tema:</span> {result.topic}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ContentResult;

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