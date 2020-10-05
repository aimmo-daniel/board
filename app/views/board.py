import json

from flask import jsonify, request
from flask_classful import FlaskView
from marshmallow import ValidationError

from app.models.board import Board
from app.serializers.board import BoardCreateSchema, BoardSchema, BoardEditNameSchema
from app.utils import auth_required


class BoardView(FlaskView):
    # 게시판 목록 조회
    def index(self):
        boards = Board.objects(deleted=False).order_by('name')
        result = BoardSchema().dump(boards, many=True)
        return jsonify(result), 200

    # 게시판 추가
    @auth_required
    def post(self):
        form = BoardCreateSchema().load(json.loads(request.data))

        if Board.objects(name=form['name']).exists():
            return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409
        try:
            form.save()
        except ValidationError as err:
            return err

        return jsonify(message='게시판이 생성되었습니다.'), 200

    # 게시판 이름 수정
    @auth_required
    def put(self, board_id):
        form = BoardEditNameSchema().load(json.loads(request.data))

        if Board.objects(name=form['name']).exists():
            return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

        try:
            find_board = Board.objects(id=board_id).first()
            find_board.update(**form)
        except ValidationError as err:
            return err

        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시판 삭제
    @auth_required
    def delete(self, board_id):
        try:
            find_board = Board.objects(id=board_id).first()
            find_board.soft_delete()
        except ValidationError as err:
            return err

        return jsonify(message='게시판이 삭제되었습니다.'), 200