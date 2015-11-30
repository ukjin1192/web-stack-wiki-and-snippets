#### Install Webpack

~~~~
$ npm install webpack --global
~~~~


#### Install packages for example and create modules

~~~~
$ npm install lodash jquery --save
$ cd {PATH TO JS DIRECTORY}
$ vi module-foo.js

  'use strict';
  
  var _ = require('lodash');
  
  module.exports = function sumList() {
    return _.sum(arguments);
  };
  
$ vi module-bar.js

  'use strict';
  
  var $ = require('jquery');
  
  module.exports = function helloWorld() {
    $('#hello-world').html('Hello world');
  };
~~~~


#### Create entry file and template

~~~~
$ vi index.js

  'use strict'
  
  var foo = require('./foo');
  var bar = require('./bar');
  
  console.log(foo(1,2,3,4));
  bar();
  
$ vi index.html

  <!DOCTYPE html>
  <html>
  <body>
    <div id="hello-world"></div>
    <script type="text/javascript" src="{% static 'js/dist/vendor.bundle.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/dist/bundle.js' %}"></script>
  </body>
  </html>
~~~~


#### Create configuration file and bundle it

$ vi webpack.config.js

  'use strict';

  var webpack = require('webpack');
  
  module.exports = {
    entry: {
      bundle: './index.js',
      vendor: ['jquery', 'lodash'],
    },
    output: {
      path: './dist/',
      filename: '[name].js',
    },
    plugins: [
      new webpack.optimize.CommonsChunkPlugin(
        'vendor',
        'vendor.bundle.js'
      )
    ],
    resolve: {
      extensions: ['', '.js', '.es6']
    },
  };
  
$ webpack
~~~~
