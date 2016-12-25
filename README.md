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
