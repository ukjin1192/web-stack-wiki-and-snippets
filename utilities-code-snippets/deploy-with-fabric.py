#!/bin/bash
import os
from fabric.api import *

PROJECT_DIR = os.path.dirname(__file__)
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
  with cd(PROJECT_DIR):
    sudo("git pull origin master")
  
  with cd(PROJECT_DIR + "/" + PROJECT_NAME + "/static/css/"):
    local("sass styles.scss:styles.css")
  
  with cd(PROJECT_DIR):
    sudo("./manage.py collectstatic --noinput")
    sudo("./manage.py compress --force")
  
    with settings(warn_only=True):
      local("ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15")
      local("sleep 3")
      local("ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -9")
    
    with settings(warn_only=True):
      local("ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15")
      local("sleep 3")
      local("ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -9")
    
    with settings(warn_only=True):
      sudo("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -15")
      sudo("sleep 3")
      sudo("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -9")
    
    sudo("export C_FORCE_ROOT='true'")
    sudo("./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid")
    sudo("./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach")
    sudo("uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term")
