import bcrypt
from marshmallow import Schema, fields, post_load

from app.models.member import Member


# 멤버 조회를 위한 스키마
class MemberSchema(Schema):
    id = fields.String(description='사용자 PK')
    username = fields.Email(description='사용자 계정')
    name = fields.String(description='사용자 이름')
    create_time = fields.DateTime(description='회원가입일')
    last_login = fields.DateTime(description='최근 로그인')
    deleted = fields.Boolean(description='삭제 여부')


# 회원 가입을 위한 스키마
class JoinSchema(Schema):
    username = fields.Email(description='사용자 계정')
    password = fields.String(description='비밀번호')
    name = fields.String(description='사용자 이름')

    @post_load
    def make_member(self, data, **kwargs):
        password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data['password'] = password
        return Member(**data)