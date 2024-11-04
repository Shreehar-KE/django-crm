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
        primary: {
          '50': '#f2fbfa',
          '100': '#d2f5f2',
          '200': '#a5eae5',
          '300': '#70d8d3',
          '400': '#42bfbd',
          '500': '#2eb8b8',
          '600': '#1e8183',
          '700': '#1c6769',
          '800': '#1b5154',
          '900': '#1a4547',
          '950': '#09272a',
        },
      },
    },
  },
  plugins: [],
}

