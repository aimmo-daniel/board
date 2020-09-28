from flask import request, jsonify
from flask_classful import FlaskView, route

from app.service import auth_service


class AuthView(FlaskView):
    # 로그인
    @route('/login', methods=['POST'])
    def login(self):
        access_token = auth_service.get_token(request.data)
        return jsonify(access_token), 200
    
    # 로그아웃
    @route('/logout', methods=['GET'])
    def logout(self):
        auth_service.invalidate_token()
        return jsonify(message="로그아웃 되었습니다."), 200
