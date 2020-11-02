from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from api.authentications import MyAuth
from api.models import User
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

from api.permissions import MyPermission
from api.throttle import SendMessageRate


class Demo(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.first()
        print(user)
        print(user.groups.first(), "通过用户看角色")
        print(user.user_permissions.first(), "看看权限")
        return Response("ok")


class UserAPIView(APIView):

    # authentication_classes = [MyAuth]
    # 权限组件的功能依赖于认证组件 负责无法工作
    # permission_classes = [IsAuthenticated]
    # permission_classes = [MyPermission]

    throttle_classes = [SendMessageRate]

    def get(self, request, *args, **kwargs):
        print("读请求")
        return Response("读请求")