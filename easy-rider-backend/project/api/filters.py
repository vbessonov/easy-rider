import logging

from django.db.models import Q, QuerySet
from django.views import View
from rest_framework import filters
from rest_framework.request import Request

from project.api.models import RoleEnum


class UserFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def __init__(self) -> None:
        self._logger: logging.Logger = logging.getLogger(__name__)

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View) -> QuerySet:
        if request.user.role == RoleEnum.USER:
            return queryset.filter(id=request.user.id)
        elif request.user.role == RoleEnum.MANAGER:
            return queryset.filter(Q(role=int(RoleEnum.USER)) | Q(role=int(RoleEnum.MANAGER)))
        elif request.user.role == RoleEnum.ADMIN:
            return queryset
        else:
            self._logger.error(f'Unknown role {request.user.role}')

            return queryset.none()


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View) -> QuerySet:
        return queryset.filter(owner=request.user)
