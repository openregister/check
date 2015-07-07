===============================
check
===============================


Quickstart
----------

Then run the following commands to bootstrap your environment.

```
mkvirtualenv --python=/path/to/required/python3 [appname]
```

Install python requirements.
```
pip install -r requirements/dev.txt
```

Once that this all done you can:

```
./run.sh
```

Deployment
----------

In your production environment, make sure the ``SETTINGS`` environment variable is set to ``config.Config``.

