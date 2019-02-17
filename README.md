

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

## Later changes to the db can be implemented through migrations
```
flask db migrate -m "adding a new column/table"
flask db upgrade
```
