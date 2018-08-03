const webpack = require ('webpack');

const config = {
  entry : __dirname + '/js/index.jsx',
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css', '.min']
  },
  module: {
    rules: [
      {
        test: /\.min?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.js?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  }
};

module.exports = config;
