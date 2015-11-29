#### Install Webpack

~~~~
$ npm install webpack --global
~~~~


#### Create configuration file and bundle it

~~~~
$ cd {PATH TO JS DIRECTORY}
$ vi webpack.config.js

  'use strict';

  var _ = require('lodash');
  var pkg = require('{PROJECT PATH}/package.json');
  
  module.exports = {
    entry: {
      'index': './raw/index.js'
    },
    output: {
      path: 'dist/',
      filename: '[name].js',
      library: 'MySiteLib',
      libraryTarget: 'umd'
    }
  };
  
$ vi {PROJECT PATH}/package.json

  ...
  "main": "{PATH TO JS DIRECTORY}/dist/index.js",
  ...
  
$ webpack
~~~~


#### Use module at browser

~~~~
$ vi index.html

  <script type="text/javascript" src="{% static 'js/dist/index.js' %}"></script>
  <script type="text/javascript">MySiteLib();</script>
~~~~
