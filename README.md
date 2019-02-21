

## Create virtualenv

```
virtualenv -p /usr/local/bin/python3 envname
source envname/bin/activate
pip install -r requirements.txt
deactivate # deactivate environment
```

## Setup SQLLite DB and initiate website

```
export FLASK_APP=app.py
flask db init
flask db migrate -m "setup db"
flask db upgrade
python app.py
```
Web app should now be reacheable at http://localhost:5000/

## Later changes to the db can be implemented through migrations
```
flask db migrate -m "adding a new column/table"
flask db upgrade
```

## Config templates have to be made available in order to build configs
Config templates to be specified in the sabi/devices/views.py under the ops_build_config views:

```

def ops_build_config(device_id):
	...
    config_template = "/tmp/mikrotik_config.rsc"
    ...
```
Newly built configs will be created in the same basedir (eg: /tmp).

....
