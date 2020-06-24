module.exports = {
  chainWebpack: config => {
    config.module.rules.delete('eslint');
},

  publicPath: "/",
  devServer: {
    proxy: {
      "/api": {
        target: "http://i02b207.p.ssafy.io:8083/"
      }
    }
  },
  transpileDependencies: ["vuetify"]
};
