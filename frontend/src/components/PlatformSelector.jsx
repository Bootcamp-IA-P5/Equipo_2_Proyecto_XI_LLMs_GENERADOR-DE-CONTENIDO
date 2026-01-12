import { FiFileText, FiTwitter, FiInstagram, FiLinkedin } from 'react-icons/fi';

const platformIcons = {
  blog: FiFileText,
  twitter: FiTwitter,
  instagram: FiInstagram,
  linkedin: FiLinkedin,
};

const platformColors = {
  blog: 'bg-purple-100 text-purple-600 border-purple-200',
  twitter: 'bg-blue-100 text-blue-500 border-blue-200',
  instagram: 'bg-pink-100 text-pink-600 border-pink-200',
  linkedin: 'bg-sky-100 text-sky-700 border-sky-200',
};

const PlatformSelector = ({ platforms, selected, onChange }) => {
  return (
    <div className="grid grid-cols-2 md: grid-cols-4 gap-3">
      {platforms?.map((platform) => {
        const Icon = platformIcons[platform.id] || FiFileText;
        const isSelected = selected === platform.id;
        const colors = platformColors[platform.id] || 'bg-gray-100 text-gray-600';
        
        return (
          <button
            key={platform.id}
            type="button"
            onClick={() => onChange(platform.id)}
            className={`
              p-4 rounded-lg border-2 transition-all duration-200 flex flex-col items-center gap-2
              ${isSelected 
                ? `${colors} border-current shadow-md scale-105` 
                : 'bg-white border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }
            `}
          >
            <Icon className={`h-6 w-6 ${isSelected ? '' : 'text-gray-400'}`} />
            <span className={`text-sm font-medium ${isSelected ? '' : 'text-gray-600'}`}>
              {platform.name}
            </span>
          </button>
        );
      })}
    </div>
  );
};

export default PlatformSelector;