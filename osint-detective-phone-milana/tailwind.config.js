/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'samsung-bg': '#09090b',
        'samsung-card': '#1c1c1e',
        'samsung-blue': '#3b82f6',
        'samsung-green': '#22c55e',
      },
      fontSize: {
        'xs': ['12px', '16px'],
        'sm': ['14px', '20px'],
        'base': ['16px', '24px'],
      },
      spacing: {
        '4.5': '1.125rem',
      },
    },
  },
  plugins: [],
}
