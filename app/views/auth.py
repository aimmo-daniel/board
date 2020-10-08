import json

import jwt
from bson.json_util import dumps
from flask import request, jsonify, current_app
from flask_classful import route, FlaskView

from app.models.member import Member
from app.serializers.member import LoginSchema


class AuthView(FlaskView):
    # 로그인
    @route('/login', methods=['post'])
    def login(self):
        form = LoginSchema().load(json.loads(request.data))

        find_member = Member.objects(email=form.get('email')).first()

        if not find_member:
            return jsonify(message='존재하지 않는 이메일 입니다.'), 422
        if not find_member.check_password(form.get('password')):
            return jsonify(message='비밀번호가 틀렸습니다.'), 422

        find_member.update_last_login_time()

        token = jwt.encode({"member_id": dumps(find_member.id)}, current_app.config['SECRET'], current_app.config['ALGORITHM'])

        return jsonify(token.decode('utf-8')), 200

    # 로그아웃
    #@route('/logout', methods=['get'])
    #def logout(self):
        #auth_service.invalidate_token()
        #return jsonify(message="로그아웃 되었습니다."), 200
