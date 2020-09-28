import logging

# Mongodb 연결 congif 파일
class Config:
    MONGO_URI = 'mongodb://localhost:27017/board'
    SECRET = 'hiitssecret'
    ALGORITHM = 'HS256'
    TESTING = False

    LOG_LEVEL = logging.getLevelName(logging.DEBUG)
    LOG_RESPONSE = True


class LocalConfig(Config):
    MONGO_URI = 'mongodb://localhost:27017/board'
    QUERY_LOG = True


class TestConfig(Config):
    MONGO_URI = 'mongomock://127.0.0.1:27017/board?connect=false'
    TESTING = True
    QUERY_LOG = True
    AUTO_CREATE_INDEX = True