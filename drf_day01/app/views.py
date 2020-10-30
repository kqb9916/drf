from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User


@csrf_exempt
def user(request):
    if request.method == "GET":
        username = request.GET.get("username")
        print(username)
        print("GET 查询")
        return HttpResponse("GET ok")
    if request.method == "POST":
        print("POST 新增")
        return HttpResponse("POST ok")
    if request.method == "PUT":
        print("PUT 修改")
        return HttpResponse("PUT ok")
    if request.method == "DELETE":
        print("DELETE 删除")
        return HttpResponse("DELETE ok")



# 添加csrf验证
# @method_decorator(csrf_protect, name="dispatch")
# 免除csrf验证
@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):

    def get(self, request, *args, **kwargs):
        """
        提供查询单个用户以及  多个用户的接口
        :param request:  请求对象
        :param args:
        :param kwargs:
        :return: 返回查询结果
        """
        user_id = kwargs.get("id")
        if user_id:
            user_val = User.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_val:
                #  如果查询出用户信息，则返回前端
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_val
                })
        else:
            #  用户id不存在   查询所有用户信息
            user_objects_all = User.objects.all().values("username", "password", "gender")
            if user_objects_all:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_objects_all)
                })
        return JsonResponse({
            "status": 400,
            "message": "查询单个用户失败",
        })


    def post(self, request, *args, **kwargs):

        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                "status": 200,
                "message": "新增单个成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })
        except:
            return JsonResponse ({
                "status": 400,
                "message": "新增单个失败",
            })

    def put(self, request, *args, **kwargs):
        print("PUT 修改")
        return HttpResponse("PUT ok")
    def delete(self, request, *args, **kwargs):
        print("DELETE 删除")
        return HttpResponse("DELETE ok")




class StudentAPIView(APIView):

    def get(self, request, *args, **kwargs):
        print("DRF GET VIEW")
        return Response("DRF GET VIEW")

    def post(self, request, *args, **kwargs):
        print("DRF POST VIEW")
        return Response("DRF POST VIEW")




















