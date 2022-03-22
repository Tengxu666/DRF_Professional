from django.urls import path
# from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('user', views.UserViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('user/signup', views.UserSignupAPIView.as_view()),
    path('user/signin', views.UserSigninAPIView.as_view())
]
