#### Install npm

- Install `nodejs-legacy` to use `node` command instead of `nodejs`

~~~~
$ apt-get update
$ apt-get install nodejs npm nodejs-legacy
~~~~


#### npm command

~~~~
# Install packages with package.json
$ cd {PATH TO package.json}
$ npm install

# Install package globally
$ npm install {MODULE NAME}@{VERSION} --global

# Install package to run this application
$ npm install {MODULE NAME}@{VERSION} --save

# Install package for development purpose (e.g. unit test or minification)
$ npm install {MODULE NAME}@{VERSION} --save-dev

# Uninstall packaes - same with install command
$ npm uninstall {MODULE NAME}@{VERSION} --global
$ npm uninstall {MODULE NAME}@{VERSION} --save
$ npm uninstall {MODULE NAME}@{VERSION} --save-dev

# Check version of module
$ npm list {MODULE NAME}

# Check list of whole module
$ npm ls --depth=0
~~~~


#### Package management

- Initiate package management

~~~~
$ cd {PROJECT PATH}
$ npm init [Put information]
$ npm install --save lodash
~~~~

- Recommend to add `node_modules/` to `.gitignore`
- Example of `package.json`

~~~~
{
  "name": "mysite.com",
  "version": "0.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "BSD-2-Clause",
  "dependencies": {
    "lodash": "~3.10.1"
  }
}
~~~~


#### Node style programming example

~~~~
$ vi index.js

  'use strict';

  var _ = require('lodash');
  
  module.exports = function helloWorld() {
    _.times(10, function (index) {
      console.log('[' + index + '] hello world!');
    });
  };
  
$ vi test.js

  'use strict';
  
  var helloWorld = require('./');
  helloWorld();
  
$ node test.js
~~~~
