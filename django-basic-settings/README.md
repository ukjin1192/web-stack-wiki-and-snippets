# Django basic settings

#### Install django and helpful packages

~~~~
$ pip install django django-debug-toolbar httplib2
$ django-admin startproject {PROJECT NAME}
$ cd {PROJECT PATH}
$ ./manage.py migrate
$ ./manage.py runserver 0.0.0.0:8000
~~~~

- Check URL `{PUBLIC IP}:8000` on browser


#### Clone sample django project if exist

~~~~
$ ssh-keygen
$ cat ~/.ssh/id_rsa.pub
~~~~

- Add public key to Github or Bitbucket

~~~~
$ mkdir -p /var/www/
$ cd /var/www/
$ git clone {GIT REMOTE ORIGIN URL}
~~~~

- Install pip requirements

~~~~
$ pip install -r {PATH TO PIP REQUIREMENTS}/requirements.txt
~~~~


#### Connect with MySQL

~~~~
$ pip install MySQL-python
$ service mysql restart
$ mysql -u root -p [Enter password]
mysql $ CREATE DATABASE {DB NAME} DEFAULT CHARACTER SET utf8;
mysql $ exit;
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': '{DB NAME}',
      'USER': 'root',
      'PASSWORD': '{MySQL ROOT PASSWORD}',
      'HOST': '',
      'PORT': '',
      'DEFAULT-CHARACTER-SET': 'utf8',
    },
  }
~~~~


#### Connect with PostgreSQL

~~~~
$ pip install psycopg2 
$ sudo su - postgres
postgresql $ createdb {DB NAME}
postgresql $ createuser -P {USERNAME} [enter password]
postgresql $ exit
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': '{DB NAME}',
      'USER': 'root',
      'PASSWORD': '{PostgreSQL PASSWORD}',
      'HOST': '127.0.0.1',
      'PORT': '5432',
    }
  }
~~~~


#### When schema changed

~~~~
$ cd {PROJECT PATH}
$ ./manage.py makemigrations {APP NAME}
$ ./manage.py migrate {APP NAME}
~~~~


#### Use django-suit *(Custom admin interface)*

~~~~
$ pip install django-suit
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  INSTALLED_APPS = (
    # django-suit should come before 'django.contrib.admin'
    'suit',
    'django.contrib.admin',
    ...
  )

  from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

  TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
  )
~~~~


#### Use django-compressor *(Compress static files)*

~~~~
$ pip install django-compressor
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  INSTALLED_APPS += (
    'compressor',
  )
  
  # Use compressor only for production mode
  COMPRESS_ENABLED = not DEBUG
  COMPRESS_URL = STATIC_URL
  COMPRESS_ROOT = STATIC_ROOT
  COMPRESS_OUTPUT_DIR = 'CACHE'
  STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
  )

$ cd {PROJECT PATH}
$ ./manage.py migrate
$ ./manage.py collectstatic --noinput
~~~~


#### Install redis and connect with django

~~~~
$ apt-get install redis-server
$ pip install redis django-redis django-redisboard
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

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

$ ./manage.py migrate
$ ./manage.py collectstatic --noinput
~~~~


#### Use redisboard at admin

- Go to admin site
- `Redisboard` > `Redis Servers` > `Add Redis Server`
- Label : `localhost` / Hostname : `127.0.0.1`
- Check cache list at `Tools` > `Inspect`


#### Redis command

~~~~
$ service redis-server start    # Run redis as daemon
$ redis-cli save                # Save redis
$ redis-cli flushall            # Flush redis DB
$ redis-cli shutdown            # Shutdown redis
~~~~


#### Install celery and connect with django

~~~~
$ apt-get install rabbitmq-server
$ pip install celery django-celery amqp
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  import djcelery

  INSTALLED_APPS += (
    'djcelery',
  )

  djcelery.setup_loader()
  BROKER_URL = 'amqp://guest:guest@localhost:5672/'

$ vi {PROJECT PATH}/{PROJECT NAME}/wsgi.py

  import djcelery

  djcelery.setup_loader()

