import datetime
from typing import Type

from django.conf import settings
from django.db import models
from django.test import TestCase
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.test import APIClient

from project.api.models import RoleEnum, Trip, User
from project.api.serializers import TripSerializer, UserSerializer


class BaseTestCase(TestCase):
    USER1_EMAIL = 'user1@example.com'
    USER1_PASSWORD = 'user1@example.com'

    USER2_EMAIL = 'user2@example.com'
    USER2_PASSWORD = 'user2@example.com'

    MANAGER1_EMAIL = 'manager1@example.com'
    MANAGER1_PASSWORD = 'manager1@example.com'

    MANAGER2_EMAIL = 'manager2@example.com'
    MANAGER2_PASSWORD = 'manager2@example.com'

    ADMIN1_EMAIL = 'admin1@example.com'
    ADMIN1_PASSWORD = 'admin1@example.com'

    ADMIN2_EMAIL = 'admin2@example.com'
    ADMIN2_PASSWORD = 'admin2@example.com'

    def _authenticate(self, email: str, password: str) -> None:
        response = self.client.post(
            '/api/auth/obtain_token/',
            {
                'email': email,
                'password': password
            })
        token = response.data['token']
        auth_header_prefix = settings.JWT_AUTH["JWT_AUTH_HEADER_PREFIX"]

        self.client.credentials(HTTP_AUTHORIZATION=f'{auth_header_prefix} {token}')

    def _create_user_instance(self, email: str, password: str, role: RoleEnum, save: bool = True) -> User:
        user = User(email=email, role=int(role))
        user.set_password(password)

        if save:
            user.save()

        return user

    def _get_expected_result(
            self,
            serializer_class: Type[serializers.Serializer],
            *instances: models.Model,
            as_list: bool = True) -> bytes:
        data = []

        for instance in instances:
            serializer = serializer_class(instance)
            data.append(serializer.data)

        if len(instances) == 1 and not as_list:
            data = data[0]

        expected_result = CamelCaseJSONRenderer().render(data)

        return expected_result

    def _get_expected_users(self, *users: User, as_list: bool = True) -> bytes:
        return self._get_expected_result(UserSerializer, *users, as_list=as_list)

    def setUp(self) -> None:
        self.user1 = self._create_user_instance(self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)
        self.user2 = self._create_user_instance(self.USER2_EMAIL, self.USER2_PASSWORD, RoleEnum.USER)

        self.manager1 = self._create_user_instance(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD, RoleEnum.MANAGER)
        self.manager2 = self._create_user_instance(self.MANAGER2_EMAIL, self.MANAGER2_PASSWORD, RoleEnum.MANAGER)

        self.admin1 = self._create_user_instance(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD, RoleEnum.ADMIN)
        self.admin2 = self._create_user_instance(self.ADMIN2_EMAIL, self.ADMIN2_PASSWORD, RoleEnum.ADMIN)

        self.client = APIClient()


