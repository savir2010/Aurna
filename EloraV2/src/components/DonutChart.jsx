import React from 'react';

const DonutChart = ({ percentage, size = 100, strokeWidth = 10, strokeColor = '#4CAF50', backgroundColor = '#e0e0e0' }) => {
  // Calculate the stroke offset based on the percentage
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeOffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex justify-center items-center">
      <svg
        width={size}
        height={size}
        className="transform rotate-90"
        viewBox={`0 0 ${size} ${size}`}
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={backgroundColor}
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Foreground circle for the progress */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeOffset}
          style={{ transition: 'stroke-dashoffset 1s ease' }} // Smooth animation for change in percentage
        />
      </svg>
      <div className="absolute text-lg font-bold text-gray-700">{percentage}%</div>
    </div>
  );
};

export default DonutChart;
