from django.http import HttpResponse

def home(request):
    """
    首页视图函数
    """
    return HttpResponse("Hello World!")