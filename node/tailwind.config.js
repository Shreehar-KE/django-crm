/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../templates/*.html',
    '../**/templates/**/*.html',
    '../**/forms.py'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2eb8b8',
        primary_dark: '#196767',
        primary_light: '#6fdcdc',
      },
    },
  },
  plugins: [],
}

