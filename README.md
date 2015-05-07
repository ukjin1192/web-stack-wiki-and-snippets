<h1>Tutorial : Sample Django Project</h1>

django snippets and setting tutorial

- Based on Amazon Web Service
  - EC2 (OS: ubuntu 14.04 LTS)
  - ELB (Load balancing)
  - RDS (DB: MySQL or PostgreSQL)
  - Route 53 (Domain)

- Stack
  - Nginx 1.6
  - uWSGI
  - Django 1.7
  - redis (In-Memory DB)
  - Celery (for Async and Cron task)
  - Compressor (Compress static files)
  - Fabric (for Deployment)
  - Pillow (for Image processing)

<i>Note that I didn't use virtualenv with assumption `1 service in 1 instance`</i>

- Django examples
  - Localization
  - Send mail
  - Upload image
  - Send requests to another server
  - HMAC

<h2>EC2 Instance</h2>

1. Create EC2 instance
2. Set security group as following (Inbound value)
3. Connect to terminal with PEM file

Type | Protocol | Port | Source
-----|----------|------|-------
SSH | TCP | 22 | 0.0.0.0/0 (or Your IP)
HTTP | TCP | 80 | 0.0.0.0/0 (for nginx)
HTTPS | TCP | 443 | 0.0.0.0/0 (for nginx)
Custom TCP Rule | TCP | 8000 | 0.0.0.0/0 (for test)

<h4>Checkout to root</h4>

    ubuntu $ sudo su

<h4>Basic setting</h4>

    root $ apt-get update
    root $ apt-get install build-essential git python-dev libxml2-dev libxslt1-dev python-pip

<h4>Set Timezone</h4>

    root $ dpkg-reconfigure tzdata [Select city]

<h4>Customize Vim</h4>

    root $ apt-get install vim ctags cmake
    root $ vi ~/.vimrc
    - Copy and paste vimrc
    
    root $ mkdir -p ~/.vim/bundle
    root $ cd ~/.vim/bundle
    root $ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
    root $ vim [:PluginInstall]
    root $ cd ~/.vim/bundle/YouCompleteMe
    root $ ./install.sh

<h4>Clone sample django project if exist</h4>

    root $ ssh-keygen
    - Add public key(id_rsa.pub) to Github or Bitbucket
    
    root $ mkdir -p /var/www/
    root $ cd /var/www/
    root $ git clone {GIT REMOTE ORIGIN URL}
    root $ mv {PROJECT NAME}/ {DOMAIN NAME}

<h4>Git setting</h4>

    root $ git config --global user.name {USERNAME}
    root $ git config --global user.email {EMAIL ADDRESS}
    root $ git commit --amend --reset-author

<h4>Install django and helpful packages</h4>

    root $ pip install fabric django==1.7.7 django-debug-toolbar django-suit django-compressor httplib2
    root $ cd {PROJECT PATH} (=/var/www/{DOMAIN NAME})
    root $ ./manage.py migrate
    root $ ./manage.py collectstatic --noinput

<h4>Check on test server</h4>

    root $ ./manage.py runserver 0.0.0.0:8000
    - Check on browser URL {PUBLIC IP}:8000

<h4>Compressor setting</h4>

    root $ vi {PROJECT PATH}/{PROJECT NAME}/settings/prod.py
    
      COMPRESS_ENABLED = True
      COMPRESS_URL = STATIC_URL
      COMPRESS_ROOT = STATIC_ROOT
      COMPRESS_OUTPUT_DIR = 'CACHE'
      COMPRESS_REBUILD_TIMEOUT = 60 * 60 * 24 * 7
      COMPRESS_OFFLINE = False
      STATICFILES_FINDERS += (
        'compressor.finders.CompressorFinder',
      )

<h4>Install Nginx (Upper than version 1.6 required)</h4>

    root $ add-apt-repository ppa:nginx/stable [Enter]
    root $ apt-get update
    root $ apt-get install nginx
    - Check on browser URL {PUBLIC IP}:80

<h4>Install uWSGI</h4>

    root $ pip install uwsgi

