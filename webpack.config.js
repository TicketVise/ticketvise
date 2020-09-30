const TerserJSPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const autoprefixer = require('autoprefixer');
const tailwindcss = require('tailwindcss');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const path = require('path');
const purgecss = require('@fullhuman/postcss-purgecss')
const webpack = require("webpack");

module.exports = {
    entry: ['./frontend/index.js', './frontend/styles/index.scss'],
    output: {
        filename: 'bundle.js',
        chunkFilename: "[id]-[chunkhash].js",
        path: path.join(__dirname, './backend/ticketvise/static'),
        publicPath: '/static/'
    },
    devtool: 'source-map',
    devServer: {
        writeToDisk: true
    },
    optimization: {
        minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
        // splitChunks: {
        //     chunks: 'all',
        //     name: false,
        // },
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.(sa|sc|c)ss$/,
                exclude: ['/node_modules', '/dist', '/src/js', '/docs', '/src/docs'],
                loader: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: [
                                autoprefixer,
                                tailwindcss('./tailwind.config.js'),
                                purgecss(
                                    {
                                        content: ['./**/*.html', './**/*.vue'],
                                        defaultExtractor(content) {
                                            const contentWithoutStyleBlocks = content.replace(/<style[^]+?<\/style>/gi, '')
                                            return contentWithoutStyleBlocks.match(/[A-Za-z0-9-_/:]*[A-Za-z0-9-_/]+/g) || []
                                        },
                                        whitelist: [],
                                        whitelistPatterns: [
                                            /-(leave|enter|appear)(|-(to|from|active))$/,
                                            /^(?!(|.*?:)cursor-move).+-move$/,
                                            /^router-link(|-exact)-active$/,
                                            /data-v-.*/,
                                            // whitelist comment editor
                                            /^tui-.*/,
                                            /^CodeMirror/,
                                            /^cm-.*/,
                                            /^te/,
                                            /^code-.*/,
                                            /^hljs-.*/
                                        ],
                                    }
                                )
                            ],
                        }
                    },
                    'sass-loader'],
            },
            {
                test: /\.(ico|jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2)(\?.*)?$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[path][name].[ext]',
                    },
                },
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
                        loader: 'webpack-mjml-loader',
                        options: {
                            minify: process.env.NODE_ENV === "production"
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            SENTRY_DSN: JSON.stringify(process.env.SENTRY_DSN),
        }),
        new MiniCssExtractPlugin({
            filename: "styles.css",
            chunkFilename: '[id].css'
        }),
        new VueLoaderPlugin()
    ],
};
