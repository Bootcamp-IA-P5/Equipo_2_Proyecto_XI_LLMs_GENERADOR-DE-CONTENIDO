import { useContentGenerator } from '../hooks/useContentGenerator';
import ContentForm from '../components/ContentForm';
import ContentResult from '../components/ContentResult';
import { FiLoader } from 'react-icons/fi';

const Home = () => {
  const { 
    config, 
    configLoading, 
    loading, 
    result, 
    generateContent, 
    clearResult 
  } = useContentGenerator();

  if (configLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <FiLoader className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🚀 Generador de Contenido con IA
        </h1>
        <p className="text-gray-600">
          Crea contenido optimizado para diferentes plataformas y audiencias
        </p>
      </div>

      {/* Main Content */}
      <div className="grid gap-8">
        {/* Form Card */}
        <div className="card bg-white p-6 rounded-lg shadow-sm">
          <ContentForm
            config={config}
            onSubmit={generateContent}
            loading={loading}
          />
        </div>

        {/* Result & Image Section */}
        {result && (
          <div className="space-y-6">
            <ContentResult 
              result={result} 
              onClear={clearResult}
            />
            
            {result.image_url && (
              <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                <h3 className="text-lg font-medium text-gray-800 mb-3">
                  🎨 Imagen Sugerida
                </h3>
                <div className="flex justify-center bg-gray-50 rounded-lg p-2">
                  <img 
                    src={result.image_url} 
                    alt="Contenido generado por IA" 
                    className="rounded-lg shadow-md max-w-full h-auto object-cover max-h-[500px]"
                    loading="lazy"
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
