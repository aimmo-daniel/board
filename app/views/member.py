import json

import bcrypt
from flask import jsonify, request
from flask_classful import FlaskView
from mongoengine import ValidationError

from app.models.member import Member
from app.serializers.member import MemberSchema, JoinSchema, SimpleMemberSchema
from app.utils import auth_required


class MemberView(FlaskView):
    # 회원 목록 조회
    def index(self):
        try:
            members = Member.objects(deleted=False).order_by('+created_time', '-email')
            result = SimpleMemberSchema().dump(members, many=True)
        except ValidationError as err:
            return err

        return jsonify(result), 200

    # 회원 정보 상세 조회
    def get(self, member_id):
        try:
            find_member = Member.objects(id=member_id).first()
            member_detail = MemberSchema().dump(find_member)
        except ValidationError as err:
            return err

        return jsonify(member_detail), 200

    # 회원 가입
    def post(self):
        try:
            form = JoinSchema().load(json.loads(request.data))

            if Member.objects(email=form['email']).first():
                return jsonify(message='이미 가입된 아이디 입니다.'), 409

            form['password'] = bcrypt.hashpw(form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            form.save()
        except ValidationError as err:
            return jsonify(err.messages), 422

        return jsonify(message='회원가입이 완료되었습니다.'), 200

    # 회원 탈퇴
    @auth_required
    def delete(self, member_id):
        try:
            find_member = Member.objects(id=member_id).first()
            find_member.soft_delete()
        except ValidationError as err:
            return err

        return jsonify(message='회원탈퇴가 정상처리 되었습니다.'), 200
