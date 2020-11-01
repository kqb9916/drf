from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from api.models import Book
from api.serializers import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")

        if book_id:
            book = Book.objects.get(pk=book_id)
            data = BookModelSerializer(book).data

            return Response({
                "statue": 200,
                "message": "查询单本成功",
                "results": data,
            })
        else:
            book_objects_all = Book.objects.all()
            book_ser = BookModelSerializer(book_objects_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询多本图书成功",
                "results": book_ser,
            })


    def post(self, request, *args, **kwargs):
        request_data = request.data

        serializer = BookDeModelSerializer(data=request_data)
        #  判断是否抛异常
        serializer.is_valid(raise_exception=True)

        book_obj = serializer.save()

        return Response({
            "status": 200,
            "message": "新增单本图书成功",
            "results": BookModelSerializer(book_obj).data,
        })


class BookAPIViewV2(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")

        if book_id:
            book = Book.objects.get(pk=book_id, is_delete=False)
            data = BookModelSerializerV2(book).data

            return Response({
                "statue": 200,
                "message": "查询单本成功",
                "results": data,
            })
        else:
            book_objects_all = Book.objects.all()
            book_ser = BookModelSerializerV2(book_objects_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询多本图书成功",
                "results": book_ser,
            })


    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):  #单个对象
            many = False
        elif isinstance(request_data, list):  # 多个对象 [{},{}] 列表中嵌套的是一个个图书对象
            many = True
        else:
            return Response({
                "status": 400,
                "message": "参数格式有误"
            })
        serializer = BookDeModelSerializer(data=request_data, many=many)
        #  判断是否抛异常
        serializer.is_valid(raise_exception=True)

        book_obj = serializer.save()

        return Response({
            "status": 200,
            "message": "新增单本图书成功",
            "results": BookModelSerializerV2(book_obj, many=many).data,
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")

        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        print(response)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })
        return Response({
            "status": 400,
            "message": "删除失败或者图书不存在"
        })

    def put(self, request, *args, **kwargs):
        '''
        修改对象时,在调用序列化器验证数据时必须指定`instance`关键字
        在调用serializer.save() 底层是通过`ModelSerializer`内部的`update()`方法来完成的更新
        可以在序列化器通过重写`update()`方法来完成自定义更新
        更新单个局部只需要指定参数`partial=True`即可
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        # 获取要修改的对象的值
        request_data = request.data
        # 获取要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": "图书不存在"
            })

        # 只有涉及到数据的改变 更新的时候需要对前端传递的数据进行安全校验
        # 更新的时候需要指定关键字参数data
        # TODO 如果是修改  需要自定关键字参数instance  指定你要修改的实例对象是哪一个

        serializer = BookModelSerializerV2(data=request_data, instance=book_obj)
        serializer.is_valid(raise_exception=True)

        # 经过序列化器对全局钩子与局部钩子校验后开始更新
        serializer.save()
        return Response({
            "status": 200,
            "message": '修改成功',
            "results": BookModelSerializerV2(book_obj).data
        })


    # def patch(self, request, *args, **kwargs):
    #     """
    #     整体修改单个:  修改一个对象的全部字段
    #     修改对象时,在调用序列化器验证数据时必须指定instance关键字
    #     在调用serializer.save() 底层是通过ModelSerializer内部的update()方法来完成的更新
    #     """
    #
    #     # 获取要修改的对象的值
    #     request_data = request.data
    #     # 获取要修改的图书的id
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except Book.DoesNotExist:
    #         return Response({
    #             "status": 400,
    #             "message": '图书不存在'
    #         })
    #
    #     # 更新的时候需要对前端传递的数据进行安全校验
    #     # 更新的时候需要指定关键字参数data
    #     # TODO 如果是修改  需要自定关键字参数instance  指定你要修改的实例对象是哪一个
    #     serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 经过序列化器对   全局钩子与局部钩子校验后  开始更新
    #     serializer.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": '修改成功',
    #         "results": BookModelSerializerV2(book_obj).data
    #     })

    # 群体修改  :  修改多个整体  修改局部多个
    def patch(self, request, *args, **kwargs):
        """
        单个: id 传递的修改的内容   1 {book_name: "python"}
        多个: 多个id  多个值(request.data)  超过一个id就无法通过路由传递
        id与值相匹配   [{pk:1, book_name:"python"},{pk:2, price:300},{pk:3, publish:3}]
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.data
        book_id = kwargs.get("id")
        if book_id and isinstance(request_data, dict):
            # 修改单个  将单个修改改变为群体修改一个
            book_ids = [book_id]
        elif not book_id and isinstance(request_data, list):
            # 修改多个  将所有的要修改的图书的id取出放入 book_ids
            book_ids = []
            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在"
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "参数格式有误"
            })
        print(request_data)
        print(book_ids)
        # TODO 需要判断传递过来的id所对应的图书是否存在  对book_id和request_data进行筛选
        # TODO 如果id对应的图书不存在  移除id  id对应的request_data也需要移除
        book_list = []  # 所有要修改的图书对象
        new_data = []  # 图书对象对应的要修改的值
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
            except Book.DoesNotExist:
                # 图书对象不存在 则将id与对应的数据移除
                # index = book_ids.index(pk)
                # request_data.pop(index)
                continue

        book_ser = BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        })


# GenericAPIView继承自APIView  两者完全兼容
# GenericAPIView在APIView基础上完成了哪些事情
class BookGenericAPIView(GenericAPIView,
                         mixins.ListModelMixin,  # 查询所有
                         mixins.RetrieveModelMixin,  # 查询单个
                         mixins.DestroyModelMixin,  # 删除单个
                         mixins.CreateModelMixin,   # 创建单个对象
                         mixins.UpdateModelMixin):  # 更新单个
    # 获取当前视图要操作的模型数据
    queryset = Book.objects.filter()
    # 获取当前视图要使用的序列化器
    serializer_class = BookModelSerializerV2

    lookup_field = "pk"
    def get(self, request, *args, **kwargs):
        # 查询单个  查询所有
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


    # def get(self, request, *args, **kwargs):
    #
    #     # 获取book模型中的所有数据
    #     # book_list = Book.objects.filter(is_delete=False)
    #     book_list = self.get_queryset()
    #
    #     # 获取序列化器
    #     # data = BookModelSerializerV2(book_list, many=True).data
    #     serializer = self.get_serializer(book_list, many=True)
    #     serializer_data = serializer.data
    #     return Response({
    #         "status": 200,
    #         "message": "查询所有图书成功",
    #         "results": serializer_data,
    #     })

    # def get(self, request, *args, **kwargs):
    #
    #     book_obj = self.get_object()
    #     print(book_obj)
    #     serializer = self.get_serializer(book_obj, many=False).data
    #     print(serializer)
    #
    #     return Response({
    #         "status": 200,
    #         "message": "查询单个图书成功",
    #         "results": serializer,
    #     })



# 继承generics.CreateAPIView...， 创建两个对象 queryset和serializer_class
class BookGenericAPIViewV2(generics.CreateAPIView,
                           generics.ListAPIView,
                           generics.RetrieveAPIView,
                           generics.DestroyAPIView,
                           generics.UpdateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializerV2


"""
发起一个post请求  不想执行标准的http操作的情况下完成登录
允许开发者自定义方法函数  
"""
class BookViewSetView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializerV2
    def user_login(self, request, *args, **kwargs):
        # 可以在此完成登录的逻辑
        print("登录成功")
        return Response("登录成功")


    def get_user_count(self, request, *args, **kwargs):
        # 完成获取用户数量的逻辑
        print("查询成功")
        return self.list(request, *args, **kwargs)
















