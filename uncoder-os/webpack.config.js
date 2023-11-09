const path = require('path');
require('dotenv').config({ path: '.env' });
const commonConfig = require('./configs/webpack.common');
const { merge } = require('webpack-merge');

const HtmlWebpackPlugin = require('html-webpack-plugin');

const debug = process.env.NODE_ENV !== 'production';

const plugins = [
  new HtmlWebpackPlugin({
    template: path.resolve(__dirname, 'src', 'index.html'),
    favicon: path.resolve(__dirname, 'src/assets/images', 'favicon.svg'),
    publicPath: '/',
    filename: 'index.html',
  }),
];

const outputConfig = {
  path: path.resolve(__dirname, 'build/'),
  filename: '[name].bundle.js',
  publicPath: '/',
  clean: true,
  sourceMapFilename: '[file].map',
};

const config = {
  devtool: debug ? 'source-map' : false,
  entry: path.resolve(__dirname, 'src', 'index.tsx'),
  output: outputConfig,
  devServer: {
    allowedHosts: 'all',
    open: true,
    hot: true,
    host: '0.0.0.0',
    port: 4010,
    historyApiFallback: true,
    static: {
      directory: path.join(__dirname, 'build'),
    },
  },
  plugins,
};

module.exports = merge(commonConfig, config);
