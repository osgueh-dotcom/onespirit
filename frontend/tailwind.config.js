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
            DEFAULT: '#F1592A',
            light: '#F7941E',
            dark: '#D9471C',
            soft: '#FDE6DC',
            pastel: '#FFF7F3'
          },
          amber: {
            DEFAULT: '#F7941E',
            soft: '#FFF1D8'
          },
          yellow: {
            DEFAULT: '#F5EE31',
            soft: '#FFFDE8'
          },
          charcoal: {
            DEFAULT: '#172033',
            light: '#334155',
            dark: '#0F172A',
            gray: '#64748B'
          },
          blue: {
            DEFAULT: '#0EA5E9',
            light: '#38BDF8',
            dark: '#0369A1'
          },
          emerald: {
            DEFAULT: '#10B981',
            light: '#34D399',
            dark: '#047857'
          }
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        card: '0 12px 32px -24px rgba(15, 23, 42, 0.35)',
        'card-hover': '0 18px 44px -28px rgba(241, 89, 42, 0.42)'
      }
    },
  },
  plugins: [],
}
