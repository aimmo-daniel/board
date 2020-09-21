import json

from app.serializers.comment import CommentCreateSchema


def createComment(post_id, data):
    """댓글 작성"""
    format_data = json.loads(data)
    format_data['post_id'] = post_id

    result = CommentCreateSchema().load(format_data)
    result.save()