<h4>Nginx and uWSGI setting</h4>

    - Edit following files to customize
      {PROJECT PATH}/conf/nginx/{PROJECT NAME}.conf
      {PROJECT PATH}/conf/uwsgi/{PROJECT NAME}.ini
    
    root $ rm /etc/nginx/nginx.conf
    root $ ln -s {PROJECT PATH}/conf/nginx/nginx.conf /etc/nginx/
    root $ ln -s {PROJECT PATH}/conf/nginx/{PROJECT NAME}.conf /etc/nginx/sites-enabled/
    root $ ln -s {PROJECT PATH}/conf/uwsgi/uwsgi.conf /etc/init/
    root $ mkdir -p /etc/uwsgi/vassals/
    root $ ln -s {PROJECT PATH}/conf/uwsgi/{PROJECT NAME}.ini /etc/uwsgi/vassals/
    root $ cd {PROJECT PATH}/logs/
    root $ chown www-data.www-data uwsgi.log uwsgi.pid

<h4>Start Nginx and uWSGI</h4>

    root $ service nginx restart
    root $ uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term

<h4>Install PostgreSQL (or MySQL below)</h4>

    root $ apt-get install libpq-dev build-dep python-psycopg2 postgresql postgresql-contrib
    root $ pip install psycopg2 
    root $ sudo su - postgres
    
    postgresql $ createdb {DB NAME}
    postgresql $ createuser -P {USERNAME} [enter password]
    postgresql $ exit
    
    root $ vi {PROJECT PATH}/{PROJECT NAME}/settings/prod.py
    
      DATABASES = {
        'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': '{DB NAME}',
          'USER': 'root',
          'PASSWORD': '{PASSWORD}',
          'HOST': '127.0.0.1',
          'PORT': '5432',
        }
      }
      
    root $ ./manage.py migrate

<h4>Install MySQL (or PostgreSQL above)</h4>

    root $ apt-get install mysql-server libmysqlclient-dev [enter root password]
    root $ pip install MySQL-python
    root $ vi /etc/mysql/my.cnf
    - Add configuration from {PROJECT PATH}/conf/mysql/my.cnf
    
    root $ chmod 600 /etc/mysql/my.cnf
    root $ service mysql restart
    root $ mysql -u root
    
    mysql $ CREATE DATABASE {DB NAME} DEFAULT CHARACTER SET utf8;

<h4>When schema changed</h4>

    root $ ./manage.py makemigrations {APP NAME}
    root $ ./manage.py migrate {APP NAME}

<h4>Install redis</h4>

    root $ apt-get install redis-server
    root $ pip install redis django-redis django-redisboard
    root $ vi {PROJECT PATH}/{PROJECT NAME}/settings/prod.py
    
      INSTALLED_APPS += (
        'redisboard',
      )
      
      CACHES = {
        'default': {
          'BACKEND': 'django_redis.cache.RedisCache',
          'LOCATION': 'redis://127.0.0.1:6379/1',
          'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
          }
        }
      }
      
    root $ ./manage.py collectstatic --noinput

<h4>Use redis in controller</h4>

    root $ vi {PROJECT PATH}/{PROJECT NAME}/apps/{APP NAME}/views.py
    
      from django.core.cache import cache
      from django_redis import get_redis_connection
      
      con = get_redis_connection('default')

      cache.set('foo', 'bar', timeout=10) # Create cache
      cache.get('foo')                    # Retrieve cache value
      con.expire(':1:foo', 100)           # Extend cache TTL
      cache.delete('foo')                 # Delete cache

<h4>Redis command</h4>

    root $ redis-server			    # Start redis
    root $ redis-cli save		    # Save redis memory DB
    root $ redis-cli flushall	  # Flush redis memory DB
    root $ redis-cli shutdown	  # Shutdown redis

<h4>Install Celery</h4>

    root $ apt-get install rabbitmq-server
    root $ pip install celery django-celery amqp
    root $ vi {PROJECT PATH}/{PROJECT NAME}/settings/prod.py
    
      import djcelery
      
      INSTALLED_APPS += (
        'djcelery',
      )
      
      djcelery.setup_loader()
      
      BROKER_URL = 'amqp://guest:guest@localhost:5672/'
      CELERYD_PREFETCH_MULTIPLIER = {More time-consuming tasks, More closer to number 1}
      CELERYD_CONCURRENCY = {Default : Number of CPU cores}
    
    root $ vi {PROJECT PATH}/{PROJECT NAME}/wsgi.py	
    
      import djcelery
      
      djcelery.setup_loader()

