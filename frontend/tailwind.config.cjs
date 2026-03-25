/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        slateblue: '#1E293B',
        mint: '#10B981',
        amber: '#F59E0B',
        rose: '#F43F5E',
        cream: '#F8FAFC'
      },
      fontFamily: {
        heading: ['\"Atkinson Hyperlegible\"', 'sans-serif'],
        body: ['\"Manrope\"', 'sans-serif']
      }
    }
  },
  plugins: []
};
