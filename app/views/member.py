import json

import bcrypt
from flask import jsonify, request
from flask_apispec import use_kwargs
from flask_classful import FlaskView, route
from mongoengine import ValidationError

from app.models.member import Member
from app.serializers.member import MemberSchema, JoinSchema
from app.utils import auth_required


class MemberView(FlaskView):
    # 회원 목록 조회
    @route('', methods=['GET'])
    def members(self):
        try:
            member_list = Member.objects(deleted=False).order_by('+created_time', '-username')
            result = MemberSchema().dump(member_list, many=True)
        except ValidationError as err:
            return err

        return jsonify(result), 200

    # 회원 정보 조회
    @route('/<member_id>', methods=['GET'])
    def detail(self, member_id):
        try:
            find_member = Member.objects(id=member_id).first()
            result = MemberSchema().dump(find_member)
        except ValidationError as err:
            return err

        return jsonify(result), 200

    # 회원 가입 #TODO: 여기 수정해야함
    @route('', methods=['POST'])
    # @use_kwargs(JoinSchema(), locations=('json',))
    def join(self, **kwargs):
        form = JoinSchema().load(json.loads(request.data))
        if Member.objects(email=form.get('email')):
            return jsonify(message='이미 가입된 아이디 입니다.'), 409

        try:
            form['password'] = bcrypt.hashpw(form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            member = Member(**form)
            member.save()
        except ValidationError as err:
            return err

        return jsonify(message='회원가입이 완료되었습니다.'), 200


    # 회원 탈퇴
    @route('/<member_id>', methods=['DELETE'])
    @auth_required
    def withdrawal(self, member_id):
        try:
            find_member = Member.objects(id=member_id).first()
            find_member.soft_delete()
        except ValidationError as err:
            return err

        return jsonify(message='회원탈퇴가 정상처리 되었습니다.'), 200
