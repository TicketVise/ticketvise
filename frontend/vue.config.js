module.exports = {
  chainWebpack: config => {
    config.module.rules.delete('eslint');
  },
  pwa: {
    name: 'TicketVise',
    themeColor: '#dd6b20',
    msTileColor: '#FFFFFF',
    manifestOptions: {
      background_color: '#FFFFFF'
    },
    manifestOptions: {
      icons: [
        {
            'src': 'favicon.ico',
            'sizes': '500x500',
            'type': 'image/ico',
        },
      ],
      iconPaths: {
        favicon32: null,
        favicon16: null,
        appleTouchIcon: null,
        maskIcon: null,
        msTileImage: null
      }
    },
    iconPaths: {
      favicon32: null,
      favicon16: null,
      appleTouchIcon: null,
      maskIcon: null,
      msTileImage: null
    }
  },
  devServer: {
    disableHostCheck: true
  }
}
