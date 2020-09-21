import os

import mongoengine
from flask import Flask
from .views import register_api


def create_app():
    app = Flask(__name__)
    app.debug = True
    phase = os.environ.get('PHASE', 'local').lower()

    try:
        app.config.from_object('app.config.%sConfig' % phase.capitalize())
        mongoengine.connect(host=app.config['MONGO_URI'])
    except Exception as e:
        print('데이터베이스 연결 에러 : ' + str(e))

    from flask_cors import CORS

    CORS(send_wildcard=True, expose_headers=['content-disposition', 'Content-Length', 'Content-Range'], max_age=6000).init_app(app)

    register_api(app)

    return app