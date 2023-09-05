from flask import Flask
from api import api
import os

app_version = os.environ.get('APP_VERSION', 'dev')

app = Flask(__name__)

api.init_app(app,
             version=app_version,
             title='Sample Flask BoilerPlate',
             description='An BoilerPlate Application with usage of pandas',
             license="GNU GPLv3",
             license_url="https://www.gnu.org/licenses/gpl-3.0.en.html"
)

if __name__ == '__main__':
    app.run(debug=True)