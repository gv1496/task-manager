from flask import Flask
from flasgger import Swagger


def create_app(test_config=None):
    app = Flask(__name__)
    Swagger(app)

    if test_config:
        app.config.update(test_config)

    from app.routes import task_bp

    app.register_blueprint(task_bp)

    return app
