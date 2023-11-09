const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
require('dotenv').config({ path: '.env' });

const commonConfig = require('./webpack.common');
const { merge } = require('webpack-merge');
const packageJson = require('../package.json');

const debug = process.env.NODE_ENV !== 'production';

const plugins = [
  new ModuleFederationPlugin({
    name: 'uncoder',
    filename: 'remoteEntry.js',
    exposes: {
      './UncoderEditor': './src/pages/UncoderEditor/bootstrap',
    },
    shared: packageJson.dependencies,
  }),
];

const config = {
  devtool: debug ? 'source-map' : false,
  plugins,
};

module.exports = merge(commonConfig, config);
