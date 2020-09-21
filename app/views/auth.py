import jwt
from flask import request, jsonify
from flask_classful import FlaskView, route

from app.service import authService


class AuthView(FlaskView):
    @route('/login', methods=['POST'])
    def login(self):
        access_token = authService.getToken(request.data)
        return jsonify(access_token), 200

    @route('/logout', methods=['GET'])
    def logout(self):
        authService.invalidateToken()
        return jsonify(message="로그아웃 되었습니다."), 200
