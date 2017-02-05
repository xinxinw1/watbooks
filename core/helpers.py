#################################
# Programmer: Kenneth Sinder
# Date: 2017-02-04
# Filename: core/helpers.py
# Description: Services to support API endpoints at views.py
#################################

from core.models import *
from core.serializers import *
import re
import requests

def get_or_create_textbook(name, author, sku, new_price, used_price = None, is_required = False):
    """
    Creates and persists a new textbook with the given params.
    Returns the created Textbook for convenience.
    If a Textbook with the same SKU already exists, return that book
    and perform no database operations.
    """
    try:
        return Textbook.objects.get(sku=sku)
    except Textbook.DoesNotExist:
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

def add_rating(sku, subject, catalog_no, is_useful):
    """
    Identifies the Course and Textbook using the given arguments,
    and applies the given boolean usefulness flag to a new Rating.
    The new Rating is returned for convenience.
    """
    book = Textbook.objects.get(sku=sku)
    course = Course.objects.get(catalog_number=catalog_no, subject=subject)
    rating = Rating(is_useful=is_useful, book=book, course=course)
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

def get_entries_for_course(subject, catalog_no):
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
