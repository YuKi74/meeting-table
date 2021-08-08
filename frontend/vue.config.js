const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
module.exports = {
    css: {
        loaderOptions: {
            less: {
                lessOptions: {
                    // If you are using less-loader@5 please spread the lessOptions to options directly
                    modifyVars: {
                        'primary-color': '#ffcc5f',
                        'link-color': '#1DA57A',
                        'border-radius-base': '2px',
                        'btn-primary-color': '#212529',
                        'btn-danger-color': '#212529',
                        'btn-danger-bg': '#b4c8ff',
                    },
                    javascriptEnabled: true,
                },
            },
        },
    },
    configureWebpack: {
        plugins: [new MonacoWebpackPlugin()],
    },
};
