from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_nested.routers import NestedSimpleRouter

from project.api.views import (CurrentUserView, LogoutView, TripViewSet,
                               UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
users_router = NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'trips', TripViewSet, basename='user-trips')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('auth/obtain_token/', obtain_jwt_token),
    path('auth/refresh_token/', refresh_jwt_token),
    path('auth/user/', CurrentUserView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]
