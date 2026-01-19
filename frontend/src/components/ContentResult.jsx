import { useState } from 'react';
import { FiCopy, FiCheck, FiRefreshCw, FiTwitter, FiInstagram, FiLinkedin, FiFileText } from 'react-icons/fi';
import toast from 'react-hot-toast';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

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
        <div className="prose prose-sm max-w-none text-gray-800">
          <ReactMarkdown 
            remarkPlugins={[remarkGfm]}
            components={{
              // Custom styling for markdown elements
              h1: ({node, ...props}) => <h1 className="text-xl font-bold mb-2 text-gray-900" {...props} />,
              h2: ({node, ...props}) => <h2 className="text-lg font-bold mb-2 mt-4 text-gray-900" {...props} />,
              h3: ({node, ...props}) => <h3 className="text-base font-semibold mb-1 mt-3 text-gray-800" {...props} />,
              p: ({node, ...props}) => <p className="mb-3 leading-relaxed" {...props} />,
              ul: ({node, ...props}) => <ul className="list-disc list-inside mb-3 space-y-1" {...props} />,
              ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-3 space-y-1" {...props} />,
              li: ({node, ...props}) => <li className="ml-2" {...props} />,
              strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
              em: ({node, ...props}) => <em className="italic" {...props} />,
              blockquote: ({node, ...props}) => (
                <blockquote className="border-l-4 border-gray-300 pl-4 italic my-3 text-gray-600" {...props} />
              ),
              code: ({node, inline, ...props}) => 
                inline ? (
                  <code className="bg-gray-200 px-1 py-0.5 rounded text-sm font-mono" {...props} />
                ) : (
                  <code className="block bg-gray-200 p-3 rounded-lg text-sm font-mono overflow-x-auto my-3" {...props} />
                ),
              a: ({node, ...props}) => (
                <a className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer" {...props} />
              ),
            }}
          >
            {result.content}
          </ReactMarkdown>
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