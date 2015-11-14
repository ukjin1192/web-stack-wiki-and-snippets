# Ubuntu basing settings

#### Install basic packages

~~~~
$ apt-get update
$ apt-get install build-essential git python-dev libxml2-dev libxslt1-dev python-pip
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

- Check {PUBLIC IP}:80 URL on browser


#### Install MySQL

~~~~
$ apt-get install mysql-server libmysqlclient-dev mysql-client-core-5.5 [Enter root password]
~~~~


#### Install PostgreSQL

~~~~
$ apt-get install libpq-dev build-dep python-psycopg2 postgresql postgresql-contrib [Enter password]
~~~~
