/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f7ff',
          100: '#ebf0ff',
          200: '#d6e0ff',
          300: '#b3c5ff',
          400: '#8da3ff',
          500: '#667eea',
          600: '#5568d3',
          700: '#4553b8',
          800: '#374199',
          900: '#2d3580',
        },
        secondary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#764ba2',
          600: '#65408a',
          700: '#553573',
          800: '#462b5d',
          900: '#38234a',
        },
      },
    },
  },
  plugins: [],
}

