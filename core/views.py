from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import *
from core.serializers import *

# Create your views here.

class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
        return context


class SampleView(View):
	"""View to render django template to angular"""
	def get(self, request):
		return HttpResponse("OK!")


class NgTemplateView(View):
	"""View to render django template to angular"""
	def get(self, request):
		return render(request, 'template.html', {"django_variable": "This is django context variable"})


@api_view(['GET'])
def book_collection(request):
    if request.method == 'GET':
        books = Textbook.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
