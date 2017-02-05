"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/books/$', book_collection),
    url(r'^api/v1/course/([A-Z]{3,6})/([0-9]{2,4})/', course_endpoint),
    url(r'^$', send_to_angular)
] + static('/', document_root=settings.ANGULAR_ROOT)

