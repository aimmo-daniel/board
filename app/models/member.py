from datetime import datetime

import bcrypt
from flask_mongoengine import Document
from mongoengine import StringField, EmailField, DateTimeField, BooleanField


class Member(Document):
    email = EmailField(unique=True, required=True, description='계정 아이디 이메일 형식')
    name = StringField(required=True, description='사용자 이름')
    password = StringField(required=True, min_length=6, description='비밀번호 6자리 이상')
    created_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='가입 일시')
    last_login_time = DateTimeField(description='최근 로그인 일시')
    deleted = BooleanField(default=False, description='탈퇴 여부')
    deleted_time = DateTimeField(null=True, default=None, description='탈퇴 시간')

    # 마지막 로그인시간 업데이트
    def update_last_login_time(self):
        self.last_login_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()

    # 비밀번호 체크
    def check_password(self, req):
        if not bcrypt.checkpw(req.encode('utf-8'), self.password.encode('utf-8')):
            return False
        else:
            return True

    # 회원 탈퇴
    def soft_delete(self):
        self.deleted = True
        self.deleted_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()