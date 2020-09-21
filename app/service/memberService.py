import json

from flask import jsonify

from app.models.member import Member
from app.serializers.member import JoinSchema, MemberSchema


def memberList():
    """회원목록 조회 서비스"""
    members = Member.objects(deleted=False)
    result = MemberSchema().dump(members, many=True)
    return result


def memberDetail(member_id):
    """회원정보 조회 서비스"""
    find_member = Member.objects(id=member_id).get()
    result = MemberSchema().dump(find_member)
    return result


def memberJoin(data):
    """회원가입 서비스"""
    format_data = json.loads(data)

    if Member.objects(username=format_data['username']):
        return jsonify(message='이미 가입된 아이디 입니다.'), 409

    result = JoinSchema().load(format_data)
    result.save()


def memberWithdrawal(member_id):
    """회원탈퇴 서비스"""
    find_member = Member.objects(id=member_id)
    find_member.update(deleted=True)