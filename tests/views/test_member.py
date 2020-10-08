import json

import pytest
from bson import ObjectId
from flask import url_for

from app.models.member import Member
from tests.factories.member import MemberFactory, WithdrawalMemberFactory


class Describe_MemberView:
    class Describe_index:
        @pytest.fixture
        def subject(self, client):
            url = url_for('MemberView:index')
            return client.get(url)

        class Context_정상케이스:
            @pytest.fixture(autouse=True)
            def already_joined_member(self):
                return MemberFactory.create()

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_member_list가_반환된다(self, subject, already_joined_member):
                body = subject.get_json()

                assert body[0]['id'] == str(already_joined_member.id)
                assert body[0]['email'] == already_joined_member.email
                assert body[0]['name'] == already_joined_member.name

        class Context_Member가_없는경우:
            @pytest.fixture
            def member(self):
                return None

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_빈값이_반환된다(self, subject, member):
                body = subject.get_json()
                assert body == []

        class Context_탈퇴한_멤버인경우:
            @pytest.fixture
            def withdrawal_member(self):
                return WithdrawalMemberFactory.create()

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_빈값이_반환된다(self, subject, withdrawal_member):
                body = subject.get_json()
                assert body == []

    class Describe_get:
        @pytest.fixture
        def already_joined_member(self):
            return MemberFactory.create()

        @pytest.fixture
        def target_member_id(self, already_joined_member):
            return already_joined_member.id

        @pytest.fixture
        def subject(self, client, target_member_id):
            url = url_for('MemberView:get', member_id=target_member_id)
            return client.get(url)

        class Context_정상케이스:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_member가_반환된다(self, subject, already_joined_member):
                body = subject.get_json()

                assert body['id'] == str(already_joined_member.id)
                assert body['email'] == already_joined_member.email
                assert body['name'] == already_joined_member.name

        class Context_존재하지않는_member_id인경우:
            @pytest.fixture
            def target_member_id(self, already_joined_member):
                return ObjectId()

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_빈값이_반환된다(self, subject):
                body = subject.get_json()
                assert body == {}

    class Describe_post:
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
            url = url_for('MemberView:post')

            form = {
                'email': email,
                'password': password,
                'name': name
            }

            return client.post(url, data=json.dumps(form))

        class Context_정상케이스:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_db에_저장된다(self, subject, email, name):
                member = Member.objects(email=email).get()
                assert member.name == name

        class Context_이미_가입된_이메일인경우:
            @pytest.fixture
            def already_joined_member(self):
                return MemberFactory.create()

            @pytest.fixture
            def email(self, already_joined_member):
                return already_joined_member.email

            def test_409가_반환된다(self, subject):
                assert subject.status_code == 409

    class Describe_delete:
        @pytest.fixture
        def logged_in_member(self):
            return MemberFactory.create()

        @pytest.fixture(autouse=True)
        def subject(self, client, headers, logged_in_member):
            url = url_for('MemberView:delete', member_id=logged_in_member.id)
            return client.delete(url, headers=headers)

        class Context_정상케이스:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200

            def test_member의_deleted가_True가_된다(self, subject):
                member_is_deleted = Member.objects.get().deleted
                assert member_is_deleted is True

        class Context_로그인하지_않은경우:
            @pytest.fixture
            def token(self):
                return None

            def test_401이_반환된다(self, subject):
                assert subject.status_code == 401
