from marshmallow import Schema, fields, post_load

from app.models.member import Member


# 멤버 조회를 위한 스키마
class MemberSchema(Schema):
    id = fields.String(description='사용자 PK')
    email = fields.Email(description='사용자 계정')
    name = fields.String(description='사용자 이름')
    created_time = fields.DateTime(description='회원가입일')
    last_login_time = fields.DateTime(description='최근 로그인')


# 회원 가입을 위한 스키마
class JoinSchema(Schema):
    email = fields.Email(description='사용자 계정')
    password = fields.String(load_only=True, description='비밀번호')
    name = fields.String(description='사용자 이름')

    @post_load
    def make_member(self, data, **kwargs):
        return Member(**data)