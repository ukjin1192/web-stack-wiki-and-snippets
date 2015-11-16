# Ubuntu basing settings

#### Install basic packages

~~~~
$ apt-get update
$ apt-get install build-essential git python-dev libxml2-dev libxslt1-dev python-pip curl
~~~~


#### Set timezone

~~~~
$ dpkg-reconfigure tzdata [Select city]
~~~~


#### Customize vim editor

~~~~
$ apt-get install vim ctags cmake
$ vi ~/.vimrc
~~~~

- Copy and paste vimrc

~~~~
$ mkdir -p ~/.vim/bundle
$ cd ~/.vim/bundle
$ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
$ vim [:PluginInstall]
$ cd ~/.vim/bundle/YouCompleteMe
$ ./install.sh
~~~~


#### Install zshell and oh-my-zshell

~~~~
$ apt-get install zsh
$ chsh -s `which zsh`
~~~~

- Restart server
- Check default shell (`echo $SHELL`)

~~~~
$ curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
~~~~


#### Install Fail2ban to protect from malicious attack

~~~~
$ apt-get install fail2ban
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

$ service fail2ban restart
~~~~


#### Configure git setting

~~~~
$ git config --global user.name {USERNAME}
$ git config --global user.email {EMAIL ADDRESS}
$ git commit --amend --reset-author
~~~~


#### Install nginx *(Recommend version upper than 1.6)*

~~~~
$ add-apt-repository ppa:nginx/stable [Enter]
$ apt-get update
$ apt-get install nginx
~~~~

- Check URL `{PUBLIC IP}:80` on browser


#### Install MySQL

~~~~
$ apt-get install mysql-server libmysqlclient-dev mysql-client-core-5.5 [Enter root password]
~~~~


#### Install PostgreSQL

~~~~
$ apt-get install libpq-dev build-dep python-psycopg2 postgresql postgresql-contrib [Enter password]
~~~~



# For Mac OS X

#### Customize terminal profile *(Mac OS X only)*

- Download solarized theme at <a href="https://github.com/tomislav/osx-terminal.app-colors-solarized" target="_blank">here</a> (e.g. `Solarized Dark.terminal`)
- Open `Terminal` app
- Open `Profile` by press key `Command` + `,` 
- Click `settings` and import `.terminal` file


#### Install brew

- Open `terminal`

~~~~
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
~~~~

- Put password
- Install some requirements


#### Install zshell and oh-my-zshell

~~~~
$ brew update
$ brew install zsh
$ command -v zsh | sudo tee -a /etc/shells
~~~~

- Put password

~~~~
$ chsh -s `which zsh`
~~~~

- Put password
- Check default shell (`echo $SHELL`)

~~~~
$ curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
~~~~

- Restart `terminal`
