import os
from check.factory import create_app
app = create_app(os.environ['SETTINGS'])
