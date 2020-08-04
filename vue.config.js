const webpack = require("webpack");
const path = require('path');

module.exports = {
  devServer: {
    host: "localhost",
    port: 3001
  },
  configureWebpack: {
    resolve: {
      alias: {
        config: path.resolve(`src/config/${process.env.NODE_ENV}.js`)
      }
    },
    plugins: [
      new webpack.ProvidePlugin({
        $: "jquery",
        jquery: "jquery",
        "window.jQuery": "jquery",
        jQuery: "jquery"
      })
    ]
  }
};
