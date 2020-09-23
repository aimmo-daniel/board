from functools import wraps

import jwt
from bson.json_util import loads
from flask import current_app, request
from flask import g, jsonify


# 토큰 인증 필요
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not 'Authorization' in request.headers:
            return jsonify(message='로그인하지 않은 사용자입니다.'), 401

        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, current_app.config['SECRET'], current_app.config['ALGORITHM'])

        except jwt.InvalidTokenError:
            return jsonify(message='유효하지 않은 토큰입니다'), 401

        g.member_id = loads(payload['member_id'])

        return f(*args, **kwargs)
    return decorated_function
