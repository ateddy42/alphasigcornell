### Initial Setup

Software Requirements
```
Python = 2.7
Django = 1.11.17
```
This version uses a MySQL database, so use the dbProps.cnf file to change the connection settings, or create an additional settings file and overwrite the database connection. Sample `dbProps.cnf` listed below.

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

Add a file named `alphasigcornell.fcgi` with the following contents (replace ellipses with proper paths):
```
#!/......./python27
import sys, os

# Add a custom Python path.
sys.path.append(".../alphasigcornell")

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
