# Django with amazon web service
- EC2 (OS: ubuntu 14.04 LTS)
- ELB (Load balancing)
- Route 53 (DNS)
- RDS (MySQL or PostgreSQL)
- ElasticCache (Redis)


## EC2 (OS: ubuntu 14.04 LTS)
- EC2 menu > Launch Instance
- Select 'Ubuntu Server 14.04 LTS'
- Click 'Next' until '6. Configure Security Group'
- Set inbound rule for security group as following

Type | Protocol | Port | Source
-----|----------|------|-------
SSH | TCP | 22 | 0.0.0.0/0 (or Your IP)
HTTP | TCP | 80 | 0.0.0.0/0 (for nginx)
HTTPS | TCP | 443 | 0.0.0.0/0 (for nginx)
Custom TCP Rule | TCP | 8000 | 0.0.0.0/0 (for test)

- Review and Launch > Launch
- Create PEM file and save it into local directory
- Connect to terminal with PEM file


## ELB (Load balancing)
- EC2 menu > Load Balancers > Create Load Balancer
- Put 'Load Balancer name'
- Click 'Next' until '4. Configure Health Check'
- Set 'Ping Path' as "/health_check"
- Change nginx configuration
- Click 'Next' repeatedly and 'Create'
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


## Route 53
- If you don't have domain yet, get domain from 'Route 53 menu > Domain Registration'
- Route 53 menu > DNS Management > Create Hosted Zone
- Put 'Domain Name'
- Create Record Set

Type | Alias | Alias Target or Value
-----|-------|----------------------
NS | No | {NAME SERVER LIST}
A | Yes | {ELB A RECORD}
MX | No | {MAIL SERVER}


## Adapt SSL certificate
- Create private key

		$ openssl req -new -newkey rsa:2048 -nodes -keyout example_com.key -out example_com.csr

- Purchase Comodo positive SSL certificate and put example_com.key to activate SSL
- Get email from Comodo which contains 4 files as following

		Root CA Certificate - AddTrustExternalCARoot.crt
		Intermediate CA Certificate - COMODORSAAddTrustCA.crt
		Intermediate CA Certificate - COMODORSADomainValidationSecureServerCA.crt
		PositiveSSL Certificate - example_com.crt

- Combine above 4 files as following (Be careful of the order)

		$ cat example_com.crt COMODORSADomainValidationSecureServerCA.crt  COMODORSAAddTrustCA.crt AddTrustExternalCARoot.crt > example_com_bundle.crt

- Go to AWS > EC2 > Elastic Load balancer > Listener and add following row

Load Balancer Protocol | Load Balancer Port | Instance Protocol | Instance Port | Cipher | SSL Certificate
-----|-----------------|--------------------|-------------------|---------------|--------|----------------
HTTPS | 443 | HTTP | 80 | Use default | Add

	- Add certificate
		Private key : example_com.key
		Public key : example_com_bundle.crt
		Certificate chain : None
	- Save changes

- Edit nginx configuration to redirect HTTP to HTTPS

		server {
	        listen 80;
	        ...
	        
			location / {
	            
	            # Redirect HTTP to HTTPS
	            if ($http_x_forwarded_proto != 'https') {
	                return 301 https://$host$request_uri;
	            }
	            ...
	        }
		}

<h2>RDS instance</h2>

- Create RDS
- Create security group and set inbound rules as following

Type | Protocol | Port | Source
-----|----------|------|-------
MySQL | TCP | 3306 | 0.0.0.0/0

- Connect RDS with django application server

		root $ mysql -u root -p -h {RDS END POINT} [enter password]
		
		- When user want to add another Databases
		mysql $ CREATE DATABASE {DB NAME} DEFAULT CHARACTER SET utf8;
		mysql $ exit;
		
		root $ vi {PROJECT PATH}/{PROJECT NAME}/settings/prod.py
		
			DATABASES = {
		    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': '{DB NAME}',
	        'USER': 'root',
	        'PASSWORD': '{PASSWORD}',
	        'HOST': '{RDS END POINT}',
	        'PORT': '3306',
	        'DEFAULT-CHARACTER-SET': 'utf8',
		    }
			}
			
		root $ cd {PROJECT PATH}
		root $ ./manage.py migrate
		root $ ./manage.py makemigrations {APP NAME}
		root $ ./manage.py migrate {APP NAME}



<h2>Elastic Cache</h2>

- Choose Engine (Redis)
- Cancel checkbox 'Enable Replication' and choose cache.t2.micro if it is development purpose
- Choose security group. Security group should contain following inbound rule.

Type | Protocol | Port | Source
-----|----------|------|-------
Custom TCP Rule | TCP | 6379 | 0.0.0.0/0

- Change cache configuration in settings.py as following

			CACHES = {
				'default': {
				  	'BACKEND': 'django_redis.cache.RedisCache',
				    'LOCATION': 'redis://{END POINT}:6379',
				    'OPTIONS': {
				    	'CLIENT_CLASS': 'django_redis.client.DefaultClient',
				    }
				}
			}
