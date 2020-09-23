from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, BooleanField


class Board(Document):
    name = StringField(required=True, description='게시판 이름')
    create_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='게시판 생성일')
    deleted = BooleanField(default=False, description='삭제 여부')
    deleted_time = DateTimeField(null=True, default=None, description='게시판 삭제 시간')

    def edit_name(self, name):
        self.name = name
        self.save()

    def soft_delete(self):
        self.deleted = True
        self.deleted_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()