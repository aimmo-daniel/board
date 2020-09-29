# import json
#
# from flask import jsonify
# from marshmallow import ValidationError
#
# from app.models.board import Board
# from app.serializers.board import BoardSchema, BoardCreateSchema
#
#
# # TODO: 페이징 처리 및 검색 필터링
#
# # 게시판 목록 조회
# def get_boards():
#     boards = Board.objects(deleted=False).order_by('name')
#     result = BoardSchema(exclude={'deleted'}).dump(boards, many=True)
#     return result
#
#
# # 게시판 생성
# def create_board(data):
#     format_data = json.loads(data)
#     request_name = format_data['name']
#
#     if Board.objects(name=request_name):
#         return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409
#     try:
#         result = BoardCreateSchema().load(format_data)
#     except ValidationError as err:
#         return err
#
#     result.save()
#
#
# # 게시판 이름 수정
# def edit_board_name(board_id, data):
#     format_data = json.loads(data)
#     request_name = format_data['name']
#
#     if Board.objects(name=request_name):
#         return jsonify(message='이미 존재하는 게시판 이름입니다.'), 409
#
#     find_board = Board.objects(id=board_id).get()
#     find_board.edit_name(request_name)
#
#
# # 게시판 삭제
# def delete_board(board_id):
#     find_board = Board.objects(id=board_id).get()
#     find_board.soft_delete()