# Deploy django with amazon web service

- EC2 *(OS: ubuntu 14.04 LTS)*
- ELB *(Load balancing)*
	- Adapt SSL certificate at ELB
- Route 53 *(DNS)*
- RDS *(MySQL)*
- ElastiCache *(Redis)*


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
- Create PEM file and save it into local directory *(DO NOT share or delete PEM file)*
- From now on, you can make SSH connect to instance with PEM file


## ELB

- EC2 menu > Load Balancers > Create Load Balancer
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
