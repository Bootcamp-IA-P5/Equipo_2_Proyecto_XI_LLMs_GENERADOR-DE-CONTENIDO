export default function Footer() {
  return (
    <footer className="w-full bg-gradient-to-r from-purple-50 to-pink-50 border-t border-purple-100 py-6">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center">
          <p className="text-sm text-gray-600">
            © {new Date().getFullYear()} <span className="font-semibold text-purple-600">Content Generator AI</span> · Proyecto LLMs
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Generando contenido inteligente con IA ✨
          </p>
        </div>
      </div>
    </footer>
  );
}
