#################################
# Programmer: Kenneth Sinder
# Date: 2017-02-04
# Filename: core/helpers.py
# Description: Services to support API endpoints at views.py
#################################

from core.models import *
from core.serializers import *
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re
import requests
import json
from core.books_scraper import *

USER_ALREADY_CREATED = "User Already Created"

def get_or_create_textbook(name, author, sku, new_price, used_price = None, is_required = False):
    """
    Creates and persists a new textbook with the given params.
    Returns the created Textbook for convenience.
    If a Textbook with the same SKU already exists, return that book
    and perform no database operations.
    """
    try:
        return Textbook.objects.get(sku=sku)
    except:
        if not used_price is None:
            book = Textbook(name=name, author=author, sku=sku, new_price=new_price, used_price=used_price, is_required=is_required)
        else:
            book = Textbook(name=name, author=author, sku=sku, new_price=new_price, is_required=is_required)
        book.save()
    return book

def get_or_create_course(code, name):
    """
    Creates and persists a new Course with the given params.
    Returns the created Course for convenience.
    """
    if not ' ' in code:
        index = re.search('[A-Za-z][0-9]', code).start()
        subject = code[:index+1]
        catalog_no = int(code[index+1:])
    else:
        subject = code.split(' ')[0]
        catalog_no = int(code.split(' ')[1])
    course, created = Course.objects.get_or_create(subject=subject, catalog_number=catalog_no, defaults={'title': name})
    return course

def add_book_to_course(course, book):
    """
    Associates the given book with the given course.
    Returns the updated Course for consistency.
    """
    if not [x for x in course.books.all() if x.sku == book.sku]:
        course.books.add(book)
        course.save()
    return course

def add_rating(sku, subject, catalog_no, user, is_useful):
    """
    Identifies the Course and Textbook using the given arguments,
    and applies the given boolean usefulness flag to a new Rating.
    The new Rating is returned for convenience.
    """
    book = Textbook.objects.get(sku=sku)
    course = Course.objects.get(catalog_number=catalog_no, subject=subject)
    try:
        r = Rating.objects.get(book=book,course=course,user=user)
        if is_useful == "none":
            r.delete()
            return
        r.is_useful = True if is_useful=='up' else False
        r.save()
        return r
    except:
        pass
    if is_useful != "none":
        is_useful = True if is_useful=='up' else False
        rating = Rating(is_useful=is_useful, book=book, course=course, user=user)
        rating.save()
    return rating

def get_rating_for_course_book(sku, subject, catalog_no):
    try:
        book = Textbook.objects.get(sku=sku)
        course = Course.objects.get(catalog_number=catalog_no, subject=subject)
        ratings = Rating.objects.filter(book=book, course=course)
        up = sum([x.is_useful for x in ratings])
        down = len(ratings) - up
        return {'up': up, 'down': down}
    except:
        return {'up': 0, 'down': 0}

def get_entries_for_course(subject, catalog_no, user):
    try:
        course = Course.objects.get(catalog_number=catalog_no, subject=subject)
        textbooks = get_textbooks_for_course(subject, catalog_no)
        for textbook in textbooks:
            try:
                book = Textbook.objects.get(sku=textbook['sku'])
                ratings = Rating.objects.filter(book=book,course=course)
                up = sum([x.is_useful for x in ratings])
                down = len(ratings) - up
                textbook["usefulness"] = {'up': up, 'down': down}
                textbook["new_price"] = "${0}".format(textbook["new_price"])
                textbook["used_price"] = "${0}".format(textbook["used_price"])
                try:
                    rating = Rating.objects.get(book=book,course=course,user=user)
                    textbook["user_rating"] = "up" if rating.is_useful == True else "down"
                except:
                    textbook["user_rating"] = "none"
            except:
                textbook["usefulness"] = {'up': 0, 'down': 0}
        return textbooks
    except:
        return []

def get_textbooks_for_course(subject, catalog_no):
    try:
        course = Course.objects.get(catalog_number=catalog_no, subject=subject)
        return BookSerializer(course.books, many=True).data
    except:
        return []

def get_all_courses():
    r = requests.get("https://api.uwaterloo.ca/v2/courses.json?key=d457a25ed1f5f6529f15ed86137d4b0f")
    d = r.json()
    if int(d['meta']['status']) == 200:
        return [{'subject': x['subject'], 'catalog_number': x['catalog_number']} for x in d['data']]
    return []

def add_user(email, password, first_name, last_name):
    try:
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user
    except IntegrityError:
        return USER_ALREADY_CREATED

def login(email, password):
    return authenticate(username=email, password=password)


def seed():
    courses = get_all_courses()
    for c in courses:
        print(c)
        crs = get_or_create_course(c['subject'] + ' ' + str(c['catalog_number']), "BestCourse")
        new = Parse(course_dept=c['subject'], course_num=str(c['catalog_number']))
        while True:
            p = new.get_json()
            d = json.loads(p)
            if not d:
                break
            for b in d:
                #try:
                #    b['price'] = int(b['price'].split(' ')[-1]) if ':' not in b['price'].split(' ')[-1] else 0
                #except:
                #    b['price'] = '0'
                print("Price:" + b['price'])
                book = get_or_create_textbook(b['title'], b['author'], b['sku'].split(' ')[-1], str(b["price"].split(' ')[-1]))
                add_book_to_course(crs, book)
                print("success")
