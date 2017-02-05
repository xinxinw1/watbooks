from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import *
from core.serializers import *
from core.helpers import *

# Create your views here.

class AngularApp(TemplateView):
    template_name = 'index.html'

def send_to_angular(request):
    return render(request, 'index.html')

@api_view(['GET'])
def book_collection(request):
    if request.method == 'GET':
        books = Textbook.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def course_endpoint(request, course, catalog_no):
    if request.method == 'GET':
        course = str(course)
        catalog_no = int(catalog_no)
        entries = get_entries_for_course(course, catalog_no)
        result = {"data": {"latest": entries}, "meta": {"status_code": 200, "outcome": "success"}}
        return Response(result)
