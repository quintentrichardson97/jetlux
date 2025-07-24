/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#fffbea',
          100: '#fdf2c1',
          200: '#fce69a',
          300: '#f9d66c',
          400: '#f6c646',
          500: '#f3b621',
          600: '#d59818',
          700: '#b87a10',
          800: '#9b5d0a',
          900: '#7b4506',
          950: '#402304',
        },
        dark: '#0c1421',
        charcoal: {
          50: '#f2f4f5',
          100: '#e5e7ea',
          200: '#ccd1d6',
          300: '#b3bcc2',
          400: '#7d838b',
          500: '#545c64',
          600: '#434a53',
          700: '#2c333c',
          800: '#1c222b',
          900: '#0c111a',
          950: '#05080e',
        },
        mist: '#f5f7f9',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Playfair Display', 'serif'],
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/postcss')],
}

