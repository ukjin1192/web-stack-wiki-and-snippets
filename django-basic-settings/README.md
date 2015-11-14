# Django basic settings

#### Install django and helpful packages

$ pip install django django-debug-toolbar httplib2
$ cd {PROJECT PATH}
$ ./manage.py migrate
$ ./manage.py runserver 0.0.0.0:8000

  Check URL {PUBLIC IP}:8000 on browser

#### Clone sample django project if exist

~~~~
$ ssh-keygen
$ cat ~/.ssh/id_rsa.pub

  Add public key to Github or Bitbucket

$ mkdir -p /var/www/
$ cd /var/www/
$ git clone {GIT REMOTE ORIGIN URL}
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

