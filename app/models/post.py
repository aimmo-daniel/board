from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField, BooleanField

from app.models.board import Board
from app.models.comment import Comment
from app.models.member import Member


class Post(Document):
    title = StringField(required=True, description='글 제목')
    content = StringField(required=True, description='글 내용')
    create_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='글 생성 시간')
    modified_time = DateTimeField(description='글 수정 시간')
    deleted_time = DateTimeField(description='글 삭제 시간')
    deleted = BooleanField(default=False, description='글 삭제 여부')
    writer = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    board_id = ReferenceField(Board, required=True, description='게시판(board_id')
    tag_list = ListField(StringField(), description='태그 목록')
    comment_list = ListField(ReferenceField(Comment), description='댓글 목록')
    like_count = IntField(required=True, default=0, min_value=0, description='좋아요수')
    view_count = IntField(required=True, default=0, min_value=0, description='조회수')

    """좋아요"""
    def like_post(self):
        self.like_count += 1

    """좋아요 취소"""
    def unlike_post(self):
        if self.like_count > 0:
            self.like_count -= 1

    """조회수 증가"""
    def view_post(self):
        self.view_count += 1

    """글 삭제"""
    def soft_delete(self):
        self.deleted = not self.deleted