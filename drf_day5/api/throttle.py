from rest_framework.throttling import SimpleRateThrottle


# 使用方式也分局部和全局
class SendMessageRate(SimpleRateThrottle):
    scope = "anon"

    # 只对包含手机号的请求做验证
    def get_cache_key(self, request, view):
        phone = request.query_params.get("phone")
        if not phone:
            return None
        # 返回数据 根据手机号动态展示返回的值
        # return "throttle_%(scope)s_%(ident)" % {"scope": self.scope, "ident": phone}
        return phone
