import json

import pytest
from flask import url_for

from app.models.member import Member
from tests.member import MemberFactory


class Describe_MemberView:
    class Describe_join:
        @pytest.fixture
        def email(self):
            return 'test@email.com'

        @pytest.fixture
        def password(self):
            return 'abcdefghijk'

        @pytest.fixture
        def name(self):
            return 'daniel'

        @pytest.fixture
        def subject(self, client, email, password, name):
            url = url_for('MemberView:join')

            form = {
                'email': email,
                'password': password,
                'name': name
            }

            return client.post(url, data=json.dumps(form))

        class Context_정상케이스:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_member_id가_반환된다(self, subject):
                assert subject.json['id'] is not None

            def test_db에_저장된다(self, subject, email, name):
                member = Member.objects(email=email).get()
                assert member.name == name

        class Context_이름이_입력되지_않은경우:
            @pytest.fixture
            def name(self):
                return None

            def test_422가_반환된다(self, subject):
                assert subject.status_code == 422

        class Context_이미_가입된_이메일인경우:
            @pytest.fixture
            def already_joined_member(self):
                return MemberFactory.create()

            @pytest.fixture
            def email(self, already_joined_member):
                return already_joined_member.email

            def test_409가_반환된다(self, subject):
                assert subject.status_code == 409
