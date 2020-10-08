from datetime import datetime
from enum import Enum

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ListField, ReferenceField, IntField, BooleanField, ObjectIdField

from app.models.board import Board
from app.models.member import Member


class Post(Document):
    title = StringField(required=True, description='글 제목')
    content = StringField(required=True, description='글 내용')
    created_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='글 생성 시간')
    modified_time = DateTimeField(null=True, default=None, description='글 수정 시간')
    deleted_time = DateTimeField(null=True, default=None, description='글 삭제 시간')
    deleted = BooleanField(default=False, description='글 삭제 여부')
    writer = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    board = ReferenceField(Board, required=True, description='게시판(board_id')
    tags = ListField(StringField(), null=True, default=None, description='태그 목록')
    like_count = IntField(default=0, min_value=0, description='좋아요수')
    dislike_count = IntField(default=0, min_value=0, description='싫어요수')
    view_count = IntField(default=0, min_value=0, description='조회수')

    # 좋아요 싫어요 갯수 증가/감소
    def change_like_dislike_count(self, discribe):
        if discribe == "좋아요":
            self.like_count += 1
        elif discribe == "좋아요취소":
            self.like_count -= 1
        elif discribe == '싫어요':
            self.dislike_count += 1
        elif discribe == '싫어요취소':
            self.dislike_count -= 1
        elif discribe == "좋아요>싫어요":
            self.like_count -= 1
            self.dislike_count += 1
        elif discribe == "싫어요>좋아요":
            self.dislike_count -= 1
            self.like_count += 1

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
