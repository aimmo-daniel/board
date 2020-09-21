from datetime import datetime

import bcrypt
from mongoengine import StringField, Document, EmailField, DateTimeField, BooleanField


class Member(Document):
    username = EmailField(unique=True, required=True, description='계정 아이디 이메일 형식')
    name = StringField(required=True, description='사용자 이름')
    password = StringField(required=True, min_length=6, description='비밀번호 6자리 이상')
    create_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='가입 일시')
    last_login = DateTimeField(description='최근 로그인 일시')
    deleted = BooleanField(default=False, description='탈퇴 여부')

    def update_last_login(self):
        self.last_login = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')

    def check_password(self, req):
        if not bcrypt.checkpw(req.encode('utf-8'), self.password.encode('utf-8')):
            return False
        else:
            return True