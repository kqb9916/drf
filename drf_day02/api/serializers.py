from django.conf import settings
from rest_framework import serializers

from api.models import Employee


class EmployeeSerializer(serializers.Serializer):
    """
    定义序列化器类:  需要为每一个model编写对应的序列化器类
    """
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    # 自定义字段  使用SerializerMethodField来完成自定义
    aaa = serializers.SerializerMethodField()

    # 为自定义字段提供值的方法
    # 自定义字段的属性名随意  但是为字段提供值的方法必须是 get_字段名
    # self是当前序列化器对象 obj是当前被序列化的对象
    def get_aaa(self, obj):
        return "aaa"

    # 自定义性别
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        # gender 值是choices类型 get_字段名_display直接访问值
        print(obj.get_gender_display())
        return obj.get_gender_display()

    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        print(obj.pic)
        # http://127.0.0.1:8000/media/pic/3.jpg
        # print("http://127.0.0.1:8000/" + settings.MEDIA_URL + str(obj.pic))
        return "%s%s%s" % ("http://127.0.0.1:8000/", settings.MEDIA_URL, str(obj.pic))


class EmployeeDeSerializer(serializers.Serializer):
    """
    反序列化: 将前端提交的数据保存到数据库
    1. 需要前端提供哪些字段
    2. 对字段进行安全校验
    3. 有没有字段需要额外的校验
    反序列化不需要自定义字段
    """

    # 添加校验规则
    username = serializers.CharField(
        max_length=3,
        min_length=2,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField()

    # 如果想要完成对象的新增 必须重写create方法
    # self是序列化器对象  validated_data需要保存的数据
    def create(self, validated_data):
        print(self)
        print(validated_data)
        return Employee.objects.create(**validated_data)
