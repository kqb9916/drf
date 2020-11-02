from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from api.models import User

"""
1. 继承BaseAuthentication类
2. 重写authenticate方法
3. 自定义认证规则
"""

class MyAuth(BaseAuthentication):
    """
    前端发送请求必须携带 认证信息  需要按照一定的格式来
    默认使用Authorization来携带认证信息
    认证信息都包含在 request.META中
    """
    def authenticate(self, request):
        # 获取认证信息
        # print(request.META)
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        print("auth:", auth)


        if auth is None:  # 游客
            return None

        # 设置认证信息的校验规则 ”auth 认证信息“
        auth_split = auth.split()
        print("auth[0]:", auth_split[0].lower(), "auth[1]:", auth_split[1])
        # 校验规则
        if not (len(auth_split) == 2 and auth_split[0].lower() == "auth"):
            raise exceptions.AuthenticationFailed("认证信息有误，认证失败")
        # 如果认证成功 开始解析用户 规定用户信息必须是什么  这里规定为：abc.kqb.123
        if auth_split[1] != "abc.kqb.123":
            raise exceptions.AuthenticationFailed("用户信息认证失败")
        # 校验数据库是否存在此用户
        user = User.objects.filter(username="kqb").first()

        if not user:
            raise exceptions.AuthenticationFailed("用户不存在或者已删除")
        return user, None




