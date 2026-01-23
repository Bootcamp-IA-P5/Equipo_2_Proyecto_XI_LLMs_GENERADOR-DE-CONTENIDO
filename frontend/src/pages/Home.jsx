import { useContentGenerator } from '../hooks/useContentGenerator';
import ContentForm from '../components/ContentForm';
import ContentResult from '../components/ContentResult';
import GeneratingModal from '../components/GeneratingModal';
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

  /* CARGA CONFIG INICIAL */
  if (configLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <FiLoader className="h-8 w-8 animate-spin text-purple-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-50 via-pink-50 to-blue-50 relative">

      {/* 🔥 MODAL DE CARGA (SOLO FRONT) */}
      {loading && <GeneratingModal show={loading} />}

      <div className="max-w-[1400px] mx-auto px-4 py-6 flex flex-col gap-6">

        {/* HEADER */}
        <header className="text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <FiZap className="h-7 w-7 text-purple-600" />
            <h1 className="text-3xl font-bold bg-linear-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Generador de Contenido con IA
            </h1>
          </div>
          <p className="text-gray-600 text-sm">
            Crea contenido optimizado para diferentes plataformas y audiencias
          </p>
        </header>

        {/* CONFIGURACIÓN */}
        <section className="bg-white rounded-2xl shadow-xl border border-purple-100">
          <div className="bg-linear-to-r from-purple-600 to-pink-600 px-6 py-4 rounded-t-2xl">
            <div className="flex items-center gap-2">
              <FiZap className="h-5 w-5 text-white" />
              <h2 className="text-lg font-bold text-white">
                Configuración
              </h2>
            </div>
            <p className="text-purple-100 text-sm mt-1">
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
        </section>

        {/* RESULTADO / PREVIEW */}
        <section className="bg-white rounded-2xl shadow-lg border border-purple-100 p-6 min-h-[260px]">
          {result ? (
            <>
              <ContentResult 
                result={result} 
                onClear={clearResult}
              />

              {result.image_url && (
                <div className="mt-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
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
            /* 🔥 ESTA PARTE SE QUEDA TAL CUAL 🔥 */
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="w-20 h-20 bg-linear-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiZap className="h-10 w-10 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Comienza a crear
                </h3>
                <p className="text-gray-600 max-w-md mx-auto">
                  Completa la configuración superior para generar contenido con IA
                </p>

                <div className="mt-6 grid grid-cols-2 gap-3 max-w-md mx-auto text-sm">
                  <span className="bg-purple-50 border border-purple-100 rounded-lg py-2 text-purple-600 font-medium">
                    ✓ Multi-plataforma
                  </span>
                  <span className="bg-pink-50 border border-pink-100 rounded-lg py-2 text-pink-600 font-medium">
                    ✓ Personalizable
                  </span>
                  <span className="bg-blue-50 border border-blue-100 rounded-lg py-2 text-blue-600 font-medium">
                    ✓ Varios modelos
                  </span>
                  <span className="bg-orange-50 border border-orange-100 rounded-lg py-2 text-orange-600 font-medium">
                    ✓ Multi-idioma
                  </span>
                </div>
              </div>
            </div>
          )}
        </section>

      </div>
    </div>
  );
};

export default Home;
