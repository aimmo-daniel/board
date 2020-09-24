from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, BooleanField


class Board(Document):
    name = StringField(required=True, description='게시판 이름')
    create_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='게시판 생성일')
    deleted = BooleanField(default=False, description='삭제 여부')
    deleted_time = DateTimeField(null=True, default=None, description='게시판 삭제 시간')

    # 게시판 이름 수정
    def editName(self, name):
        self.name = name
        self.save()

    # 게시판 삭제
    def softDelete(self):
        self.deleted = True
        self.deleted_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()