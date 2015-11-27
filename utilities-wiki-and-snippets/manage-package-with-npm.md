#### Install npm

~~~~
$ apt-get update
$ apt-get install nodejs npm nodejs-legacy
~~~~


#### npm command

~~~~
# Install
$ npm install {MODULE NAME}@{VERSION} [option]
  -g : Install package globally
  --save : Install package to run this application 
  --save-dev : Development purpose like unit test or minification

# Remove
$ npm remove {MODULE NAME}

# Check version of module
$ npm list {MODULE NAME}

# Check list of whole module
$ npm ls --depth=0
~~~~
