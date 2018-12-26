## Configuring the Website
* [Initial Setup](#setup) 
* [Deploying the Server](#deploy) 
* [Properties Files](#props)
* [Database Setup](#dbsetup)
  * [Database Groups](#dbgroups)
  * [Database Users](#dbusers)

### Initial Setup
<a name="setup"/>

Software Requirements
```
Python = 2.7
Django = 1.11.17
```
This version uses a MySQL database, so use the dbProps.cnf file to change the connection settings, or create an additional settings file and overwrite the database connection. Sample `dbProps.cnf` listed below.

### Deploying the Server
<a name="deploy"/>

** Note: to use a different settings file, simply replace all references to `settings_prouduction` below with the name of your settings file **

SSH into the server, and cd to the `~/public_html` directory. Clone this github repository, then add the two properties files as described below.

Configure the .htaccess file:
```
AddHandler fcgid-script .fcgi
RewriteEngine On
ExpiresDefault "access plus 1 minute"
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ alphasigcornell.fcgi/$1 [QSA,L]
<IfModule mod_headers.c>
<FilesMatch "\.(svg|ttf|otf|eot|woff|woff2)$">
    Header set Access-Control-Allow-Origin "*"
</FilesMatch>
</IfModule>
```
Huge thank-you to https://github.com/NetAngels/django-fastcgi for making it easier to deploy to shared hosting sites using FCGI. Run `pip install django-fastcgi-server` to install their package, then add a file named `alphasigcornell.fcgi` with the following contents (replace ellipses with proper paths):
```
#!/......./python27
import sys, os

# Add a custom Python path.
sys.path.append(".../alphasigcornell")

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings_production'
from django_fastcgi.servers.fastcgi import runfastcgi
from django.core.servers.basehttp import get_internal_wsgi_application

wsgi_application = get_internal_wsgi_application()
runfastcgi(wsgi_application, method="prefork", daemonize="false", minspare=1, maxspare=1, maxchildren=1)
```

Run `chmod 755 alphasigcornell.fcgi` to enable execute permissions. If everything was configured correctly, you should be able to view the website.

### Properties Files
<a name="props"/>

* `dbProps.cnf` - REQUIRED - Contains the connection properties for the database. Example below:
```
[client]
database = ''
user = ''
password = ''
host = ''
port = ''
```
* `/web/settings_production.py` - Contains the properties for running the site in production mode. Example below:
```
from settings import *

DEBUG = False

TEMPLATE_DEBUG = False

SECRET_KEY = ...

ALLOWED_HOSTS = [...]

STATIC_URL = ...

STATIC_ROOT = ...

MEDIA_URL = ...

MEDIA_ROOT = ...
```

### Database Setup
<a name="dbsetup"/>
The following are steps that should be taken to configure the database to allow users to access and edit the site.

#### Database Groups
<a name="dbgroups"/>

* `Rush` - (Required) Users in this group can view the list of rushes. No permissions need to be configured via the Admin portal.
* `RushChair` - (Required) Users in this group have administrator capabilities for the Rush section of the website. No permissions need to be configured via the Admin portal.
* `Secretary` - (Recommended) Users in this group can add/edit Brothers and Officers via the Admin Portal. Group must be configured to have create/edit/delete permissions for the `main | brother` and `main | officer` models.

#### Database Users
<a name="dbusers"/>

If not configured already, create a superuser via `python manage.py createsuperuser --settings=web.settings_production`. You can then login to the Admin Portal as this user to configure additional users and groups.

* To grant a user access to view the list of rush signins, add them to the group `Rush`
* To grant a user access to edit the list of rush signins and configure who can comment on rushes, add them to the groups `Rush` and `RushChair`
* (if configured above) To grant a user access to edit the list of Brothers/Officers on the main part of the website, add them to the group `Secretary`
