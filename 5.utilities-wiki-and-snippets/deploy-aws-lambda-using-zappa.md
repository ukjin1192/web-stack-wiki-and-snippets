#### Install AWS CLI

~~~~
$ pip install awscli --upgrade
~~~~

#### Create IAM

- http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
- Permission : `AdministratorAccess`

#### Set AWS configuration at the local instance

~~~~
$ aws configure
  AWS Access Key ID [None]: {BLAH}
  AWS Secret Access Key [None]: {BLAH}
  Default region name [None]: ap-northeast-2 // SEOUL
  Default output format [None]: json
~~~~

- Check configuration

~~~~
$ cat ~/.aws/credentials
$ cat ~/.aws/config
~~~~

#### Clone python project

~~~~
$ git clone {GIT REPOSITORY}
$ cd {PROJECT DIRECTORY}
~~~~

#### Install virtualenv and install python packages

~~~~
$ pip install virtualenv --upgrade
$ virtualenv {VIRTUALENV NAME}
$ source {VIRTUALENV NAME}/bin/activate
$ pip install -r pip-requirements.txt
$ pip install zappa
~~~~

#### Deploy AWS lambda using Zappa

~~~~
$ zappa init
  What do you want to call this environment (default 'dev'): dev  // Environment = Stage
  What do you want call your bucket? (default 'zappa-xi82x3v32'):
  Where is your app's function?: {PYTHON_MODULE.FUNCTION_NAME}
  Would you like to deploy this application globally? (default 'n') [y/n/(p)rimary]: n
  Does this look okay? (default 'y') [y/n]: y
$ vi zappa_settings.json
  "keep_warm": false,
$ zappa deploy {STAGE NAME}
~~~~

- After every code updates,

~~~~
$ zappa update {STAGE NAME}
~~~~

- Using local variables : https://github.com/Miserlou/Zappa#setting-environment-variables
- Search logs at CloudWatch
  - Metric Filters
  - Expire Events After
