const webpack = require('webpack');
const path = require("path");
const miniCss = require('mini-css-extract-plugin');
const dotenv = require('dotenv')

dotenv.config();

module.exports = {
    entry: "./src/index.js",
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            "@babel/preset-env",
                            "@babel/preset-react"
                        ]
                    }
                },
                exclude: /node_modules/,

            },
            {
                test: /\.(s*)css$/,
                use: [
                    miniCss.loader,
                    'css-loader',
                    'sass-loader',
                ]
            }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': JSON.stringify(process.env)
        }),
        new miniCss({
            filename: 'style.css',
        })
    ],
    resolve: {
        extensions: [".jsx", ".js"],
    },
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "bundle.js"
    },
    devServer: {
        static: path.join(__dirname, "dist"),
        compress: true,
        port: 9000
    }
};
