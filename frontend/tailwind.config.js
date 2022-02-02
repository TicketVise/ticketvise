const colors = require('tailwindcss/colors')

module.exports = {
  mode: 'jit',
  purge: { content: ['./public/**/*.html', './src/**/*.vue'] },
  darkMode: false, // 'class'
  theme: {
    extend: {
      colors: {
        'primary-50': '#FFF7ED',
        'primary-100': '#FFEDD5',
        'primary-200': '#FED7AA',
        'primary-300': '#FDBA74',
        'primary-400': '#E17730',
        'primary': '#dd6b20',
        'primary-500': '#dd6b20',
        'primary-600': '#CF651E',
        'primary-700': '#BF5D1B',
        sky: colors.sky,
        teal: colors.teal,
        cyan: colors.cyan,
        rose: colors.rose,
        sky: colors.sky
      },
      fontFamily: {
        'ticketvise': ['Raleway', 'sans-serif']
      },
      width: {
        '22': '5.5rem'
      }
    }
  },
  variants: {
    extend: {}
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio')
  ]
}
