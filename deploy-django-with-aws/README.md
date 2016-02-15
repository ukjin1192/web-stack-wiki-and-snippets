# Deploy django with Amazon Web Services

- **EC2** *(OS: ubuntu 14.04 LTS)*
	- Use fixed IP with **Elastic IPs**
	- Load balance with **ELB**(Elastic Load Balancer)
	- Adapt SSL ceritificate at **ELB**
	- **Auto Scaling Groups** with **Cloud Watch**
	- Get access permission with **IAM**(Identity & Access Management)
- **Route** 53 *(DNS)*
- **RDS** *(MySQL)*
- **ElastiCache** *(Redis)*
- **S3** *(Storage)*
- **CloudFront** *(CDN)*


## EC2

- `EC2 menu` > `Launch Instance` > `Ubuntu Server 14.04 LTS`
- Click `Next` until `6. Configure Security Group`
- Set inbound rule for security group as following

Type | Protocol | Port | Source
-----|----------|------|-------
SSH | TCP | 22 | 0.0.0.0/0 (or Your IP)
HTTP | TCP | 80 | 0.0.0.0/0 (for nginx)
HTTPS | TCP | 443 | 0.0.0.0/0 (for nginx)
Custom TCP Rule | TCP | 8000 | 0.0.0.0/0 (for test)

- `Review and Launch` > `Launch`
- Create PEM file and save it into local directory *(DO NOT share or delete PEM file)*- 

#### Use fixed IP with Elastic IPs

- `EC2 menu` > `Elastic IPs` > `Allocate New Address` > `Yes, Allocate`
- Right click IP > `Release addresses` > `Yes, Release` > Select instance > `Release`
- From now on, you can make SSH connect to instance with PEM file 

~~~~
$ ssh -i {PATH TO PEM FILE} {EC2 PUBLIC DNS}

OR,

$ vi ~/.ssh/config

    Host *
      TCPKeepAlive yes
      ServerAliveInterval 120

    host {NICKNAME}
      Hostname {EC2 PUBLIC DNS}
      User ubuntu
      IdentityFile {PATH TO PEM FILE}
    
$ ssh {NICKNAME}
~~~~

#### Load balance with ELB(Elastic Load Balancer)

- `EC2 menu` > `Load Balancers` > `Create Load Balancer`
- Put `Load Balancer name`
- Assign security group same as EC2
- Click `Next` until `4. Configure Health Check`
- Set `Ping Path` value with `/health_check`
- Click `Next` repeatedly and click `Create`
- Edit `nginx.conf`

~~~~
server {
	...
  location /health_check {
  	access_log off;
    return 200;
  }
  ...
}
~~~~

#### Adapt SSL certificate at ELB

- *Certificate Manager is only available at US East region until now*
- Create private key

~~~~~
$ openssl req -new -newkey rsa:2048 -nodes -keyout mysite_com.key -out mysite_com.csr
~~~~~

- Purchase Comodo positive SSL certificate and put mysite_com.key to activate SSL
- Check email from Comodo which contains below files
	- Root CA Certificate - `AddTrustExternalCARoot.crt`
	- Intermediate CA Certificate - `COMODORSAAddTrustCA.crt`
	- Intermediate CA Certificate - `COMODORSADomainValidationSecureServerCA.crt`
	- PositiveSSL Certificate - `mysite_com.crt`
- Merge above files into one *(Be careful of the order)*

~~~~
$ cat mysite_com.crt COMODORSADomainValidationSecureServerCA.crt  COMODORSAAddTrustCA.crt AddTrustExternalCARoot.crt > mysite_com_bundle.crt
~~~~

- `EC2 menu` > `Load Balancers`
- Select load balancer and click `Listeners` tab
- Click `Edit` and add listener as following

Load Balancer Protocol | Load Balancer Port | Instance Protocol | Instance Port | Cipher | SSL Certificate
-----------------------|--------------------|-------------------|---------------|--------|----------------
HTTPS | 443 | HTTP | 80 | Use default | Add

- Click `Change` on `SSL Certificate` column and add certificate
	- Private key : `mysite_com.key`
	- Public key : `mysite_com_bundle.crt`
	- Certificate chain : `None`
- Edit `nginx.conf` to redirect `HTTP` to `HTTPS`

~~~~
server {
  listen 80;
  ...
	location / {
		if ($http_x_forwarded_proto != 'https') {
			return 301 https://$host$request_uri;
		}
	...
	}
}
~~~~

#### Auto Scaling Groups with Cloud Watch

- `EC2 menu` > `Instances`
- Right click instance > `Image` > `Create Image` > Put `Image name` > `Create Image`
- `EC2 menu` > `Launch Configurations` > `Create launch configuration`
- `My AMIs` > Select AMI > Select instance type > Put `Name` > Check `Monitoring` > Click `Advanced Details`
- Fill out `User data` as initial script when instance created. For example,

~~~~
#!/bin/bash
cd {PATH TO PROJECT PATH}
git pull origin master
	# OR git clone {REMOTE URL} if pull request requires username and password
{INITIAL COMMANDS}
	# Maybe fabric commands like 
		# fab run_updatestaticfiles
		# fab run_uwsgi
		# fab run_celery
~~~~

- `Next: Add Storage` > `Next: Configure Security Group`
- `Select an existing security group` > Select same one with EC2 > `Review` > `Create launch configuration`
- `Choose an existing key pair` > Select same one with EC2 > `Create launch configuration`
- Put `Group name` > Click empty input of `Subnet` > Select all *(...northeast...)*
- Click `Advanced Details` > Check `Load Balancing` > Click empty input of `Load Balancing` > Choose ELB
- Check `Monitoring` > `Next: Configure scaling pollicies` 
- Select `Use scaling policies to adjust the capacity of this group` > Put minimum and maximum number of instances. For example, 
	- Scale between `1` and `4` instances.
