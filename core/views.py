#################################
# Programmers: Kenneth Sinder, Xin-Xin Wang
# Date: 2017-02-04
# Filename: core/views.py
# Description: API endpoints and Angular2 redirection
#################################

import re
import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from core.models import *
from core.serializers import *
from core.helpers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

BAD_REQUEST_RESPONSE = Response({"data": [], "meta": {"status_code": 400, "outcome": "bad_request_type"}}, status=400)

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
@authentication_classes((TokenAuthentication))
@permission_classes((IsAuthenticated,))
def course_endpoint(request, course, catalog_no):
    if request.method == 'GET':
        course = str(course)
        catalog_no = int(catalog_no)
        user = request.user
        entries = get_entries_for_course(course, catalog_no, user)
        result = {"data": {"latest": entries}, "meta": {"status_code": 200, "outcome": "success"}}
        return Response(result)

@api_view(['POST'])
@authentication_classes((TokenAuthentication))
@permission_classes((IsAuthenticated,))
def rate_endpoint(request):
    """
    Sample POST Payload (JSON):
    {"sku": 123123, "subject": "PHYS", catalog_number: 234, "is_useful": true}
    """
    if request.method == 'POST':
        payload = json.loads(request.body.decode())
        sku = str(payload["sku"])
        subject = str(payload["subject"])
        catalog_number = int(payload["catalog_number"])
        is_useful = str(payload["is_useful"])
        user_rating = str(payload["user_rating"])
        add_rating(sku, subject, catalog_number, request.user, is_useful)
        return response({"data": "Successfully added a rating for {0} in {1} {2}".format(sku, subject, catalog_number)})


@api_view(['GET'])
def all_courses_endpoint(request):
    if request.method == 'GET':
        return Response({"data": get_all_courses(), "meta": {"status_code": 200, "outcome": "success"}})
    return BAD_REQUEST_RESPONSE

@api_view(['POST'])
def create_user_endpoint(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode())

        try:
            password = str(payload["password"])
            if len(password) > 25 or len(password) < 5:
                raise Exception()
        except:
            return Response({"data": "Password must be 5-25 characters", \
                "meta": {"status_code": 400, "outcome": "bad_request_type"}}, status=400)
        try:
            email = str(payload["email"])
            if len(email) > 100 or "uwaterloo.ca" not in email or re.search(r'[^A-Za-z0-9.-_]+', email) is not None:
                raise Exception()
        except:
            return Response({"data": "E-mail must be a valid UWaterloo e-mail", \
                "meta": {"status_code": 400, "outcome": "bad_request_type"}}, status=400)
        try:
            first_name = str(payload["first_name"])
            last_name = str(payload["last_name"])
            if re.search(r'[^A-Za-z]+', first_name) is not None or len(first_name) > 20:
                raise Exception()
            if re.search(r'[^A-Za-z]+', last_name) is not None or len(last_name) > 20:
                raise Exception()
        except:
            return Response({"data": "First and last name must be alphabetic and less than 21 characters", \
                "meta": {"status_code": 400, "outcome": "bad_request_type"}}, status=400)

        user = add_user(email, password, first_name, last_name)
        if user == USER_ALREADY_CREATED:
            return Response({"data": "Username already exists. Choose a different username.", \
                "meta": {"status_code": 400, "outcome": "bad_request_type"}}, status=400)
        token = Token.objects.create(user=user)
        return Response({"data": {"message": "Successfully created user", "token": token.key}, "meta": {"status_code": 200}})
    else:
        return BAD_REQUEST_RESPONSE

@api_view(['POST'])
def login_endpoint(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode())
        email = str(payload["email"])
        password = str(payload["password"])
        user = login(email, password)
        if user is None:
            return Response({"data": "Bad e-mail or password"}, status=401)
        token = Token.objects.create(user=user)
        return Response({"data": {"token": token.key}})
    return Response({})