<h4>Use Celery in controller</h4>

    root $ vi {PROJECT PATH}/{PROJECT NAME}/apps/utils/tasks.py
    
      from celery import task
      
      @task()
      def sample_async_task(*args):
        return None
      
    root $ vi {PROJECT PATH}/{PROJECT NAME}/apps/{APP NAME}/views.py
      
      from utils.tasks import sample_async_task
        
      sample_async_task.apply_async(args=["foo"], countdown=1)

<h4>Celery command</h4>

    root $ cd {PROJECT PATH}
    root $ ./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid   # Start celery worker
    root $ ./manage.py celery worker --loglevel=debug   # Start celeryt worker with debug mode 
    root $ ./manage.py celeryctl purge                  # Flush celery tasks
    root $ ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15   # Stop celery worker
    
    - Enroll tasks at Admin > Djcelery > Periodic tasks
    root $ ./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach   # Start celery beat (cron task)
    root $ ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15   # Stop celery beat

<h4>Localization</h4>
  
    root $ vi {PROJECT PATH}/{PROJECT NAME}/settings/prod.py
    
      ...
      LANGUAGE_CODE = 'ko-kr'
      ugettext = lambda s: s
      LANGUAGES = (
        ('ko', ugettext('Korean')),
        ('en', ugettext('English')),
      )
      LOCALE_PATHS = (
        ABS_PATH('locale'),     # /var/www/mysite.com/locale
      )
      USE_I18N = True
      USE_L10N = True
      ...
      MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
      )
      # TEMPLATE_CONTEXT_PROCESSORS have django.core.context_processors.i18n as default
      
    root $ vi {PROJECT PATH}/{PROJECT NAME}/templates/test.html
    
      {% load i18n %}
      ...
      {% trans "안녕" %}
      ...
    
    root $ sudo apt-get install gettext
    root $ mkdir {PROJECT PATH}/locale
    
    # Case of Template translation
    root $ django-admin.py makemessages -l {LOCALE NAME}
    
    # Case of Javascript translation
    root $ django-admin.py makemessages -d djangojs -l {LOCALE NAME}
    
    root $ vi {PROJECT PATH}/locale/{LOCALE NAME}/LC_MESSAGES/django.po
    
      msgid "안녕"
      msgstr "Hello"
    
    root $ django-admin.py compilemessages

<h4>Pillow setting</h4>

    root $ apt-get install imagemagick libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev
    
    # 32bit : i386-linux-gnu, 64bit : x86_64-linux-gnu
    root $ ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib 
    root $ ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib 
    root $ ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib 
	
    # Only for ubuntu 14.04 LTS version 
    root $ ln -s /usr/include/freetype2 /usr/include/freetype 
    root $ pip install pillow
    - Check available list

<h4>Use Pillow in controller</h4>

    root $ vi {PROJECT PATH}/{PROJECT NAME}/apps/utils/utilities.py
    
      from PIL import Image as ImageObj
      from PIL import ImageOps
      import os
      import StringIO
      import urllib

<h4>When CPU Core or Memery Size changed</h4>
	
    # Nginx
      worker_processes = {NUMBER OF CORE}
      worker_connections = {MEMORY SIZE}
      
    # MySQL
      innodb_buffer_pool_size = {MEMORY SIZE} * 0.5
      innodb_log_file_size = {innodb_buffer_pool_size} * 0.15
      
    # Celery
      CELERYD_CONCURRENCY = {NUMBER OF CORE}

<h2>ELB instance</h2>

1. Create Load Balancer
  - Set "/health_check" as 'Ping Path' value at Health Check Configuration
2. Change nginx configuration

    server {
      ...
      location /health_check {
        access_log off;
        return 200;
      }
      ...
    }

<h2>RDS instance</h2>

1. Create RDS
2. Connect RDS with django application server

<h2>Route 53</h2>

1. Create hosted zone
2. Create record set

Type | Alias | Alias Target
-----|-------|-------------
A | Yes | {ELB A RECORD}

<h2>Django examples</h2>

