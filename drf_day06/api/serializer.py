from rest_framework.serializers import ModelSerializer
import re
from rest_framework import serializers
# from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.settings import api_settings
from api.models import User, Computer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserModelSerializer(ModelSerializer):

    """
    前端发送请求  传递参数  但数据不需要保存至数据
    反序列化的过程中，有些字段只参与反序列化的业务，并不会保存到数据中，模型也没有对应的字段
    """
    # 自定义反序列化字段  代表这个字段只参与反序列化  且不会要求这个字段与model类进行映射
    account = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["account", "password", "username", "phone", "email"]

        extra_kwargs = {
            "username": {
                "read_only": True
            },
            "phone": {
                "read_only": True
            },
            "email": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        account = attrs.get("account")
        password = attrs.get("password")

        # 对各种 登录方式进行处理
        if re.match(r'1[3-9][0-9]{9}', account):
            user_obj = User.objects.filter(phone=account).first()
        elif re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()

        # 判断用户是否存在
        if user_obj and user_obj.check_password(password):
            # 签发token
            """
            根据用户信息生成荷载  根据荷载生成token
            """
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            self.obj = user_obj
            self.token = token
            # print(payload, token,attrs)

        return attrs


class ComputerModelSerializer(ModelSerializer):

    class Meta:
        model = Computer
        fields =("name", "price", "brand")