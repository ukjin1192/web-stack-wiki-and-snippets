# Web stack architecture

<img src="./architecture.png" />

# Contents in this repository

## Ubuntu basic settings

- Install basic packages
- Set timezone
- Customize **vim** editor
- Install **zshell** and oh-my-zshell
- Install **Fail2ban** to protect from malicious attack
- Configure **git** setting
- Install **nginx** *(Recommend version upper than 1.6)*
- Install **MySQL**
- Install **PostgreSQL**

#### Mac OS X basic settings
- Customize **terminal profile**
- Optimize key input
- Install **brew**


## Django basic settings

- Install django and helpful packages
- Clone sample django project if exist
- Connect with **MySQL**
- Connect with **PostgreSQL**
- When **schema changed**
- Use **django-suit** *(Custom admin interface)*
- Use **django-compressor** *(Compress static files)*
- Install **redis** and connect with django
- Use **redisboard** at admin
- Redis command
- Install **celery** and connect with django
- Celery command
- Use **cerely beat** as cron task runner
- Celery beat command
- Install uWSGI and configure **Nginx and uWSGI settings**
- Nginx command
- uWSGI command
- When number of **CPU** core or **memory** size changed
- Configure **New Relic** settings
- Install **Pillow** for image processing


## Django code snippets

- **Internationalization** *(Localization)*
- Send **mail** with template
- Use **redis** to manage in-memory DB
- Use **celery** to run task asynchronously
- Use **pillow** to process image
- Upload image to **cloudinary**
- Detect **facebook** deauthorization
- Use **firebase** as realtime DB


## Deploy django with Amazon Web Services

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


## Utilities wiki and snippets

- Deploy with **Fabric**
- Manage package with **npm**
- Use **Webpack** as module bundler
- Use **Gulp** as task runner
- Use **SASS** for stylesheet
- Multi browser test by **Selenium grid**
- Use **Docker** at Mac OS X
- **MeteorJS** wiki
