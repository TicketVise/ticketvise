module.exports = {
    purge: [
        './frontend/**/*.vue',
        './backend/ticketvise/templates/**/*.html'
    ],
    theme: {
        extend: {
            colors: {
                'tv-blue-lightest': '#EEF8FC',
                'tv-blue-ligher': '#CAE7F6',
                'tv-blue-light': '#90B5D0',
                'tv-blue': '#5781A8',
                'tv-blue-dark': '#2F4C6F',
                'tv-blue-darker': '#061732',
                'tv-orange': '#dd6b20',
                'primary': '#dd6b20',
                'tv-pink': '#FF1F4F'
            },
            fontSize: {
                '2xs': '.625rem'
            },
            minWidth: {
                '0': '0',
                '3': '0.75rem',
                '4': '1rem',
                '1/4': '25%',
                '1/2': '50%',
                '3/4': '75%',
                '3/5': '60%',
                'full': '100%',
                'side': '275px'
            },
            maxWidth: {
                'side': '275px'
            },
            width: {
                'side': '275px'
            }
        }
    },
    variants: {},
    plugins: [
        require('@tailwindcss/ui'),
        require('@tailwindcss/forms'),
    ],
};
