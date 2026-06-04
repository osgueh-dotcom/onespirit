/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          orange: {
            DEFAULT: '#FF6B35',
            light: '#FF8A5C',
            dark: '#E04A15',
            soft: '#F7C59F',
            pastel: '#FFF3EB'
          },
          charcoal: {
            DEFAULT: '#1A1D20',
            light: '#2D3136',
            dark: '#111315',
            gray: '#6B7280'
          },
          blue: {
            DEFAULT: '#00A8E8',
            light: '#33BAEC',
            dark: '#0083B6'
          },
          emerald: {
            DEFAULT: '#2EC4B6',
            light: '#56D0C5',
            dark: '#20A89C'
          }
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
