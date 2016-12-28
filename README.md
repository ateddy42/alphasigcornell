### Initial Setup

Install the following versions of `django` and `flup`. Deploying to the remote server with fastcgi will not work for django versions >= 1.9
```
pip install django==1.8.7
pip install flup==1.0.2
```
This version uses a MySQL database, so use the dbProps.cnf file to change the connection settings, or create an additional settings file and overwrite the database connection.

### Deploying the Server

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

Add a file named `alphasigcornell.fcgi` with the following contents:
```
#!/home/alphasi4/python27/bin/python27
import sys, os

# Add a custom Python path.
sys.path.append("/home/alphasi4/python27")
sys.path.append("/home/alphasi4/public_html/dev/alphasigcornell")
sys.path.append("/home/alphasi4/public_html/dev/alphasigcornell/web")

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings_dev'
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
```

Run `chmod 755 alphasigcornell.fcgi` to enable execute permissions. If everythin was configured correctly, you should be able to view the website.

### Properties Files

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

### Database Groups

* `Rush` - Users in this group can view the list of rushes
* `RushChair` - Users in this group have administrator capabilities for the Rush section of the website