$ cd {PROJECT PATH}
$ ./manage.py migrate
$ ./manage.py collectstatic --noinput
$ touch logs/celery_daemon.log logs/celery_beat.log
~~~~


#### Celery command

- Check rabbitmq is running. If it is not running, type

~~~~
$ service rabbitmq-server start
~~~~

- If you want to run celery with root, add following code at shell configuration file such as `~/.zshrc`

~~~~
$ vi {SHELL CONFIGURATION FILE}

  export C_FORCE_ROOT='true'

$ source {SHELL CONFIGURATION FILE}
~~~~

~~~~
$ cd {PROJECT PATH}
$ ./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid   # Start celery as daemon
$ ./manage.py celery worker --loglevel=debug    # Start celery with debug mode 
$ ./manage.py celery purge                      # Flush celery tasks
$ ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15   # Stop celery
~~~~


#### Use cerely beat as cron task runner

- Enroll tasks at Admin > Djcelery > Periodic tasks

~~~~
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  CELERY_IMPORTS = ('utils.cron',)
  CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
~~~~


#### Celery beat command

~~~~
$ ./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach   # Start celery beat
$ ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15   # Stop celery beat
~~~~


#### Install uWSGI and configure Nginx and uWSGI settings

~~~~
$ pip install uwsgi
$ rm /etc/nginx/nginx.conf /etc/nginx/sites-enabled/default /etc/nginx/sites-avilable/default
$ ln -s {PROJECT PATH}/conf/nginx/nginx.conf /etc/nginx/nginx.conf
$ ln -s {PROJECT PATH}/conf/uwsgi/uwsgi.conf /etc/init/uwsgi.conf
$ mkdir -p /etc/uwsgi/vassals/
$ ln -s {PROJECT PATH}/conf/uwsgi/{PROJECT NAME}.ini /etc/uwsgi/vassals/
$ mkdir -p {PROJECT PATH}/logs/
$ cd {PROJECT PATH}/logs/
$ touch uwsgi.log uwsgi.pid
$ chown www-data.www-data uwsgi.log uwsgi.pid
~~~~


#### Nginx command

~~~~
$ service nginx status    # Check nginx status
$ service nginx start     # Start nginx
$ service nginx restart   # Restart nginx
$ service nginx stop      # Stop nginx
~~~~


#### uWSGI command

~~~~
$ uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term  --daemonize={LOG FILE PATH} # Run uWSGI
$ ps -ef | grep uwsgi | grep -v grep | awk "{print $2}" | xargs kill -15'   # Stop uWSGI
~~~~


#### When number of CPU core or memory size changed

~~~~~
$ vi nginx.conf

  worker_processes = {NUMBER OF CPU CORE}
  worker_connections = {MEMORY SIZE IN MEGA BYTES}
~~~~


#### Configure New Relic settings

- Visit <a href="http://newrelic.com/" target="_blank">newrelic.com</a> and login
- `APM` > `Python application`
- Get license key

~~~~
$ pip install newrelic
$ mkdir -p {PROJECT PATH}/conf/newrelic/
$ cd {PROJECT PATH}/conf/newrelic/
$ newrelic-admin generate-config {LICENSE KEY} newrelic.ini
$ vi {PROJECT PATH}/{PROJECT NAME}/wsgi.py

  import newrelic.agent
  
  newrelic.agent.initialize({PATH TO NEW RELIC CONFIGURATION}/newrelic.ini')
  application = newrelic.agent.wsgi_application()(application)
~~~~

- Restart uWSGI


#### Install Pillow for image processing

~~~~
$ apt-get install imagemagick libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev

# 32bit : i386-linux-gnu, 64bit : x86_64-linux-gnu
$ ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib 
$ ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib 
$ ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib 

# Only for ubuntu 14.04 LTS version 
$ ln -s /usr/include/freetype2 /usr/include/freetype 

$ pip install pillow
~~~~

- Check available list 
