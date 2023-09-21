import time

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        # 计算响应时间
        duration = time.time() - start_time
        response["X-Response-Time"] = str(duration)

        return response
