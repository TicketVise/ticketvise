module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  // darkMode: 'class',
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
      },
      fontFamily: {
        'ticketvise': ['Raleway', 'sans-serif']
      }
    }
  },
  variants: {
    extend: {}
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/typography')
  ]
}
