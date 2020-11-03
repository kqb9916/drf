from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token

from api import views

urlpatterns = [
    path("login/", ObtainJSONWebToken.as_view()),
    # 等同
    # path("login/", obtain_jwt_token),
    path("detail/", views.UserDetailAPIView.as_view()),
    path("user/", views.LoginAPIView.as_view()),
    path("com/", views.ComputerListAPIView.as_view()),
]