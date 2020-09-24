import json

from flask import jsonify
from marshmallow import ValidationError

from app.models.member import Member
from app.serializers.member import JoinSchema, MemberSchema


# 회원목록 조회 서비스
def memberList():
    member_list = Member.objects(deleted=False).order_by('+create_date', '-username')
    result = MemberSchema().dump(member_list, many=True)
    return result


# 회원정보 조회 서비스
def memberDetail(member_id):
    find_member = Member.objects(id=member_id).get()
    result = MemberSchema().dump(find_member)
    return result


# 회원가입 서비스
def memberJoin(data):
    format_data = json.loads(data)
    request_username = format_data['username']

    if Member.objects(username=request_username):
        return jsonify(message='이미 가입된 아이디 입니다.'), 409

    try:
        result = JoinSchema().load(format_data)
    except ValidationError as err:
        return err

    result.save()


# 회원탈퇴 서비스
def memberWithdrawal(member_id):
    find_member = Member.objects(id=member_id)
    find_member.softDelete()