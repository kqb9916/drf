from rest_framework import serializers

from api.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "pic", "address")



class BookModelSerializer(serializers.ModelSerializer):

    # TODO 自定义连表查询  查询图书时可以将图书对应的出版社的信息查询出来
    # 在一个序列化器内可以嵌套另外一个序列化器类来完成多表查询
    # 序列化器对应的字段必须是当前模型类中的外键
    publish = PressModelSerializer()
    class Meta:
        # 指定当前序列化器类要序列化的模型
        model = Book

        # 指定要序列化的字段
        fields = ("book_name", "price", "pic", "publish")
        # fields = ("book_name", "price", "pic", "press_name", "author_list")
        # fields = ("book_name", "price", "pic", "aaa")

        # 直接序列化所有的字段
        # fields = "__all__"

        # 指定不展示哪些字段
        # exclude = ("is_delete", "status", "create_time")

        # 指定查询的深度
        # depth = 1


class BookDeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")

        # 添加DRF提供的默认校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,  # 必填字段
                "min_length": 2,  # 最小长度
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能小于两个字符"
                }
            },
            "price":{
                "required": True,
            }
        }
    def validate(self, attrs):
        # 书名
        print(attrs)
        return attrs

    def validate_book_name(self, obj):
        # obj对象
        print(obj)
        return obj

class BookListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成更新多个对象
    """
    # 重写update方法
    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        # instance 是要修改的对象  ； validated_data  是要修改的值

        # TODO 将修改多个变成循环中每次修改一个
        for index, obj in enumerate(instance):
            # 没遍历一次 就修改一个对象的数据
            self.child.update(obj.validated_data[index])

        return instance


# 序列化器与反序列化器整合
class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # 应该填写序列化与反序列化所需字段的并集
        fields = ("book_name", "price", "publish", "authors", "pic")
        extra_kwargs = {
            "book_name": {
                "required": True,  # 必填字段
                "min_length": 2,  # 最小长度
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            },
            # 指定某个字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
        }

        list_serializer_class = BookListSerializer
        def validate(self, attrs):
            print(attrs)
            return attrs

        def validate_book_name(self, obj):
            print(obj)
            return obj



