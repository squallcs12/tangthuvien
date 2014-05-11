from django.views.generic.base import View
from django.http.response import HttpResponse
from tangthuvien import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class WebImageGenerateView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WebImageGenerateView, self).dispatch(*args, **kwargs)

    def post(self, request):
        url = request.POST['url']

        filename = url.split("/").pop().split(".")[0]

        import os
        os.system("/usr/bin/wkhtmltoimage \"%s\" %s.jpg" % (url, os.path.join(
                                                        settings.MEDIA_ROOT,
                                                         "web_images",
                                                         filename)))

        return HttpResponse("1")
