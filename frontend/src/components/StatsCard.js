import React from 'react';

const StatsCard = ({ title, value, icon, color = 'primary' }) => {
  const colorClasses = {
    primary: 'from-primary-500 to-primary-600',
    secondary: 'from-secondary-500 to-secondary-600',
    accent: 'from-purple-500 to-pink-600',
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition fade-in">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-800">{value}</p>
        </div>
        <div
          className={`w-16 h-16 rounded-full bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center text-3xl shadow-lg`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatsCard;

