from flask import jsonify, request
from flask_classful import FlaskView, route

from app.service import board_service
from app.utils import auth_required


class BoardView(FlaskView):
    # 게시판 목록 조회
    @route('', methods=['GET'])
    def boards(self):
        board_list = board_service.get_boards()
        return jsonify(board_list), 200

    # 게시판 추가
    @route('', methods=['POST'])
    @auth_required
    def create(self):
        board_service.create_board(request.data)
        return jsonify(message='게시판이 생성되었습니다.'), 200

    # 게시판 이름 수정
    @route('/<board_id>', methods=['PUT'])
    @auth_required
    def edit(self, board_id):
        board_service.edit_board_name(board_id, request.data)
        return jsonify(message='게시판 이름이 변경되었습니다.'), 200

    # 게시판 삭제
    @route('/<board_id>', methods=['DELETE'])
    @auth_required
    def delete(self, board_id):
        board_service.delete_board(board_id)
        return jsonify(message='게시판이 삭제되었습니다.'), 200