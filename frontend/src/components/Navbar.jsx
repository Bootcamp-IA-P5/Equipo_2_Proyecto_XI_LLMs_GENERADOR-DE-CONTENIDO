export default function Nav() {
  return (
    <nav className="w-full bg-white shadow-sm px-8 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-linear-to-r from-purple-500 to-pink-500 flex items-center justify-center text-white text-xl">
          ✨
        </div>
        <div>
          <h1 className="text-xl font-bold text-gray-800">
            Generador de Contenido IA
          </h1>
          <p className="text-sm text-gray-500">
            Crea contenido con inteligencia artificial
          </p>
        </div>
      </div>
    </nav>
  );
}
