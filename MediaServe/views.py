from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from APAS.settings import MEDIA_ROOT

# Create your views here.


def serve_media(request):
    try:
        file_path = request.path.replace('/media/', '')
        file_path = MEDIA_ROOT + file_path
        file = open(file_path, 'rb')
        return FileResponse(file, content_type='application/pdf')
    except FileNotFoundError:
        return HttpResponse("<h1>File not found</h1>", status=404)