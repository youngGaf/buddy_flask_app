import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config import app_config

env_name = os.getenv('FLASK_ENV')

# app_initialisation
app = Flask(__name__)
app.config.from_object(app_config[env_name])

# initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.models import UserModel, FeaturesModel, FeatureVotesModel

# Register API views blueprint
from src.views import FeaturesApiView, UsersApiView, FeatureVotesApiView
app.register_blueprint(FeaturesApiView.features_api, url_prefix='/api/v1/feature')
app.register_blueprint(UsersApiView.user_api, url_prefix='/api/v1/user')
app.register_blueprint(FeatureVotesApiView.features_vote_api, url_prefix='/api/v1/vote-feature')


@app.route('/', methods=['GET'])
def index():
    """
    Test endpoint
    """
    return 'Test endpoint is now working'


if __name__ == '__main__':
    app.run(debug=True)
