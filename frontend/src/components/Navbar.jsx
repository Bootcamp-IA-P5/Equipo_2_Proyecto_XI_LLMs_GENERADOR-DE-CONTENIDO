import { FiZap } from 'react-icons/fi';

export default function Nav() {
  return (
    <nav className="w-full bg-white border-b border-purple-100 px-2 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-linear-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
            <FiZap className="text-white text-2xl" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-linear-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Content Generator
            </h1>
            <p className="text-sm text-gray-500">
              Powered by AI
            </p>
          </div>
        </div>
        <div className="hidden md:flex items-center gap-2">
          <span className="text-xs font-semibold text-purple-600 bg-purple-50 px-3 py-1.5 rounded-full border border-purple-200">
            ✨ AI Powered
          </span>
        </div>
      </div>
    </nav>
  );
}
