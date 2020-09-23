import json

import jwt
from bson.json_util import dumps
from flask import jsonify, current_app

from app.models.member import Member


def getToken(data):
    # 로그인 시간 업데이트 및 인증 토큰발급
    format_data = json.loads(data)
    request_username = format_data['username']
    request_password = format_data['password']

    find_member = Member.objects(username=request_username).get()

    if find_member is None:
        return jsonify(message='없는 아이디 입니다.'), 422
    if not find_member.check_password(request_password):
        return jsonify(message='비밀번호가 틀렸습니다.'), 422

    find_member.update_last_login()

    token = jwt.encode({"member_id": dumps(find_member.id)}, current_app.config['SECRET'], current_app.config['ALGORITHM'])
    return token.decode('utf-8')


def invalidateToken():
    # 로그아웃, 인증 토큰 만료
    pass