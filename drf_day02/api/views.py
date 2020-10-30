from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Student, Employee
from api.serializers import EmployeeSerializer, EmployeeDeSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):

    def get(self, request, *args, **kwargs):
        print("get Success")
        username = request.GET.get("username")
        print(username)

        return HttpResponse("GET OK")

    def post(self, request, *args, **kwargs):
        print("post Success")
        get = request.POST.get("username")
        print(get)
        return HttpResponse("POST OK")


class StudentAPIView(APIView):
    # 为某个视图单独指定渲染器  局部使用
    # 局部配置的优先级高于全局配置
    # renderer_classes = (BrowsableAPIRenderer, JSONRenderer)
    # parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        print("get Success")
        # WSGI request
        print(request._request.GET.get("email"))  # 不推荐
        # restframework.views.Request
        print(request.GET.get("email"))
        # 通过DRF扩展的方式来获取参数
        print(request.query_params.get("pwd"))  # DRF扩展的获取参数的方式

        stu_id = kwargs.get("id")

        stu_obj = Student.objects.get(pk=stu_id)

        print(stu_obj)

        return Response("GET OK")

    def post(self, request, *args, **kwargs):
        print("post Success")
        print(request._request.POST.get("email"))
        print(request.POST.get("email"), "1111")
        # 可以获取前端传递各种类型的参数  DRF扩展的  兼容性最强
        print(request.data)

        return Response("POST OK")


class EmployeeAPIView(APIView):

    def get(self, request, *args, **kwargs):

        emp_id = kwargs.get("id")

        if emp_id:
            # 查询单个
            emp_obj = Employee.objects.get(pk=emp_id)

            # 使用序列化器完成对象的序列化
            # .data 将序列化器中的数据打包成字典返回
            employee_serializer = EmployeeSerializer(emp_obj).data

            return Response({
                "status": 200,
                "message": "查询单个员工成功",
                "results": employee_serializer
            })

        else:
            employee_objects_all = Employee.objects.all()

            # 在序列化多个对象时  需要制定属性many=True
            emp_data = EmployeeSerializer(employee_objects_all, many=True).data
            print(emp_data)

            return Response({
                "status": 200,
                "message": "查询所有员工成功",
                "results": emp_data
            })

    def post(self, request, *args, **kwargs):

        # 获取前端传递的参数
        request_data = request.data

        # 前端传递的数据进行入库时  需要判断数据的格式是否合法
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 400,
                "message": "参数有误",
            })

        # 使用序列化器完成数据库的反序列化
        # 在数据进行反序列化的时候需要指定关键字 data
        serializer = EmployeeDeSerializer(data=request_data)

        # 需要对反序列化的数据进行校验  通过is_valid() 方法来对传递过来的参数进行校验  校验合法时才会返回True
        if serializer.is_valid():
            # 调用save()方法进行数据的保存  必须重写create()方法
            emp_ser = serializer.save()
            print(emp_ser)
            return Response({
                "status": 200,
                "message": "员工添加成功",
                "results": EmployeeSerializer(emp_ser).data
            })
        else:

            return Response({
                "status": 400,
                "message": "员工添加失败",
                # 保存失败的信息会包含在 .errors中
                "results": serializer.errors
            })

