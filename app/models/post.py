from datetime import datetime
from enum import Enum

from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField, BooleanField

from app.models.board import Board
from app.models.member import Member


class Category(Enum):
    general = 0
    notice = 1


class Post(Document):
    title = StringField(required=True, description='글 제목')
    content = StringField(required=True, description='글 내용')
    created_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='글 생성 시간')
    modified_time = DateTimeField(null=True, default=None, description='글 수정 시간')
    deleted_time = DateTimeField(null=True, default=None, description='글 삭제 시간')
    deleted = BooleanField(default=False, description='글 삭제 여부')
    writer = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    board = ReferenceField(Board, required=True, description='게시판(board_id')
    type = IntField(default=Category.general, description='게시물 타입')
    tags = ListField(StringField(), null=True, default=None, description='태그 목록')
    likes = ListField(StringField(), description='좋아요 누른 유저 목록')
    view_count = IntField(default=0, min_value=0, description='조회수')

    # 좋아요
    def like(self, member_id):
        if not member_id in self.likes:
            self.likes.append(member_id)
            self.save()

    # 좋아요 취소
    def unlike(self, member_id):
        if member_id in self.likes:
            self.likes.remove(member_id)
            self.save()

    # 조회수 증가
    def increase_view_count(self):
        self.view_count += 1
        self.save()

    # 글 수정
    def update_post_modified_time(self, title, content):
        self.modified_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()

    # 글 삭제 및 삭제시간 업데이트
    def soft_delete(self):
        self.deleted = True
        self.deleted_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()
