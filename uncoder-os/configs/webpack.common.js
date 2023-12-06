require('dotenv').config({ path: '.env' });

const debug = process.env.NODE_ENV !== 'production';
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const Dotenv = require('dotenv-webpack');
const NodePolyfillPlugin = require('node-polyfill-webpack-plugin');

const rules = [
  {
    test: /\.(js|jsx)$/,
    exclude: /node_modules/,
    use: ['babel-loader'],
  },
  {
    test: /\.(ts|tsx)?$/,
    use: ['babel-loader', {
      loader: 'ts-loader',
      options: {
        onlyCompileBundledFiles: true,
      },
    }],
    exclude: [/node_modules/, /workers/],
  },
  {
    test: /\.worker\.ts$/,
    use: [
      {
        loader: 'worker-loader',
        options: {
          inline: 'no-fallback',
        },
      },
      'babel-loader',
      {
        loader: 'ts-loader',
        options: {
          onlyCompileBundledFiles: true,
        },
      }],
    exclude: [/node_modules/],
  },
  {
    test: /\.svg$/,
    issuer: /\.[jt]sx?$/,
    use: [{
      loader: '@svgr/webpack',
      options: {
        exportType: 'named',
      },
    }],
  },
  {
    test: /\.(css)$/,
    use: [(debug ? 'style-loader' : MiniCssExtractPlugin.loader), 'css-loader'],
  },
  {
    test: /\.(sass)?$/,
    use: [(debug
      ? 'style-loader'
      : MiniCssExtractPlugin.loader),
    {
      loader: 'css-loader',
      options: {
        url: true,
      },
    },
    {
      loader: 'postcss-loader',
      options: {
        postcssOptions: {
          plugins: [
            [
              'postcss-inline-base64',
              {
                baseDir: './src/assets',
              },
            ],
          ],
        },
      },
    },
    {
      loader: 'sass-loader',
    },
    ],
  },
];

if (debug) {
  rules.unshift({
    test: /\.(ts|tsx)?$/,
    enforce: 'pre',
    use: ['source-map-loader'],
  });
}

const plugins = [
  new Dotenv({
    systemvars: true,
  }),
  new NodePolyfillPlugin(),
];
if (!debug) {
  plugins.push(new MiniCssExtractPlugin({
    filename: 'style.css',
  }));
}

module.exports = {
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  module: {
    rules,
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  plugins,
};
