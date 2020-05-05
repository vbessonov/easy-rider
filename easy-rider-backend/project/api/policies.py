import logging
from functools import reduce
from typing import Optional

from rest_access_policy import AccessPolicy
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.request import Request

from .models import RoleEnum, User


class BaseAccessPolicy(AccessPolicy):
    """
    Class used as a base for all other access policies
    """

    def __init__(self) -> None:
        self._logger: logging.Logger = logging.getLogger(__name__)

    def _check_user_role_condition(
            self,
            condition: str,
            request: Request,
            view: GenericAPIView,
            action: str,
            allowed_for_authors: bool,
            roles: Optional[RoleEnum] = None) -> bool:
        """
        Checks that specific action is allowed depending on the parameters

        :param condition: Name of the policy condition to be checked
        :param request: Incoming request
        :param view: Django REST view
        :param action: Django REST view action
        :param allowed_for_authors: Boolean value indicating whether the action is allowed for authors
               (users created the record)
        :param roles: Optional parameter containing a combination of roles to be checked
        :return: Boolean value indicating whether @action is allowed
        """

        self._logger.debug(f'Started evaluating {condition} policy condition')

        try:
            result = False

            if allowed_for_authors:
                url_arguments = request.parser_context['kwargs']

                self._logger.debug(f'URL arguments: {url_arguments}')

                user_id = url_arguments['user_pk']
                user = get_object_or_404(User, id=user_id)
                result = user == request.user

            if roles is not None:
                result |= RoleEnum(request.user.role) in roles

            self._logger.debug(f'{condition} policy condition has been successfully evaluated: {result}')

            return result
        except Exception:
            self._logger.exception(
                f'An unexpected exception occurred while evaluating {condition} policy condition')
            raise

    def is_privileged(self, request: Request, view: GenericAPIView, action: str) -> bool:
        """
        Checks that specific action is allowed only for authors (users who created the record)
        and privileged users (managers and admins)

        :param request: Incoming request
        :param view: Django REST view
        :param action: Django REST view action
        :return: Boolean value indicating whether @action is allowed
        """

        return self._check_user_role_condition(
            'is_author_or_privileged', request, view, action, False, RoleEnum(RoleEnum.MANAGER | RoleEnum.ADMIN))

    def is_author_or_privileged(self, request: Request, view: GenericAPIView, action: str) -> bool:
        """
        Checks that specific action is allowed only for authors (users who created the record)
        and privileged users (managers and admins)

        :param request: Incoming request
        :param view: Django REST view
        :param action: Django REST view action
        :return: Boolean value indicating whether @action is allowed
        """

        return self._check_user_role_condition(
            'is_author_or_privileged', request, view, action, True, RoleEnum(RoleEnum.MANAGER | RoleEnum.ADMIN))

    def is_author_or_admin(self, request: Request, view: GenericAPIView, action: str) -> bool:
        """
        Checks that specific action is allowed only for authors (users who created the record)
        and admins

        :param request: Incoming request
        :param view: Django REST view
        :param action: Django REST view action
        :return: Boolean value indicating whether @action is allowed
        """

        return self._check_user_role_condition(
            'is_author_or_privileged', request, view, action, True, RoleEnum.ADMIN)

    def _parse_role(self, role: str) -> RoleEnum:
        return reduce(
            lambda role1, role2: role1 | role2,
            [RoleEnum[role_item] for role_item in role.split('|')]
        )

    def _get_user_pk(self, request: Request) -> int:
        return int(request.parser_context.get('kwargs', {}).get('pk', 0))

    def requested_user_is_originator(self, request: Request, view: GenericAPIView, action: str) -> bool:
        """
        Checks whether a requested user is the same as originator of the request
        :param request: Incoming request
        :param view: Django view
        :param action: Requested action
        :return: Boolean value indicating whether the requested action is allowed
        """

        return request.user.id == self._get_user_pk(request)

    def requested_user_has_one_of_roles(self, request: Request, view: GenericAPIView, action: str, roles: str) -> bool:
        """
        Checks whether a requested user has one of the requested roles
        :param request: Incoming request
        :param view: Django view
        :param action: Requested action
        :param roles: Requested roles
        :return: Boolean value indicating whether the requested action is allowed
        """

        try:
            requested_user = User.objects.get(pk=self._get_user_pk(request))

            return RoleEnum(requested_user.role) in self._parse_role(roles)
        except User.DoesNotExist:
            raise NotFound()

    def requested_role_is_one_of(self, request: Request, view: GenericAPIView, action: str, roles: str) -> bool:
        """
        Checks whether a role specified in the request is one of the requested
        :param request: Incoming request
        :param view: Django view
        :param action: Requested action
        :param roles: Requested roles
        :return: Boolean value indicating whether the requested action is allowed
        """

        return RoleEnum(int(request.data.get('role', RoleEnum.USER))) in self._parse_role(roles)

    def requested_role_is_the_same_as_originators(self, request: Request, view: GenericAPIView, action: str) -> bool:
        """
        Checks whether a role specified in the request is the same as originator's one
        :param request: Incoming request
        :param view: Django view
        :param action: Requested action
        :return: Boolean value indicating whether the requested action is allowed
        """

        return RoleEnum(int(request.data.get('role', RoleEnum.USER))) == RoleEnum(request.user.role)

    def originator_has_one_of_roles(self, request: Request, view: GenericAPIView, action: str, roles: str) -> bool:
        """
        Checks whether the originator of the request have one of the requested roles
        :param request: Incoming request
        :param view: Django view
        :param action: Requested action
        :param roles: Requested roles
        :return: Boolean value indicating whether the requested action is allowed
        """

        return RoleEnum(request.user.role) in self._parse_role(roles)