- Fill out `Increase Group Size`
	- `Take the action` : `Add` `1` `instances`
	- `Add new alarm` > Uncheck `Send a notification to` > Whenever `Average` of `CPU Utilization` Is `>=` `80` Percent For at least `1` consecutive period(s) of `1 Minute` > `Create alarm`
- Fill out `Decrease Group Size`
	- `Take the action` : `Remove` `1` `instances`
	- `Add new alarm` > Uncheck `Send a notification to` > Whenever `Average` of `CPU Utilization` Is `<=` `10` Percent For at least `1` consecutive period(s) of `1 Minute` > `Create alarm`
- `Next: Configure Notifications` > `Add notification` > `create topic` > Put `topic name` and `email address`
- `Review` > `Create Auto Scaling Group`
- `EC2 menu` > `Instances`
- Check new instace is initializing and terminate original instance
- **When `user data` script updated,**
	- `EC2 menu` > `Launch Configurations` > `Copy launch configuration` > `Advanced details` > Update `user data` > `Select an existing security group` > Select same one with EC2 > `Review` > `Create launch configuration`
	- `EC2 menu` > `Auto Scaling Groups` > `Edit` > Switch `Launch Configuration`
- **When `models.py` updated,**
	- `EC2 menu` > `Auto Scaling Groups` > `Edit` > Set `min` and `max` as `1`
	- Connect to remained instace and migrate DB
	- Create new `AMI` with this instance
	- Create new `Launch configuration` with this `AMI`
	- `EC2 menu` > `Auto Scaling Groups` > `Edit` > Switch `Launch Configuration` to this `Launch configuration`
	- `EC2 menu` > `Auto Scaling Groups` > `Edit` > Set `min` and `max` with original value

#### Get access permission with IAM(Identity & Access Management)

- `IAM` > `Users` > `Create New Users` > Put `User Name` > Click `Show User Security Credentials` > Check `Access Key ID` and `Secret Access Key` > `Close`
- Click newly created user > `Permissions` > `Attach Policy` > Select `AmazonEC2FullAccess` > `Attach Policy`


## Route 53

- If you don't have domain yet, get domain from `Route 53 menu` > `Domain Registration`
- `Route 53 menu` > `DNS Management` > `Create Hosted Zone`
- Put `Domain Name`
- Click `Create Record Set`
- Put values as following

Type | Alias | Alias Target or Value
-----|-------|----------------------
NS | No | {NAME SERVER LIST}
A | Yes | {ELB A RECORD}
MX | No | {MAIL SERVER}


## RDS

- `RDS menu` > `Launch a DB Instance` > `MySQL`
- Click `No` for `Multi-AZ deployment` option to use free-tier
- Select `db.t2.micro` for `DB Instance Class` and `No` for `Multi-AZ Deployment`
- Put `DB Instance Identifier`, `Master Username`, `Master Password`
- `Launch DB Instance`
- Edit inbound rule of security group as following

Type | Protocol | Port | Source
-----|----------|------|-------
MySQL | TCP | 3306 | 0.0.0.0/0

- Create database with MySQL command

~~~~
$ sudo su
$ mysql -u {MASTER USERNAME} -p -h {RDS END POINT} 
$ {MASTER PASSWORD}
mysql $ CREATE DATABASE {DB NAME} DEFAULT CHARACTER SET utf8;
mysql $ exit;
~~~~

- Edit `settings.py`

~~~~
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
     'NAME': '{DB NAME}',
     'USER': '{MASTER USERNAME}',
     'PASSWORD': '{MASTER PASSWORD}',
     'HOST': '{RDS END POINT}',
     'PORT': '3306',
     'DEFAULT-CHARACTER-SET': 'utf8',
   }
}
~~~~

- Migrate database

~~~~
$ cd {PROJECT PATH}
$ ./manage.py migrate
$ ./manage.py makemigrations {APPLICATION NAME}
$ ./manage.py migrate {APPLICATION NAME}
~~~~


## ElastiCache

- `ElastiCache menu` > `Launch Cache Cluster` > `Redis`
- Uncheck `Enable Replication` option to use free-tier
- Put `Cluster Name` and select `cache.t2.micro` for `Node Type`
- Create new security group as following inbound rule

Type | Protocol | Port | Source
-----|----------|------|-------
Custom TCP Rule | TCP | 6379 | 0.0.0.0/0

- Edit `settings.py`

~~~~
CACHES = {
	'default': {
		'BACKEND': 'django_redis.cache.RedisCache',
		'LOCATION': 'redis://{END POINT}:6379',
		'OPTIONS': {
			'CLIENT_CLASS': 'django_redis.client.DefaultClient',
		}
	}
}
~~~~


## S3

- `S3 menu` > `Create Bucket`
- Put `Bucket Name` and `Create`
- Go to newly created bucket > `Propeties` > `Permissions` > `Add bucket policy`

~~~~
{
	"Version": "2008-10-17",
	"Id": "Policy1403276359730",
	"Statement": [
		{
			"Sid": "Stmt1403276358543",
			"Effect": "Allow",
			"Principal": {
				"AWS": "*"
			},
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::{BUCKET NAME}/*"
		}
	]
}
~~~~

- `Save` policy > `Save` permissions
- `Create Folder` and upload `sample.png`


## CloudFront

- `CloudFront menu` > `Create distribution` > Choose `Web`
- Click `Origin Domain Name` and choose `bucket` under `Amazon S3 Buckets`
- `Create distribution`
- You can get `sample.png` from `{CLOUDFRONT DOMAIN NAME}/{FOLDER NAME}/sample.png`
- Note that `{BUCKET NAME}` is not included in URL
