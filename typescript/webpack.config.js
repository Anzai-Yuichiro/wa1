const path = require('path');
const webpack = require('webpack');

module.exports = {
  mode: 'development',
  entry: './src/index.ts',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
    fallback: {
      "stream": require.resolve("stream-browserify"),
      "buffer": require.resolve("buffer/"),
      "process": require.resolve("process/browser"),
      "os": require.resolve("os-browserify/browser"),
      "path": require.resolve("path-browserify"),
      "querystring": require.resolve("querystring-es3"),
      "url": require.resolve("url/"),
      "crypto": require.resolve("crypto-browserify"),
      "util": require.resolve("util/"),
      "assert": require.resolve("assert/"),
      "vm": require.resolve("vm-browserify"),
      "http": require.resolve("stream-http"),
      "https": require.resolve("https-browserify"),
      "net": require.resolve("net-browserify"),
      "tls": require.resolve("tls-browserify"),
      "child_process": require.resolve("child_process-browserify")
    }
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'dist'),
    },
    compress: true,
    port: 9000,
  },
  plugins: [
    new webpack.ProvidePlugin({
      process: 'process/browser',
      Buffer: ['buffer', 'Buffer']
    })
  ]
};
