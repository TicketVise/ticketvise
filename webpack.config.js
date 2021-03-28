const path = require('path')
const { VueLoaderPlugin } = require('vue-loader')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

module.exports = {
  entry: './frontend/index.js',

  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, './backend/ticketvise/static')
  },

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },

  watchOptions: {
    ignored: /node_modules/
  },

  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          /* Creates `style` nodes from JS strings. */
          'style-loader',
          /* Translates CSS into CommonJS. */
          'css-loader',
          'postcss-loader',
          /* Compiles Sass to CSS. */
          'sass-loader'
        ]
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.mjml$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '../templates/email/[name].html',
              esModule: false,
            },
          },
          {
            loader: "extract-loader"
          },
          {
            loader: 'webpack-mjml-loader'
          }
        ]
      }
    ]
  },

  plugins: [
    new VueLoaderPlugin()
  ],

  optimization: {
    minimize: false,
    minimizer: [
      `...`,
      new BundleAnalyzerPlugin()
    ]
  }
}
