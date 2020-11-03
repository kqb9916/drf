from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your views here.
# from rest_framework.authentication import
from rest_framework.filters import SearchFilter, OrderingFilter
from api.authentication import JWTAuthentication
from api.models import Computer
from api.serializer import UserModelSerializer, ComputerModelSerializer


class UserDetailAPIView(APIView):

    """
    只能登录以后在访问
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        return Response("ok")


# 自定义
class LoginAPIView(APIView):
    '''
    实现多方式登录
    1.禁用权限和认证组件
    2.获取前端传递的参数
    3.校验传递的参数 来得到对应的用户
    4.签发token并返回
    '''
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        # 前端账号来传递用户标识 account 密码使用password
        # account = request.data.get("account")

        serializer = UserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer)

        data = {
            "token": serializer.token,
            "user": UserModelSerializer(serializer.obj).data
        }
        print(data)
        return Response(data)


class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerModelSerializer
    # 通过filter_backends来配置你要使用的过滤类
    filter_backends = [SearchFilter, OrderingFilter]
    # 指定你要搜索的字段|条件
    search_fields =['name', 'price']
    # 指定排序的条件
    # ordering = ['price']








