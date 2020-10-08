import json

from flask import jsonify, request
from flask_classful import FlaskView
from marshmallow import ValidationError

from app.models.board import Board
from app.serializers.board import BoardCreateSchema, BoardSchema, BoardEditNameSchema, SimpleBoardSchema
from app.utils import auth_required


class BoardView(FlaskView):
    # 게시판 목록 조회
    def index(self):
        find_boards = Board.objects(deleted=False).order_by('name').paginate(1, 10)
        boards = SimpleBoardSchema().dump(find_boards, many=True)
        return jsonify(boards), 200

    # 게시판 상세 조회
    def get(self, board_id):
        find_board = Board.objects(id=board_id).first()
        board_detail = BoardSchema().dump(find_board)
        return jsonify(board_detail), 200

    # 게시판 추가
    @auth_required
    def post(self):
        try:
            form = BoardCreateSchema().load(json.loads(request.data))

            if Board.objects(name=form['name']).first():
                return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

            form.save()
        except ValidationError as err:
            return jsonify(err.messages), 422

        return jsonify(message='게시판이 생성되었습니다.'), 200

    # 게시판 이름 수정
    @auth_required
    def put(self, board_id):
        try:
            form = BoardEditNameSchema().load(json.loads(request.data))

            if Board.objects(name=form['name']).first():
                return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409

            find_board = Board.objects(id=board_id).first()
            find_board.update(**form)
        except ValidationError as err:
            return jsonify(err.messages), 422

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