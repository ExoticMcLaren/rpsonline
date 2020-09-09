module.exports = {
  entry: {
    index: './src/index.js',
    game: './src/game.js'
  },
  output: {
    filename: '[name].js',
    path: __dirname + '/static/frontend'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};