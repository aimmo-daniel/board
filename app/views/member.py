from flask import request, jsonify
from flask_classful import FlaskView, route

from app.service import memberService
from app.utils import auth_required


class MemberView(FlaskView):
    # 회원 목록 조회
    @route('', methods=['GET'])
    def list(self):
        member_list = memberService.memberList()
        return jsonify(member_list), 200

    # 회원 정보 조회
    @route('/<member_id>', methods=['GET'])
    def detail(self, member_id):
        member_detail = memberService.memberDetail(member_id)
        return jsonify(member_detail), 200

    # 회원 가입
    @route('', methods=['POST'])
    def join(self):
        memberService.memberJoin(request.data)
        return jsonify(message='회원가입이 완료되었습니다.'), 200

    # 회원 탈퇴
    @route('/<member_id>', methods=['DELETE'])
    @auth_required
    def withdrawal(self, member_id):
        memberService.memberWithdrawal(member_id)
        return jsonify(message='회원탈퇴가 정상처리 되었습니다.'), 200


