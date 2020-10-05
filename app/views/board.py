from flask import jsonify
from flask_apispec import use_kwargs
from flask_classful import FlaskView, route
from marshmallow import ValidationError

from app.models.board import Board
from app.serializers.board import BoardCreateSchema, BoardSchema
from app.utils import auth_required


class BoardView(FlaskView):
    # 게시판 목록 조회
    @route('', methods=['GET'])
    def boards(self):
        boards = Board.objects(deleted=False).order_by('name')
        result = BoardSchema().dump(boards, many=True)
        return jsonify(result), 200

    # 게시판 추가
    @route('', methods=['POST'])
    @use_kwargs(BoardCreateSchema(), locations=('json',))
    @auth_required
    def create(self, **kwargs):
        if Board.objects(name=kwargs.get('name')).exists():
            return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409
        try:
            result = BoardCreateSchema().load(kwargs)
            result.save()
        except ValidationError as err:
            return err

        return jsonify(message='게시판이 생성되었습니다.'), 200

    # 게시판 이름 수정
    @route('/<board_id>', methods=['PUT'])
    @use_kwargs(BoardSchema(only={'name'}, partial=True), locations=('json',))
    @auth_required
    def edit(self, board_id, **kwargs):
        if Board.objects(name=kwargs.get('name')).exists():
            return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

        try:
            find_board = Board.objects(id=board_id).first()
            find_board.update(**kwargs)
        except ValidationError as err:
            return err

        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시판 삭제
    @route('/<board_id>', methods=['DELETE'])
    @auth_required
    def delete(self, board_id):
        try:
            find_board = Board.objects(id=board_id).first()
            find_board.soft_delete()
        except ValidationError as err:
            return err

        return jsonify(message='게시판이 삭제되었습니다.'), 200