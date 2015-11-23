#### Install fabric 

~~~~
$ pip install fabric
$ cd {PROJECT PATH}
$ vi fabfile.py
~~~~


#### `fabfile.py`

~~~~
#!/bin/bash
import os
from fabric.api import *

ROOT_DIR = os.path.dirname(__file__)
PROJECT_NAME = {PROJECT NAME}

# Remote server information
env.hosts = {HOST IP}
env.user = 'ubuntu'
env.key_filename = {PEM FILE PATH}
env.port = 22


def remote_deploy():
  """
  Deploy at remote server
  """
  with cd(ROOT_DIR):
    sudo("git pull origin master")
    sudo("./manage.py collectstatic --noinput")
    sudo("./manage.py compress --force")
    with settings(warn_only=True):
      sudo("ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15")
    with settings(warn_only=True):
      sudo("ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15")
    with settings(warn_only=True):
      sudo("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -15")
    sudo("./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid")
    sudo("./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach")
    sudo("uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term --daemonize=" + ROOT_DIR + "/logs/uwsgi.log")
~~~~
