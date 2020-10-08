from marshmallow import Schema, fields, post_load

from app.models.member import Member


# 멤버 조회를 위한 스키마
class MemberSchema(Schema):
    id = fields.String(description='사용자 PK')
    email = fields.Email(description='사용자 계정')
    name = fields.String(description='사용자 이름')
    created_time = fields.DateTime(description='회원가입일')
    last_login_time = fields.DateTime(description='최근 로그인')
    deleted = fields.Boolean(description='탈퇴여부')
    deleted_time = fields.DateTime(description='탈퇴 일시')


# 멤버 목록 조회를 위한 스키마
class SimpleMemberSchema(Schema):
    id = fields.String(description='사용자 PK')
    email = fields.Email(description='사용자 계정')
    name = fields.String(description='사용자 이름')


# 회원 가입을 위한 스키마
class JoinSchema(Schema):
    email = fields.Email(description='사용자 계정', required=True)
    password = fields.String(load_only=True, description='비밀번호', required=True)
    name = fields.String(description='사용자 이름', required=True)

    @post_load
    def make_member(self, data, **kwargs):
        return Member(**data)


# 로그인을 위한 스키마
class LoginSchema(Schema):
    email = fields.Email(description='사용자 계정')
    password = fields.String(description='비밀번호')