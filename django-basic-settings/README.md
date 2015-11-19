# Django basic settings

#### Install django and helpful packages

~~~~
$ pip install django django-debug-toolbar fabric httplib2
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


#### Connect with MySQL

~~~~
$ pip install MySQL-python
$ service mysql restart
$ mysql -u root [Enter password]
mysql $ CREATE DATABASE {DB NAME} DEFAULT CHARACTER SET utf8;
mysql $ exit;
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': '{DB NAME}',
      'USER': 'root',
      'PASSWORD': '{PASSWORD}',
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
      'PASSWORD': '{PASSWORD}',
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
$ pip instal django-suit
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
$ redis-server          # Start redis
$ redis-cli save        # Save redis DB
$ redis-cli flushall    # Flush redis DB
$ redis-cli shutdown    # Shutdown redis
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
  CELERYD_PREFETCH_MULTIPLIER = 1   # More time-consuming tasks, More closer to number 1
  CELERYD_CONCURRENCY = 1           # Default : Number of CPU cores

$ vi {PROJECT PATH}/{PROJECT NAME}/wsgi.py

  import djcelery

  djcelery.setup_loader()

$ cd {PROJECT PATH}
$ ./manage.py migrate
$ ./manage.py collectstatic --noinput
$ touch logs/celery_daemon.log logs/celery_beat.log
~~~~


#### Celery command

~~~~
$ cd {PROJECT PATH}
$ export C_FORCE_ROOT='true'
$ ./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid   # Start celery worker
$ ./manage.py celery worker --loglevel=debug   # Start celeryt worker with debug mode 
$ ./manage.py celeryctl purge                  # Flush celery tasks
$ ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15   # Stop celery worker
~~~~


#### Use cerely beat as cron task runner

- Enroll tasks at Admin > Djcelery > Periodic tasks

~~~~
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  # Execute periodic tasks by DB scheduler to enroll tasks at Admin
  CELERY_IMPORTS = ('utils.cron',)
  CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
~~~~


#### Celery beat command

~~~~
$ export C_FORCE_ROOT='true'
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
$ service nginx restart
$ uwsgi --uid www-data --gid www-data --emperror /etc/uwsgi/vassals --master --die-on-term
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
  
  newrelic.agent.initialize({PROJECT PATH}/conf/newrelic/newrelic.ini')
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


#### When CPU core or memory size changed

~~~~~
$ vi nginx.conf

  worker_processes = {NUMBER OF CORE}


$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py
  
  CELERYD_CONCURRENCY = {NUMBER OF CORE}
~~~~
