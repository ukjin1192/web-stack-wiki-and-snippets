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

# Deploy server information
env.hosts = {HOST IP}
env.user = 'ubuntu'
env.key_filename = {PEM FILE PATH}
env.port = 22


def deploy():
  """
  Deploy at remote server
  """
  with cd(ROOT_DIR):
    sudo("git pull origin master")
    sudo("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -15")
    sudo("uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term --daemonize=" + ROOT_DIR + "/logs/uwsgi.log")
~~~~


#### Install boto to integrate with Amazon Web Services

~~~~
$ pip install boto3
$ cd {PROJECT PATH}
$ vi fabfile.py
~~~~


#### `fabfile.py`

~~~~
#!/bin/bash
import os
from boto3.session import Session
from fabric.api import *

ROOT_DIR = os.path.dirname(__file__)
PROJECT_NAME = {PROJECT NAME}

AWS_ACCESS_KEY_ID = {AWS ACCESS KEY ID}
AWS_SECRET_ACCESS_KEY = {AWS SECRET ACCESS KEY}


# Deploy server information
env.hosts = []
env.user = 'ubuntu'
env.key_filename = {PEM FILE PATH}
env.port = 22

session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-northeast-2')   # SEOUL REGION

ec2 = session.resource('ec2')

for instance in ec2.instances.all():            
  env.hosts.append(instance.public_dns_name)


def deploy():
  """
  Deploy at remote server
  """
  with cd(ROOT_DIR):
    sudo("git pull origin master")
    sudo("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -15")
    sudo("uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term --daemonize=" + ROOT_DIR + "/logs/uwsgi.log")
~~~~
