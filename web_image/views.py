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
        width = request.POST['width']
        height = request.POST['height']

        filename = url.split("/").pop().split(".")[0]

        import os
        program = settings.realpath('program/wkhtmltoimage')
        des_file = "%s.jpg" % os.path.join(settings.MEDIA_ROOT, "web_images", filename)
        try:
            os.unlink(des_file)
        except OSError:
            pass
        os.system("%s --width %s --height %s \"%s\" %s" % (program, width, height, url, des_file))

        return HttpResponse("1")
