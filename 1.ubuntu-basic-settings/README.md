# Ubuntu basing settings

#### Install basic packages

~~~~
$ apt-get update
$ apt-get install build-essential git python-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev libcurl4-openssl-dev python-pip curl sudo wget htop
$ pip install --upgrade pip
~~~~


#### Set timezone

~~~~
$ dpkg-reconfigure tzdata [Select city]
~~~~


#### Customize vim editor

~~~~
$ sudo apt-get install vim ctags cmake
$ vi ~/.vimrc
~~~~

- Copy and paste `.vimrc`

~~~~
$ mkdir -p ~/.vim/bundle
$ cd ~/.vim/bundle
$ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
$ vi [Ignore errors][:PluginInstall]
$ cd ~/.vim/bundle/YouCompleteMe
$ ./install.py
~~~~


#### Install zshell and oh-my-zshell

~~~~
$ sudo apt-get install zsh
$ chsh -s `which zsh`
~~~~

- Restart server
- Check default shell (`echo $SHELL`)

~~~~
$ curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
$ /bin/zsh
~~~~

- Append following codes

~~~~
$ vi ~/.zshrc

  setopt PROMPT_SUBST
  PROMPT='%(!.%F{red}.%F{cyan})%n%f@%F{yellow}%m%f%(!.%F{red}.)%} ➜ %{$(pwd|grep --color=always /)%${#PWD}G%} %{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[blue]%} % %{$reset_color%}'
  
$ source ~/.zshrc
~~~~


#### Install Fail2ban to protect from malicious attack

~~~~
$ sudo apt-get install fail2ban
$ cd /etc/fail2ban
$ cp jail.conf jail.local
$ vi jail.local
  
  [DEFAULT]
  ignoreip = {SAFE IP}

  [ssh]
  enabled = true
  
  [ssh-ddos]
  enabled = true
  destemail = {EMAIL ADDRESS}

$ sudo service fail2ban restart
~~~~


#### Configure git setting

~~~~
$ git config --global user.name {USERNAME}
$ git config --global user.email {EMAIL ADDRESS}
$ git config --global core.editor "vim"
~~~~


#### Install nginx *(Recommend version upper than 1.6)*

- Only for ubuntu <= 14.04

~~~~
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:nginx/stable [Enter]
~~~~

- Then,

~~~~
$ sudo apt-get update
$ sudo apt-get install nginx
$ nginx -v [Check version]
$ sudo service nginx start
~~~~

- Check URL `{PUBLIC IP}:80` on browser


#### Install MySQL

~~~~
$ sudo apt-get update
$ sudo apt-get install mysql-server mysql-client libmysqlclient-dev [Enter root password]
$ sudo service mysql start
~~~~


#### Install PostgreSQL

~~~~
$ sudo apt-get update
$ sudo apt-get install libpq-dev build-dep python-psycopg2 postgresql postgresql-contrib [Enter password]
$ sudo service postgresql start
~~~~


# Mac OS X basic settings

#### Customize terminal profile

- Download solarized theme at <a href="https://github.com/tomislav/osx-terminal.app-colors-solarized" target="_blank">here</a> (e.g. `Solarized Dark.terminal`)
- Open `Terminal` app
- Open `Profile` by press key `Command` + `,` 
- `Profile` tab > Click gear icon > import > `Solarized Dark.terminal` > Click theme > Set default


#### Optimize key input

- Open `terminal`

~~~~
# Enable key repeat
$ defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false
~~~~

- Download Karabiner from <a href="https://pqrs.org/osx/karabiner/" target="_blank">here</a>
- `Change Key` > `For PC Users`
- Check `Use PC Style Home/End` and `Use PC Style PageUp/PageDown`


#### Install brew

- Open `terminal`

~~~~
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
~~~~

- Put password
- Install some requirements

- Install use useful libraries

~~~~
$ brew install python cmake zsh vim
$ vi {Shell Configuration file}

  alias vi='/usr/local/bin/vim'
  alias vim='/usr/local/bin/vim'
~~~~


#### Install X-code command line developers tool

~~~~
$ xcode-select --install
~~~~