class UserViewSetTest(BaseTestCase):
    def _list_users(self) -> Response:
        return self.client.get('/api/users/')

    def _retrieve_user(self, pk: int) -> Response:
        return self.client.get(f'/api/users/{pk}/')

    def _create_user(self, email: str, password: str, role: RoleEnum) -> Response:
        return self.client.post(
            '/api/users/',
            {
                'email': email,
                'password': password,
                'role': int(role)
            })

    def _update_user(self, pk: int, email: str, password: str, role: RoleEnum) -> Response:
        return self.client.put(
            f'/api/users/{pk}/',
            {
                'email': email,
                'password': password,
                'role': int(role)
            })

    def _destroy_user(self, pk: int) -> Response:
        return self.client.delete(f'/api/users/{pk}/')

    def test_list_requires_authentication(self) -> None:
        # Act
        response = self._list_users()

        # Assert
        self.assertEqual(401, response.status_code)

    def test_list_for_user_returns_only_themselves(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.user1)

        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._list_users()

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_for_manager_returns_only_users_and_managers(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(
            self.user1, self.user2, self.manager1, self.manager2)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._list_users()

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_for_admin_returns_users_managers_and_admins(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(
            self.user1, self.user2, self.manager1, self.manager2, self.admin1, self.admin2)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._list_users()

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_requires_authentication(self) -> None:
        # Act
        response = self._retrieve_user(self.user1.id)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_retrieve_raises_error_for_incorrect_pk(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_user(1_000_000_000)

        # Assert
        self.assertEqual(404, response.status_code)

    def test_retrieve_for_user_returns_only_themselves(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.user1, as_list=False)

        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_user(self.user1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_user_does_not_return_another_users(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_user(self.user2.id)

        # Assert
        self.assertEqual(404, response.status_code)

    def test_retrieve_for_manager_returns_users(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.user1, as_list=False)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_user(self.user1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_manager_returns_themselves(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.manager1, as_list=False)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_user(self.manager1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_manager_returns_other_managers(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.manager2, as_list=False)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_user(self.manager2.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_manager_does_not_return_admins(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_user(self.admin1.id)

        # Assert
        self.assertEqual(404, response.status_code)

    def test_retrieve_for_admin_returns_users(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.user1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_user(self.user1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_admin_returns_managers(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.manager1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_user(self.manager1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_admin_returns_themselves(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.admin1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_user(self.admin1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_for_admin_returns_other_admins(self) -> None:
        # Arrange
        expected_result = self._get_expected_users(self.admin2, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_user(self.admin2.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_create_does_not_allow_to_insert_duplicates(self) -> None:
        # Arrange
        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._create_user(self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(400, response.status_code)

    def test_create_allows_non_authenticated_users_create_users(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.USER

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertEqual(email, response.data.get('email', None))
        self.assertEqual(role, response.data.get('role', None))

    def test_create_does_not_allow_non_authenticated_users_create_managers(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.MANAGER

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_create_does_not_allow_non_authenticated_users_create_admins(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.ADMIN

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_create_does_not_allow_authenticated_users_create_users(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.USER

        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_create_allows_managers_create_users(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.USER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertEqual(email, response.data.get('email', None))
        self.assertEqual(role, response.data.get('role', None))

    def test_create_allows_managers_create_managers(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.MANAGER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertEqual(email, response.data.get('email', None))
        self.assertEqual(role, response.data.get('role', None))

    def test_create_does_not_allow_managers_create_admins(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.ADMIN

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_create_allows_admins_create_users(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.USER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertEqual(email, response.data.get('email', None))
        self.assertEqual(role, response.data.get('role', None))

    def test_create_allows_admins_create_managers(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.MANAGER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertEqual(email, response.data.get('email', None))
        self.assertEqual(role, response.data.get('role', None))

    def test_create_allows_admins_create_admins(self) -> None:
        # Arrange
        email = 'test@example.com'
        password = 'test@example.com'
        role = RoleEnum.ADMIN

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._create_user(email, password, role)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertEqual(email, response.data.get('email', None))
        self.assertEqual(role, response.data.get('role', None))

    def test_update_requires_authentication(self) -> None:
        # Act
        response = self._update_user(self.user1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_update_raises_error_for_incorrect_pk(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(1_000_00_000, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(404, response.status_code)

    def test_update_allows_users_update_themselves(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'

        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, RoleEnum.USER)
        updated_user = User.objects.get(pk=user.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(user.role, response.data.get('role'))
        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(new_email, updated_user.email)
        self.assertEqual(user.role, updated_user.role)

    def test_update_does_not_allow_users_to_update_other_users(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.user2.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_update_managers(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.manager1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_update_admins(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.admin1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_promote_themselves_to_managers(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.user1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.MANAGER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_promote_themselves_to_admins(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.user1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.ADMIN)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_promote_other_users_to_managers(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.user2.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.MANAGER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_promote_other_users_to_admins(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.user2.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.ADMIN)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_promote_managers_to_admins(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.manager1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.ADMIN)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_demote_managers_to_users(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.manager1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_demote_admins_to_users(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.admin1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.USER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_users_to_demote_admins_to_managers(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._update_user(self.admin1.id, self.USER1_EMAIL, self.USER1_PASSWORD, RoleEnum.MANAGER)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_allows_managers_update_themselves(self) -> None:
        # Arrange
        manager = self.manager1
        new_email = 'test@example.com'

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, RoleEnum(manager.role))
        updated_manager = User.objects.get(pk=manager.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(manager.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(manager.role, response.data.get('role'))
        self.assertEqual(manager.id, updated_manager.id)
        self.assertEqual(new_email, updated_manager.email)
        self.assertEqual(manager.role, updated_manager.role)

    def test_update_allows_managers_update_users(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, RoleEnum(user.role))
        updated_user = User.objects.get(pk=user.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(user.role, response.data.get('role'))
        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(new_email, updated_user.email)
        self.assertEqual(user.role, updated_user.role)

    def test_update_allows_managers_update_managers(self) -> None:
        # Arrange
        manager = self.manager1
        new_email = 'test@example.com'

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, RoleEnum(manager.role))
        updated_manager = User.objects.get(pk=manager.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(manager.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(manager.role, response.data.get('role'))
        self.assertEqual(manager.id, updated_manager.id)
        self.assertEqual(new_email, updated_manager.email)
        self.assertEqual(manager.role, updated_manager.role)

    def test_update_does_not_allow_managers_update_admins(self) -> None:
        # Arrange
        admin = self.admin1
        new_email = 'test@example.com'

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, RoleEnum(admin.role))

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_managers_promote_themselves(self) -> None:
        # Arrange
        manager = self.manager1
        new_email = 'test@example.com'
        new_role = RoleEnum.ADMIN

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_allows_managers_promote_users_to_managers(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'
        new_role = RoleEnum.MANAGER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, new_role)
        updated_user = User.objects.get(pk=user.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(new_email, updated_user.email)
        self.assertEqual(new_role, updated_user.role)

    def test_update_does_not_allow_managers_promote_users_to_admins(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'
        new_role = RoleEnum.ADMIN

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_managers_promote_managers_to_admins(self) -> None:
        # Arrange
        manager = self.manager2
        new_email = 'test@example.com'
        new_role = RoleEnum.ADMIN

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_managers_demote_themselves_to_users(self) -> None:
        # Arrange
        manager = self.manager1
        new_email = 'test@example.com'
        new_role = RoleEnum.USER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_managers_demote_managers_to_users(self) -> None:
        # Arrange
        manager = self.manager2
        new_email = 'test@example.com'
        new_role = RoleEnum.USER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_managers_demote_admins_to_users(self) -> None:
        # Arrange
        admin = self.admin1
        new_email = 'test@example.com'
        new_role = RoleEnum.USER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, new_role)

        # Assert

        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_managers_demote_admins_to_managers(self) -> None:
        # Arrange
        admin = self.admin1
        new_email = 'test@example.com'
        new_role = RoleEnum.MANAGER

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, new_role)

        # Assert

        self.assertEqual(403, response.status_code)

    def test_update_allows_admins_update_themselves(self) -> None:
        # Arrange
        admin = self.admin1
        new_email = 'test@example.com'

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, RoleEnum(admin.role))
        updated_role = User.objects.get(pk=admin.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(admin.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(admin.role, response.data.get('role'))
        self.assertEqual(admin.id, updated_role.id)
        self.assertEqual(new_email, updated_role.email)
        self.assertEqual(admin.role, updated_role.role)

    def test_update_allows_admins_update_users(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, RoleEnum(user.role))
        updated_user = User.objects.get(pk=user.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(user.role, response.data.get('role'))
        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(new_email, updated_user.email)
        self.assertEqual(user.role, updated_user.role)

    def test_update_allows_admins_update_managers(self) -> None:
        # Arrange
        manager = self.manager1
        new_email = 'test@example.com'

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, RoleEnum(manager.role))
        updated_manager = User.objects.get(pk=manager.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(manager.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(manager.role, response.data.get('role'))
        self.assertEqual(manager.id, updated_manager.id)
        self.assertEqual(new_email, updated_manager.email)
        self.assertEqual(manager.role, updated_manager.role)

    def test_update_allows_admins_update_admins(self) -> None:
        # Arrange
        admin = self.admin2
        new_email = 'test@example.com'

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, RoleEnum(admin.role))
        updated_admin = User.objects.get(pk=admin.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(admin.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(admin.role, response.data.get('role'))
        self.assertEqual(admin.id, updated_admin.id)
        self.assertEqual(new_email, updated_admin.email)
        self.assertEqual(admin.role, updated_admin.role)

    def test_update_allows_admins_promote_users_to_managers(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'
        new_role = RoleEnum.MANAGER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, new_role)
        updated_user = User.objects.get(pk=user.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(new_email, updated_user.email)
        self.assertEqual(new_role, updated_user.role)

    def test_update_allows_admins_promote_users_to_admins(self) -> None:
        # Arrange
        user = self.user1
        new_email = 'test@example.com'
        new_role = RoleEnum.ADMIN

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(user.id, new_email, new_email, new_role)
        updated_user = User.objects.get(pk=user.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(new_email, updated_user.email)
        self.assertEqual(new_role, updated_user.role)

    def test_update_allows_admins_promote_managers_to_admins(self) -> None:
        # Arrange
        manager = self.manager2
        new_email = 'test@example.com'
        new_role = RoleEnum.ADMIN

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, new_role)
        updated_manager = User.objects.get(pk=manager.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(manager.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(manager.id, updated_manager.id)
        self.assertEqual(new_email, updated_manager.email)
        self.assertEqual(new_role, updated_manager.role)

    def test_update_does_not_allow_admins_demote_themselves_to_users(self) -> None:
        # Arrange
        admin = self.admin1
        new_email = 'test@example.com'
        new_role = RoleEnum.USER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_does_not_allow_admins_demote_themselves_to_managers(self) -> None:
        # Arrange
        admin = self.admin1
        new_email = 'test@example.com'
        new_role = RoleEnum.MANAGER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, new_role)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_update_allows_admins_demote_managers_to_users(self) -> None:
        # Arrange
        manager = self.manager2
        new_email = 'test@example.com'
        new_role = RoleEnum.USER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(manager.id, new_email, new_email, new_role)
        updated_manager = User.objects.get(pk=manager.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(manager.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(manager.id, updated_manager.id)
        self.assertEqual(new_email, updated_manager.email)
        self.assertEqual(new_role, updated_manager.role)

    def test_update_allows_admins_demote_admins_to_users(self) -> None:
        # Arrange
        admin = self.admin2
        new_email = 'test@example.com'
        new_role = RoleEnum.USER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, new_role)
        updated_admin = User.objects.get(pk=admin.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(admin.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(admin.id, updated_admin.id)
        self.assertEqual(new_email, updated_admin.email)
        self.assertEqual(new_role, updated_admin.role)

    def test_update_allows_admins_demote_admins_to_managers(self) -> None:
        # Arrange
        admin = self.admin2
        new_email = 'test@example.com'
        new_role = RoleEnum.MANAGER

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._update_user(admin.id, new_email, new_email, new_role)
        updated_admin = User.objects.get(pk=admin.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(admin.id, response.data.get('id'))
        self.assertEqual(new_email, response.data.get('email'))
        self.assertEqual(new_role, response.data.get('role'))
        self.assertEqual(admin.id, updated_admin.id)
        self.assertEqual(new_email, updated_admin.email)
        self.assertEqual(new_role, updated_admin.role)

    def test_destroy_requires_authentication(self) -> None:
        # Act
        response = self._destroy_user(self.user1.id)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_destroy_allows_users_to_destroy_themselves(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._destroy_user(self.user1.id)
        deleted_user_still_exists = User.objects.filter(pk=self.user1.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_user_still_exists)

    def test_destroy_does_not_allow_users_to_destroy_other_users(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._destroy_user(self.user2.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_destroy_does_not_allow_users_to_destroy_managers(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._destroy_user(self.manager1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_destroy_does_not_allow_users_to_destroy_admins(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._destroy_user(self.admin1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_destroy_allows_managers_to_destroy_themselves(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._destroy_user(self.manager1.id)
        deleted_manager_still_exists = User.objects.filter(pk=self.manager1.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_manager_still_exists)

    def test_destroy_allows_managers_to_destroy_users(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._destroy_user(self.user1.id)
        deleted_user_still_exists = User.objects.filter(pk=self.user1.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_user_still_exists)

    def test_destroy_allows_managers_to_destroy_other_managers(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._destroy_user(self.manager2.id)
        deleted_manager_still_exists = User.objects.filter(pk=self.manager2.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_manager_still_exists)

    def test_destroy_does_not_allow_managers_to_destroy_admins(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._destroy_user(self.admin1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_destroy_allows_admins_to_destroy_themselves(self) -> None:
        # Arrange
        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._destroy_user(self.admin1.id)
        deleted_admin_still_exists = User.objects.filter(pk=self.admin1.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_admin_still_exists)

    def test_destroy_allows_admins_to_destroy_users(self) -> None:
        # Arrange
        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._destroy_user(self.user1.id)
        deleted_user_still_exists = User.objects.filter(pk=self.user1.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_user_still_exists)

    def test_destroy_allows_admins_to_destroy_other_managers(self) -> None:
        # Arrange
        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._destroy_user(self.manager2.id)
        deleted_manager_still_exists = User.objects.filter(pk=self.manager2.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_manager_still_exists)

    def test_destroy_allows_admins_to_destroy_other_admins(self) -> None:
        # Arrange
        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._destroy_user(self.admin2.id)
        deleted_admin_still_exists = User.objects.filter(pk=self.admin2.id).exists()

        # Assert
        self.assertEqual(204, response.status_code)
        self.assertFalse(deleted_admin_still_exists)


class TripViewSetTest(BaseTestCase):
    USER1_TRIP1_DESTINATION = 'Croatia'
    USER1_TRIP1_START_DATE = '2020-07-01'
    USER1_TRIP1_END_DATE = '2020-08-01'
    USER1_TRIP1_COMMENT = ''
    USER1_TRIP2_DESTINATION = 'Italy'
    USER1_TRIP2_START_DATE = '2020-08-01'
    USER1_TRIP2_END_DATE = '2020-09-01'
    USER1_TRIP2_COMMENT = ''

    USER2_TRIP1_DESTINATION = 'Thailand'
    USER2_TRIP1_START_DATE = '2020-06-01'
    USER2_TRIP1_END_DATE = '2020-07-01'
    USER2_TRIP1_COMMENT = ''
    USER2_TRIP2_DESTINATION = 'Singapore'
    USER2_TRIP2_START_DATE = '2020-06-01'
    USER2_TRIP2_END_DATE = '2020-09-01'
    USER2_TRIP2_COMMENT = ''

    MANAGER1_TRIP1_DESTINATION = 'Kenya'
    MANAGER1_TRIP1_START_DATE = '2020-06-01'
    MANAGER1_TRIP1_END_DATE = '2020-08-01'
    MANAGER1_TRIP1_COMMENT = ''
    MANAGER1_TRIP2_DESTINATION = 'USA'
    MANAGER1_TRIP2_START_DATE = '2020-08-01'
    MANAGER1_TRIP2_END_DATE = '2020-09-01'
    MANAGER1_TRIP2_COMMENT = ''

    MANAGER2_TRIP1_DESTINATION = 'UK'
    MANAGER2_TRIP1_START_DATE = '2020-06-01'
    MANAGER2_TRIP1_END_DATE = '2020-07-01'
    MANAGER2_TRIP1_COMMENT = ''
    MANAGER2_TRIP2_DESTINATION = 'Indonesia'
    MANAGER2_TRIP2_START_DATE = '2020-06-01'
    MANAGER2_TRIP2_END_DATE = '2020-09-01'
    MANAGER2_TRIP2_COMMENT = ''

    ADMIN1_TRIP1_DESTINATION = 'Poland'
    ADMIN1_TRIP1_START_DATE = '2020-06-01'
    ADMIN1_TRIP1_END_DATE = '2020-08-01'
    ADMIN1_TRIP1_COMMENT = ''
    ADMIN1_TRIP2_DESTINATION = 'Romania'
    ADMIN1_TRIP2_START_DATE = '2020-08-01'
    ADMIN1_TRIP2_END_DATE = '2020-09-01'
    ADMIN1_TRIP2_COMMENT = ''

    ADMIN2_TRIP1_DESTINATION = 'Serbia'
    ADMIN2_TRIP1_START_DATE = '2020-06-01'
    ADMIN2_TRIP1_END_DATE = '2020-07-01'
    ADMIN2_TRIP1_COMMENT = ''
    ADMIN2_TRIP2_DESTINATION = 'Slovakia'
    ADMIN2_TRIP2_START_DATE = '2020-06-01'
    ADMIN2_TRIP2_END_DATE = '2020-09-01'
    ADMIN2_TRIP2_COMMENT = ''

    def _list_trips(self, user_pk: int) -> Response:
        return self.client.get(f'/api/users/{user_pk}/trips/')

    def _retrieve_trip(self, user_pk: int, trip_pk: int) -> Response:
        return self.client.get(f'/api/users/{user_pk}/trips/{trip_pk}/')

    def _create_trip(
            self,
            user_pk: int,
            destination: str,
            start_date: datetime,
            end_date: datetime,
            comment: str) -> Response:
        return self.client.post(
            f'/api/users/{user_pk}/trips/',
            {
                'user': user_pk,
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'comment': comment
            })

    def _update_trip(self, pk: int, email: str, password: str, role: RoleEnum) -> Response:
        return self.client.put(
            f'/api/users/{pk}/',
            {
                'email': email,
                'password': password,
                'role': int(role)
            })

    def _destroy_trip(self, user_pk: int, trip_pk: int) -> Response:
        return self.client.delete(f'/api/users/{user_pk}/trips/{trip_pk}/')

    def _get_expected_trips(self, *trips: Trip, as_list: bool = True) -> bytes:
        return self._get_expected_result(TripSerializer, *trips, as_list=as_list)

    def _create_trip_instance(
            self,
            user: User,
            destination: str,
            start_date: str,
            end_date: str,
            comment: str,
            save: bool = True) -> Trip:
        trip = Trip(
            user=user,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            comment=comment)

        if save:
            trip.save()

        return trip

    def setUp(self) -> None:
        super().setUp()

        self.user1_trip1 = self._create_trip_instance(
            self.user1,
            self.USER1_TRIP1_DESTINATION,
            self.USER1_TRIP1_START_DATE,
            self.USER1_TRIP1_END_DATE,
            self.USER1_TRIP1_COMMENT)
        self.user1_trip2 = self._create_trip_instance(
            self.user1,
            self.USER1_TRIP2_DESTINATION,
            self.USER1_TRIP2_START_DATE,
            self.USER1_TRIP2_END_DATE,
            self.USER1_TRIP2_COMMENT)

        self.user2_trip1 = self._create_trip_instance(
            self.user2,
            self.USER2_TRIP1_DESTINATION,
            self.USER2_TRIP1_START_DATE,
            self.USER2_TRIP1_END_DATE,
            self.USER2_TRIP1_COMMENT)
        self.user2_trip2 = self._create_trip_instance(
            self.user2,
            self.USER2_TRIP2_DESTINATION,
            self.USER2_TRIP2_START_DATE,
            self.USER2_TRIP2_END_DATE,
            self.USER2_TRIP2_COMMENT)

        self.manager1_trip1 = self._create_trip_instance(
            self.manager1,
            self.MANAGER1_TRIP1_DESTINATION,
            self.MANAGER1_TRIP1_START_DATE,
            self.MANAGER1_TRIP1_END_DATE,
            self.MANAGER1_TRIP1_COMMENT)
        self.manager1_trip2 = self._create_trip_instance(
            self.manager1,
            self.MANAGER1_TRIP2_DESTINATION,
            self.MANAGER1_TRIP2_START_DATE,
            self.MANAGER1_TRIP2_END_DATE,
            self.MANAGER1_TRIP2_COMMENT)

        self.manager2_trip1 = self._create_trip_instance(
            self.manager2,
            self.MANAGER2_TRIP1_DESTINATION,
            self.MANAGER2_TRIP1_START_DATE,
            self.MANAGER2_TRIP1_END_DATE,
            self.MANAGER2_TRIP1_COMMENT)
        self.manager2_trip2 = self._create_trip_instance(
            self.manager2,
            self.MANAGER2_TRIP2_DESTINATION,
            self.MANAGER2_TRIP2_START_DATE,
            self.MANAGER2_TRIP2_END_DATE,
            self.MANAGER2_TRIP2_COMMENT)

        self.admin1_trip1 = self._create_trip_instance(
            self.admin1,
            self.ADMIN1_TRIP1_DESTINATION,
            self.ADMIN1_TRIP1_START_DATE,
            self.ADMIN1_TRIP1_END_DATE,
            self.ADMIN1_TRIP1_COMMENT)
        self.admin1_trip2 = self._create_trip_instance(
            self.admin1,
            self.ADMIN1_TRIP2_DESTINATION,
            self.ADMIN1_TRIP2_START_DATE,
            self.ADMIN1_TRIP2_END_DATE,
            self.ADMIN1_TRIP2_COMMENT)

        self.admin2_trip1 = self._create_trip_instance(
            self.admin2,
            self.ADMIN2_TRIP1_DESTINATION,
            self.ADMIN2_TRIP1_START_DATE,
            self.ADMIN2_TRIP1_END_DATE,
            self.ADMIN2_TRIP1_COMMENT)
        self.admin2_trip2 = self._create_trip_instance(
            self.admin2,
            self.ADMIN2_TRIP2_DESTINATION,
            self.ADMIN2_TRIP2_START_DATE,
            self.ADMIN2_TRIP2_END_DATE,
            self.ADMIN2_TRIP2_COMMENT)

    def test_list_requires_authentication(self) -> None:
        # Act
        response = self._list_trips(self.user1.id)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_list_raises_error_for_incorrect_pk(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._list_trips(1_000_000)

        # Assert
        self.assertEqual(404, response.status_code)

    def test_list_allows_users_to_list_their_own_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.user1_trip1, self.user1_trip2)

        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._list_trips(self.user1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_does_not_allow_users_to_list_other_users_trips(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._list_trips(self.user2.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_list_does_not_allow_users_to_list_manager_trips(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._list_trips(self.manager1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_list_does_not_allow_users_to_list_admin_trips(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._list_trips(self.admin1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_list_allows_managers_to_list_their_own_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.manager1_trip1, self.manager1_trip2)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._list_trips(self.manager1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_allows_managers_to_list_users_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.user1_trip1, self.user1_trip2)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._list_trips(self.user1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_does_not_allow_managers_to_list_manager_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.manager2_trip1, self.manager2_trip2)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._list_trips(self.manager2.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_does_not_allow_managers_to_list_admin_trips(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._list_trips(self.admin1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_list_allows_admins_to_list_their_own_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.admin1_trip1, self.admin1_trip2)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._list_trips(self.admin1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_allows_admins_to_list_users_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.user1_trip1, self.user1_trip2)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._list_trips(self.user1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_allows_admins_to_list_manager_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.manager2_trip1, self.manager2_trip2)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._list_trips(self.manager2.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_list_allows_admins_to_list_admin_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(
            self.admin2_trip1, self.admin2_trip2)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._list_trips(self.admin2.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_requires_authentication(self) -> None:
        # Act
        response = self._retrieve_trip(self.user1.id, self.user1_trip1.id)

        # Assert
        self.assertEqual(401, response.status_code)

    def test_retrieve_raises_error_for_incorrect_pk(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.user1.id, 1_000_000)

        # Assert
        self.assertEqual(404, response.status_code)

    def test_retrieve_allows_users_to_list_retrieve_own_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.user1_trip1, as_list=False)

        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.user1.id, self.user1_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_does_not_allow_users_to_retrieve_other_users_trips(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.user2.id, self.user2_trip1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_retrieve_does_not_allow_users_to_retrieve_manager_trips(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.manager1.id, self.manager1_trip1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_retrieve_does_not_allow_users_to_retrieve_admin_trips(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.admin1.id, self.admin1_trip1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_retrieve_allows_managers_to_retrieve_their_own_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.manager1_trip1, as_list=False)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.manager1.id, self.manager1_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_allows_managers_to_retrieve_users_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.user1_trip1, as_list=False)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.user1.id, self.user1_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_allows_managers_to_retrieve_other_manager_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.manager2_trip1, as_list=False)

        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.manager2.id, self.manager2_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_does_not_allow_managers_to_retrieve_admin_trips(self) -> None:
        # Arrange
        self._authenticate(self.MANAGER1_EMAIL, self.MANAGER1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.admin1.id, self.admin1_trip1.id)

        # Assert
        self.assertEqual(403, response.status_code)

    def test_retrieve_allows_admins_to_retrieve_their_own_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.admin1_trip1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.admin1.id, self.admin1_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_allows_admins_to_retrieve_users_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.user1_trip1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.user1.id, self.user1_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_allows_admins_to_retrieve_manager_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.manager2_trip1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.manager2.id, self.manager2_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_retrieve_allows_admins_to_retrieve_other_admin_trips(self) -> None:
        # Arrange
        expected_result = self._get_expected_trips(self.admin2_trip1, as_list=False)

        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._retrieve_trip(self.admin2.id, self.admin2_trip1.id)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.content)
        self.assertEqual(expected_result, response.content)

    def test_create_requires_authentication(self) -> None:
        # Act
        response = self._create_trip(self.user1.id, 'Hawaii', '2020-09-01', '2020-10-01', '')

        # Assert
        self.assertEqual(401, response.status_code)

    def test_create_allows_users_to_create_trips_for_themselves(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._create_trip(self.user1.id, 'Hawaii', '2020-09-01', '2020-10-01', '')

        # Assert
        self.assertEqual(201, response.status_code)

    def test_create_does_not_allow_users_to_create_trips_for_other_users(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._create_trip(self.user2.id, 'Hawaii', '2020-09-01', '2020-10-01', '')

        # Assert
        self.assertEqual(403, response.status_code)

    def test_create_does_not_allow_users_to_create_trips_for_managers(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._create_trip(self.manager1.id, 'Hawaii', '2020-09-01', '2020-10-01', '')

        # Assert
        self.assertEqual(403, response.status_code)

    def test_create_does_not_allow_users_to_create_trips_for_admins(self) -> None:
        # Arrange
        self._authenticate(self.USER1_EMAIL, self.USER1_PASSWORD)

        # Act
        response = self._create_trip(self.admin1.id, 'Hawaii', '2020-09-01', '2020-10-01', '')

        # Assert
        self.assertEqual(403, response.status_code)

    def test_destroy_allows_admins_to_destroy_user_trips(self) -> None:
        # Arrange
        self._authenticate(self.ADMIN1_EMAIL, self.ADMIN1_PASSWORD)

        # Act
        response = self._destroy_trip(self.user1.id, self.user1_trip1.id)

        # Assert
        self.assertEqual(204, response.status_code)
