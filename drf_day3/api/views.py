from rest_framework.response import Response
from rest_framework.views import APIView

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


    def patch(self, request, *args, **kwargs):
        """
        整体修改单个:  修改一个对象的全部字段
        修改对象时,在调用序列化器验证数据时必须指定instance关键字
        在调用serializer.save() 底层是通过ModelSerializer内部的update()方法来完成的更新
        """

        # 获取要修改的对象的值
        request_data = request.data
        # 获取要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": '图书不存在'
            })

        # 更新的时候需要对前端传递的数据进行安全校验
        # 更新的时候需要指定关键字参数data
        # TODO 如果是修改  需要自定关键字参数instance  指定你要修改的实例对象是哪一个
        serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        serializer.is_valid(raise_exception=True)

        # 经过序列化器对   全局钩子与局部钩子校验后  开始更新
        serializer.save()

        return Response({
            "status": 200,
            "message": '修改成功',
            "results": BookModelSerializerV2(book_obj).data
        })




