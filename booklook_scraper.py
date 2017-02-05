import argparse
import mechanicalsoup

# //*[@id="course_search"]/tbody/tr[3]/td[2]/input

parser = argparse.ArgumentParser(description='Form Submit test')
# parser.add_argument('course')
args = parser.parse_args()

browser = mechanicalsoup.Browser()


login_page = browser.get('https://fortuna.uwaterloo.ca/cgi-bin/cgiwrap/rsic/book')

login_form = login_page.soup.select('#course_search')
print (login_form)



'''
import requests
from bs4 import BeautifulSoup
import lxml.html as lh

def getFormData(term, department,course, section, instructor):
    url = 'https://fortuna.uwaterloo.ca/cgi-bin/cgiwrap/rsic/book/search.html'

    form_data = {
        'term': term,
        'department': department,
        'course': course,
        'section': section,
        'instructor': instructor
    }

    response = requests.post(url, data = form_data)
'''
