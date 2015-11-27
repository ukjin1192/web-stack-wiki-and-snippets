#### Install npm

- Install `nodejs-legacy` to use `node` command instead of `nodejs`

~~~~
$ apt-get update
$ apt-get install nodejs npm nodejs-legacy
~~~~


#### npm command

- npm option
  - --global : Install package globally
  - --save : Install package to run this application 
  - --save-dev : Development purpose like unit test or minification

~~~~
# Install
$ npm install {MODULE NAME}@{VERSION} [option]

# Remove
$ npm remove {MODULE NAME}

# Check version of module
$ npm list {MODULE NAME}

# Check list of whole module
$ npm ls --depth=0
~~~~
