import datetime
import logging

import django_filters
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views import View
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import RoleEnum, Trip, User
from .policies import TripAccessPolicy, UserAccessPolicy
from .serializers import TripSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """

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

    authentication_class = (JSONWebTokenAuthentication,)
    permission_classes = (UserAccessPolicy,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (UserFilterBackend,)


class CurrentUserView(APIView):
    authentication_class = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> JsonResponse:
        serializer = UserSerializer(request.user)

        return JsonResponse(serializer.data, safe=False)


class LogoutView(APIView):
    authentication_class = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> JsonResponse:
        return JsonResponse(data={})


class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited.
    """

    class TripFilter(django_filters.FilterSet):
        class Meta:
            model = Trip
            fields = {
                'user': ['exact'],
                'destination': ['exact', 'contains'],
                'start_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
                'end_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
                'comment': ['contains']
            }

    authentication_class = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated, TripAccessPolicy)
    serializer_class = TripSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = TripFilter

    def get_queryset(self):
        return Trip.objects.filter(user=self.kwargs['user_pk'])

    def create(self, request: Request, *args, **kwargs) -> Response:
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # start_date = datetime.datetime( serializer.data['start_date']
        # end_date = serializer.data['end_date']
        #
        # if start_date > end_date:
        #     raise APIException(code=400)

        return super().create(request)

