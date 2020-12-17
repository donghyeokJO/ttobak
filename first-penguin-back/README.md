# Project: 또박이 

This document is about the backend part of **또박이**, especially focusing on setting Django Rest Framework for an API server. 

This Document will only contain the setting process, not about the details of the APIs. 

**Requirements**
----

 - LTS version Linux (best in 18.04 on ubuntu)
 - RAM more than 4GB
 - Storage left on more than 4GB
 - python 3.4 or later (latest recommended)
 - Django 1.11 or later (latest recommended)
 - Django Rest Framework 3.6 or later (latest recommended)
 - latest version of pip

**Used Version**
--
python : 3.6.9
Django : 3.0.8
Django Rest Framework : 3.11.0

**Setting Django Rest Framework**
--
**virtual environment and django setting**
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ (venv) python -m pip install --upgrade pip
$ (venv)pip install Django
$ (venv) pip install djangorestframework
$ (venv) django-admin startporject api
$ (venv) python manage.py startapp tt_apis
```
**modify api/settings.py** 

```python
ALLOWED_HOSTS = ['ec2-instance-dns-address','ip.of.ec2.instance'] #add the public dns address and the ip address of the ec2 instance we currently in use
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'tt_apis', #api app we added
'rest_framework', #django_rest_framework
]
...
REST_FRAMEWORK = { 
'DEFAULT_PERMISSION_CLASSES': [
'rest_framework.permissions.AllowAny', #only let allowed request
]
}
```
**modify  tt_apis/views.py & tt_apis/models.py** 

This document will not cover the details about this part as I already mentioned above.

**install nginx & uwsgi**

```bash
$ (venv) sudo apt-get install nginx
$ (venv) pip install uwsgi
$ (venv) cp /etc/nginx/uwsgi_params /home/ubuntu/ttobak/backend/api #add uwsgi parameters to project folder
$ (venv) cd /etc/nginx/sites-available
$ (venv) touch backend.conf #create nignx conf file for django
```

**backend.conf**
```bash
#set upstream(proxy)
upstream django{ 
server 127.0.0.1:8001; #the ip address and port that Django wil l listen through uwsgi
} 

#server configuration
server {
listen 8000; #port through external request
server_name 13.125.100.8; #ip address of running server
charset utf-8; 
client_max_body_size 100M;

#path to django static file
location /static{
alias /home/ubuntu/ttobak/backend/api/static;
}

#send all request(except static file) to upstream
location /{
uwsgi_pass django;
include /home/ubuntu/ttobak/backend/api/uwsgi_params;
}
}
```

**continue setting uwsgi & nginx**

```bash
$ (venv) sudo ln -s /etc/nginx/sites-available/backend.conf /etc/nginx/sites-enabled/ #add a symbolic link to sites-enabled
$ (venv) cd /home/ubuntu/ttobak/backend/api #back to project directory
$ (venv) python manage.py collectstatic #collect static file
$ (venv) touch back.ini
```
**back.ini**
```ini
[uwsgi] 
# Django-related settings
# the base directory (full path)
chdir = /home/ubuntu/ttobak/backend/api

# Django's wsgi file
module = api.wsgi

# the virtualenv (full path)
home = /home/ubuntu/ttobak/venv/

# process-related settings

# master
master = true

# maximum number of worker processes
processes = 4

# the socket (use the full path to be safe)
socket=127.0.0.1:8001

  

# permissions
chmod-socket = 666

# clear environment on exit
vacuum = true

# path of process logging file
daemonize=/home/ubuntu/ttobak/backend/api/back.log

# process pid
pidfile=/tmp/back.pid

  

# newrelic settings
enable-threads = true
single-interpreter = true
lazy-apps = true
```

**runserver using nginx&uwsgi**
```bash
$ (venv) sudo service nginx restart
$ (venv) uwsgi --ini back.ini
```



