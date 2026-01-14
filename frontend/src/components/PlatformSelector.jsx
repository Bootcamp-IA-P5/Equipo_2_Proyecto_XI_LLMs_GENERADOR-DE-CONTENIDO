import { FiFileText, FiTwitter, FiInstagram, FiLinkedin } from 'react-icons/fi';

const platformIcons = {
  blog: FiFileText,
  twitter: FiTwitter,
  instagram: FiInstagram,
  linkedin: FiLinkedin,
};

const platformColors = {
  blog: 'bg-purple-500 text-white',
  twitter: 'bg-blue-400 text-white',
  instagram: 'bg-gradient-to-br from-purple-500 via-pink-500 to-orange-400 text-white',
  linkedin: 'bg-blue-600 text-white',
};

const platformHoverColors = {
  blog: 'hover:bg-purple-600',
  twitter: 'hover:bg-blue-500',
  instagram: 'hover:from-purple-600 hover:via-pink-600 hover:to-orange-500',
  linkedin: 'hover:bg-blue-700',
};

const PlatformSelector = ({ platforms, selected, onChange }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {platforms?.map((platform) => {
        const Icon = platformIcons[platform.id] || FiFileText;
        const isSelected = selected === platform.id;
        const colors = platformColors[platform.id] || 'bg-gray-500 text-white';
        const hoverColors = platformHoverColors[platform.id] || 'hover:bg-gray-600';
        
        return (
          <button
            key={platform.id}
            type="button"
            onClick={() => onChange(platform.id)}
            className={`
              p-4 rounded-xl transition-all duration-200 flex flex-col items-center gap-2 border-2
              ${isSelected 
                ? `${colors} border-transparent shadow-lg scale-105 ring-4 ring-purple-100` 
                : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-md text-gray-600'
              }
              ${!isSelected ? hoverColors : ''}
            `}
          >
            <Icon className="h-6 w-6" />
            <span className="text-sm font-semibold">
              {platform.name}
            </span>
          </button>
        );
      })}
    </div>
  );
};

export default PlatformSelector;