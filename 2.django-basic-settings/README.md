# Django basic settings


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

- If you want to remove existing packages,

~~~~
$ pip freeze | xargs pip uninstall -y
~~~~

- Install pip requirements

~~~~
$ pip install -r {PATH TO PIP REQUIREMENTS}/requirements.txt
~~~~


#### Install django

~~~~
$ pip install --upgrade pip
$ pip install django
$ cd /var/www/
$ django-admin startproject {PROJECT NAME}
$ cd {PROJECT PATH}
$ ./manage.py runserver 0.0.0.0:8000 [Ignore migration error messages]
~~~~

- Check URL `{PUBLIC IP}:8000` on browser


#### Connect with MySQL

~~~~
$ pip install MySQL-python
$ sudo service mysql restart
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
  
$ cd {PROJECT PATH}
$ ./manage.py migrate
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
  
$ cd {PROJECT PATH}
$ ./manage.py migrate
~~~~

- Note: If you using custom user model, it would be better to migrate after fill out your user model in `models.py`


#### When schema changed

~~~~
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

  # Django < 1.9
  from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

  TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
  )
~~~~

#### Install Django extensions

~~~~
$ pip install django-extensions 
~~~~

- Commands

~~~~
$ ./manage.py shell_plus
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

$ vi {TEMPLATE FILE}

  {% load compress %}
  ...
  {% compress css %}
  ...
  {% endcompress %}
  ...
  {% compress js %}
  ...
  {% endcompress %}

$ cd {PROJECT PATH}
$ ./manage.py collectstatic --noinput
~~~~


#### Install redis and connect with django

~~~~
$ sudo apt-get install redis-server
$ pip install redis django-redis
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  CACHES = {
    'default': {
      'BACKEND': 'django_redis.cache.RedisCache',
      'LOCATION': 'redis://127.0.0.1:6379/1',
      'OPTIONS': {
        'CLIENT_CLASS': 'django_redis.client.DefaultClient',
      }
    }
  }
~~~~


#### Use redisboard at admin (Only works with local redis server)

~~~~
$ pip install django-redisboard
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  INSTALLED_APPS += (
    'redisboard',
  )

$ ./manage.py makemigrations redisboard
$ ./manage.py migrate redisboard
~~~~

- If you using django-compressor

~~~~
$ ./manage.py collectstatic --noinput
~~~~

- Go to admin page and login
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


#### Install uWSGI and configure Nginx and uWSGI settings

~~~~
$ pip install uwsgi
$ rm /etc/nginx/nginx.conf /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
$ vi {PROJECT PATH}/conf/nginx/nginx.conf
~~~~

- Copy `nginx.conf` and customize `{{DOMAIN OR PUBLIC IP}}`, `{PROJECT NAME}` and `{PROJECT PATH}`

~~~~
$ chmod 775 {PROJECT PATH}/conf/nginx/nginx.conf
$ ln -s {PROJECT PATH}/conf/nginx/nginx.conf /etc/nginx/nginx.conf
~~~~

- Copy `uwsgi.conf` and paste

~~~~
$ chmod 775 {PROJECT PATH}/conf/uwsgi/uwsgi.conf
$ ln -s {PROJECT PATH}/conf/uwsgi/uwsgi.conf /etc/init/uwsgi.conf
$ vi {PROJECT PATH}/conf/uwsgi/{PROJECT NAME}.ini
~~~~

- Copy `{PROJECT NAME}.ini` and customize `{PROJECT NAME}` and `{PROJECT PATH}`

~~~~
$ chmod 775 {PROJECT NAME}.ini
$ mkdir -p /etc/uwsgi/vassals/
$ ln -s {PROJECT PATH}/conf/uwsgi/{PROJECT NAME}.ini /etc/uwsgi/vassals/
~~~~

- Initiate log files

~~~~
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


#### Install celery and connect with django

~~~~
$ apt-get install rabbitmq-server
$ pip install django-celery==[Latest version] celery==[Same with django-celery version] amqp
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
$ ./manage.py makemigrations djcelery
$ ./manage.py migrate djcelery
~~~~


#### Celery command

- Check rabbitmq is running. If it is not running, type

~~~~
$ service rabbitmq-server start
~~~~

- If you want to run celery with root permission, add following code at shell configuration file such as `~/.zshrc`

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

  CELERY_IMPORTS = ('{Application}.{Python file that contains cron tasks}',) (e.g. 'utils.cron')
  CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
~~~~


#### Celery beat command

~~~~
$ ./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach   # Start celery beat
$ ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15   # Stop celery beat
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


#### Install Django REST framework

~~~~
$ pip install djangorestframework
$ pip install markdown
$ pip install django-filter
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  INSTALLED_APPS += (
    'rest_framework',
  ) 
~~~~


#### Use django-silk *(live profiling and inspection tool)*

~~~~
$ pip install django-silk
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  # Django >= 1.10
  MIDDLEWARE = ['silk.middleware.SilkyMiddleware', ] + MIDDLEWARE
  
  # Django <= 1.9
  MIDDLEWARE_CLASSES = ('silk.middleware.SilkyMiddleware', ) + MIDDLEWARE_CLASSES
  
  INSTALLED_APPS += (
    'silk',
  ) 
  
$ cd {PROJECT PATH}
$ ./manage.py makemigrations silk
$ ./manage.py migrate silk
~~~~

#### User JWT(Json Web Token) as authentication method in Django REST framework

~~~~
$ pip install djangorestframework-jwt
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
      ...
      'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
      ...
    )
  }
  
$ {PROJECT PATH}/{PROJECT NAME}/urls.py

  from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

  urlpatterns = [
    ...
    url(
        r'^api-token-auth/',                                                                        
        obtain_jwt_token,                                                                           
    ), 
    url(                                                                                            
        r'^api-token-refresh/',                                                                     
        refresh_jwt_token                                                                           
    ),
    url(
        r'^api-token-verify/', 
        verify_jwt_token
    ),
    ...
  ]
~~~~

- Usage
  - Get token
    - End-point: `{PROJECT DOMAIN}/api-token-auth/`
    - HTTP method: `POST`
    - parameters: `{'username': {USERNAME}, 'password': {PASSWORD}}`
    - return: `{'token': {TOKEN}}`
  - Verify token
    - End-point: `{PROJECT DOMAIN}/api-token-verify/`
    - HTTP method: `POST`
    - parameters: `{'token': {EXISTING TOKEN}}`
    - return: `200 OK` or `400 Bad Request`
  - Refresh token
    - End-point: `{PROJECT DOMAIN}/api-token-refresh/`
    - HTTP method: `POST`
    - parameters: `{'token': {EXISTING TOKEN}}`
    - return: `{'token': {NEW TOKEN}}`


#### Use django-cors-headers to enable Cross-Origin-Resouce-Sharing

~~~~
$ pip install django-cors-headers
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  INSTALLED_APPS = (
    ...
    'corsheaders',
    ...
  )

  MIDDLEWARE = [
      ...
      'corsheaders.middleware.CorsMiddleware',
      'django.middleware.common.CommonMiddleware',
      ...
  ]
  
  CORS_ORIGIN_WHITELIST = (
    '*.mysite.com',
  )
