from flask_restx import Api
import os

app_version = os.environ.get('APP_VERSION', 'dev')

api = Api(version=app_version)

# Importing Namespaces
from .sample import sample_namespace
from .utils import utils_namespace

api.add_namespace(sample_namespace, path='/api/sample-namespace')
api.add_namespace(utils_namespace, path='/api/utils')