import { useContentGenerator } from '../hooks/useContentGenerator';
import ContentForm from '../components/ContentForm';
import ContentResult from '../components/ContentResult';
import { FiLoader, FiZap } from 'react-icons/fi';

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
      <div className="flex items-center justify-center min-h-screen">
        <FiLoader className="h-8 w-8 animate-spin text-purple-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-50 via-pink-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-3">
            <FiZap className="h-8 w-8 text-purple-600" />
            <h1 className="text-4xl font-bold bg-linear-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Generador de Contenido con IA
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            Crea contenido optimizado para diferentes plataformas y audiencias
          </p>
        </div>

        {/* Main Content - Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Configuration Form */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg border border-purple-100 overflow-hidden">
              <div className="bg-linear-to-r from-purple-600 to-pink-600 p-6">
                <div className="flex items-center gap-2">
                  <FiZap className="h-6 w-6 text-white" />
                  <h2 className="text-2xl font-bold text-white">Configuración</h2>
                </div>
                <p className="text-purple-100 mt-2">
                  Personaliza tu contenido generado por IA
                </p>
              </div>
              <div className="p-6">
                <ContentForm
                  config={config}
                  onSubmit={generateContent}
                  loading={loading}
                />
              </div>
            </div>
          </div>

          {/* Right Column - Generated Content */}
          <div className="space-y-6">
            {result ? (
              <>
                <ContentResult 
                  result={result} 
                  onClear={clearResult}
                />
                
                {result.image_url && (
                  <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                      🎨 Imagen Generada
                    </h3>
                    <div className="rounded-xl overflow-hidden border border-gray-200">
                      <img 
                        src={result.image_url} 
                        alt="Contenido generado por IA" 
                        className="w-full h-auto object-cover"
                        loading="lazy"
                      />
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-12">
                <div className="text-center">
                  <div className="w-24 h-24 bg-linear-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <FiZap className="h-12 w-12 text-purple-600" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">
                    Comienza a crear
                  </h3>
                  <p className="text-gray-600 max-w-md mx-auto">
                    Completa el formulario de la izquierda y selecciona al menos una plataforma para generar contenido optimizado con IA
                  </p>
                  <div className="mt-8 grid grid-cols-2 gap-4 max-w-md mx-auto">
                    <div className="bg-purple-50 rounded-lg p-4 border border-purple-100">
                      <p className="text-purple-600 font-semibold">✓ Multi-plataforma</p>
                    </div>
                    <div className="bg-pink-50 rounded-lg p-4 border border-pink-100">
                      <p className="text-pink-600 font-semibold">✓ Personalizable</p>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
                      <p className="text-blue-600 font-semibold">✓ Varios modelos</p>
                    </div>
                    <div className="bg-orange-50 rounded-lg p-4 border border-orange-100">
                      <p className="text-orange-600 font-semibold">✓ Multi-idioma</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
