import { FiZap } from 'react-icons/fi';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-2">
            <FiZap className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">
              Content Generator
            </span>
          </div>
          <div className="text-sm text-gray-500">
            Powered by AI
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;