class UserAccessPolicy(BaseAccessPolicy):
    """
    Policy class for user-related views. It allows all actions only for privileged users (managers and admins)
    """

    statements = [
        # Listing is allowed for all authenticated users
        # NOTE: There should be additional filtering logic which, for example, will filter out admins and managers
        #       in the case of a request made by USER
        {
            'action': 'list',
            'principal': 'authenticated',
            'effect': 'allow'
        },

        # USERs are allowed to retrieve only themselves
        {
            'action': 'retrieve',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': 'requested_user_is_originator'
        },
        # MANAGERs are allowed to retrieve only USERs and other MANAGERs
        {
            'action': 'retrieve',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_role_is_one_of:USER|MANAGER'
            ]
        },
        # ADMINs are allowed to retrieve all users
        {
            'action': 'retrieve',
            'principal': 'authenticated',
            'effect': 'allow'
        },

        # Anonymous users are allowed to create new USERs
        {
            'action': 'create',
            'principal': 'anonymous',
            'effect': 'allow',
            'condition': 'requested_role_is_one_of:USER'
        },
        # Authenticated USERs are NOT allowed to create new USERs
        {
            'action': 'create',
            'principal': 'authenticated',
            'effect': 'deny',
            'condition': 'originator_has_one_of_roles:USER'
        },
        # MANAGERs are allowed to create new USERs and MANAGERs
        {
            'action': 'create',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_role_is_one_of:USER|MANAGER'
            ]
        },
        # ADMINs are allowed to create all kind of users
        {
            'action': 'create',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': 'originator_has_one_of_roles:ADMIN'
        },

        # Update operations are always allowed for originators
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'requested_user_is_originator',
                'requested_role_is_the_same_as_originators'
            ]
        },
        # MANAGERs are allowed to update USERs. However, USERs can only be promoted to MANAGERs
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_has_one_of_roles:USER',
                'requested_role_is_one_of:USER|MANAGER'
            ]
        },
        # MANAGERs are allowed to update other MANAGERs. However, MANAGERs cannot be promoted or demoted
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_has_one_of_roles:MANAGER',
                'requested_role_is_one_of:MANAGER'
            ]
        },
        # ADMINs are NOT allowed to demote themselves
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'deny',
            'condition': [
                'originator_has_one_of_roles:ADMIN',
                'requested_user_is_originator',
                'requested_role_is_one_of:USER|MANAGER'
            ]
        },
        # ADMINs are allowed to update any other users
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': 'originator_has_one_of_roles:ADMIN'
        },

        # Destroy operations are always allowed for originators
        {
            'action': 'destroy',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'requested_user_is_originator',
                'requested_role_is_the_same_as_originators'
            ]
        },
        # MANAGERs are allowed to delete USERs and other MANAGERs
        {
            'action': 'destroy',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_has_one_of_roles:USER|MANAGER'
            ]
        },
        # ADMINs are allowed to delete any user
        {
            'action': 'destroy',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': 'originator_has_one_of_roles:ADMIN'
        }
    ]


class TripAccessPolicy(BaseAccessPolicy):
    """
    Policy class for trip-related views. It allows all actions only for authors and admins
    """

    statements = [
        # List and retrieve operations allow USERs to list only their own trips
        {
            'action': ['list', 'retrieve'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:USER',
                'requested_user_is_originator'
            ]
        },
        # List and retrieve operations allow MANAGERs to list their own trips, USERs' trips and other MANAGERs' trips
        {
            'action': ['list', 'retrieve'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_is_originator'
            ]
        },
        # List allows ADMINs to list everybody's trips
        {
            'action': ['list', 'retrieve'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:ADMIN'
            ]
        },

        # Create allows USERs to create trips only for themselves
        {
            'action': 'create',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:USER',
                'requested_user_is_originator'
            ]
        },
        # Create allows MANAGERs to create trips only for themselves
        {
            'action': 'create',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_is_originator'
            ]
        },
        # Create allows ADMINs to create trips for everybody
        {
            'action': 'create',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:ADMIN'
            ]
        },

        # Update allows USERs to update only their own trips
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:USER',
                'requested_user_is_originator'
            ]
        },
        # Update allows MANAGERs to update only their own trips
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_is_originator'
            ]
        },
        # Update allows ADMINs to update everybody's trips
        {
            'action': ['update', 'partial_update'],
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:ADMIN'
            ]
        },

        # Destroy allows USERs to delete only their own trips
        {
            'action': 'destroy',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:USER',
                'requested_user_is_originator'
            ]
        },
        # Destroy allows MANAGERs to delete only their own trips
        {
            'action': 'destroy',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:MANAGER',
                'requested_user_is_originator'
            ]
        },
        # Destroy allows ADMINs to delete everybody's trips
        {
            'action': 'destroy',
            'principal': 'authenticated',
            'effect': 'allow',
            'condition': [
                'originator_has_one_of_roles:ADMIN'
            ]
        }
    ]

    def _get_user_pk(self, request: Request) -> int:
        return int(request.parser_context.get('kwargs', {}).get('user_pk', 0))
