module.exports = {
    purge: [],
    theme: {
        extend: {
            colors: {
                'tv-blue-lightest': '#EEF8FC',
                'tv-blue-ligher': '#CAE7F6',
                'tv-blue-light': '#90B5D0',
                'tv-blue': '#5781A8',
                'tv-blue-dark': '#2F4C6F',
                'tv-blue-darker': '#061732',
                'tv-orange': '#FF6600',
                'tv-pink': '#FF1F4F',
            }
        },
        minWidth: {
            '0': '0',
            '1/4': '25%',
            '1/2': '50%',
            '3/4': '75%',
            'full': '100%',
        }
    },
    variants: {},
    plugins: [
        require('@tailwindcss/ui'),
    ],
};
