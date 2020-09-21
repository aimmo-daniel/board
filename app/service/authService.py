import json

import jwt
from flask import jsonify, current_app

from bson.json_util import dumps
from app.models.member import Member


def getToken(data):
    format_data = json.loads(data)

    find_member = Member.objects(username=format_data['username']).first()

    if find_member is None:
        return jsonify(message='없는 아이디 입니다.'), 422
    if not find_member.check_password(format_data['password']):
        return jsonify(message='비밀번호가 틀렸습니다.'), 422

    find_member.update_last_login()
    find_member.save()

    token = jwt.encode({"user_id": dumps(find_member.id)}, current_app.config['SECRET'], current_app.config['ALGORITHM'])

    return token.decode('utf-8')


def invalidateToken():
    pass