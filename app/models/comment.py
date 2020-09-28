from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField, ListField

from app.models.member import Member
from app.models.post import Post


class Comment(Document):
    post = ReferenceField(Post, required=True, description='게시글 정보(post_id')
    writer = ReferenceField(Member, required=True, description='글쓴이(member_id)')
    content = StringField(required=True, description='댓글 내용')
    create_time = DateTimeField(default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'), description='댓글 생성 시간')
    likes = ListField(StringField(), description='좋아요 누른 유저 목록')
    modified_time = DateTimeField(null=True, default=None, description='댓글 수정 시간')
    deleted = BooleanField(default=False, description='댓글 삭제 여부')
    deleted_time = DateTimeField(null=True, default=None, description='댓글 삭제 시간')

    # 좋아요
    def like(self, member_id):
        if member_id not in self.likes:
            self.likes.append(member_id)
            self.save()

    # 좋아요 취소
    def unlike(self, member_id):
        if member_id not in self.likes:
            self.likes.remove(member_id)
            self.save()

    # 댓글 수정
    def editComment(self, content):
        self.content = content
        self.modified_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()

    # 댓글 삭제
    def softDelete(self):
        self.deleted = True
        self.deleted_time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        self.save()