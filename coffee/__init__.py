from coffee.src.core import FlaskApp
from coffee.src.core.extensions import db
from coffee.src.core.extensions import api
from coffee.src.core.extensions import cors
from . import config


def create_app():
    app = FlaskApp(
        __name__,
        template_folder=config.TEMPLATES_DIR
    )
    app.config.from_pyfile(config.__file__)

    app.install_blueprints()
    app.install_all_api()
    app.init_database()

    db.init_app(app)
    api.init_app(app)
    cors.init_app(app)

    return app
