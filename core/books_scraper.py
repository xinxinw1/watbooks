import requests
from bs4 import BeautifulSoup
from collections import deque
import json


class Parse(object):
    def __init__(self, course_dept='', course_num='', course_term='1171'):
        self.all_books = []
        self.first_page = None
        self.queue = None # fifo
        self.course_dept = course_dept
        self.course_num = course_num
        self.course_term = course_term
        self.first = True
        self.all_skus = dict()

    def get_links_to_all(self, first_page_source):
        """Gets links to all pages from the source of the first page."""
        soup = BeautifulSoup(first_page_source, 'html.parser')
        items = soup.select('blockquote')

        if items:
            all_links = items[0].select('a')
        else:
            return False

        all_links = all_links[:-2] # ignores the links to LAST and NEXT

        all_links = [str(i['href']) for i in all_links]

        return all_links

    def create_queue(self):
        """Creates a queue with links to all pages"""
        course_num = self.course_num
        course_dept = self.course_dept
        course_term = self.course_term
        payload = [('mv_profile', 'search_course'), ('mv_searchspec', course_term),  ('mv_searchspec', course_dept),
        ('mv_searchspec', course_num), ('mv_searchspec', ''), ('mv_searchspec', '')]

        post_url = 'https://fortuna.uwaterloo.ca/cgi-bin/cgiwrap/rsic/book/search.html'

        r = requests.post(post_url, data=payload)
        first_page_source = r.text # html source for the first page of results

        self.first_page = first_page_source

        other_page_urls = self.get_links_to_all(first_page_source)

        if other_page_urls:
            self.queue = deque(other_page_urls)
        else:
            self.queue = deque([])
            return False
        return True

    def get_page_source(self):
        if self.first:
            self.first = False
            self.create_queue()
            return self.first_page
        else:
            queue = self.queue
            while queue:
                link = queue.popleft()
                r = requests.get(link)
                return r.text
            return False

    def parse_one_page(self):

        source = self.get_page_source()
        if source:
            soup = BeautifulSoup(source, 'html.parser')

            books_all = soup.find_all("div", "book_item")

            all_book_objects = []

            for book in books_all:
                title = book.find("span","title").text
                author = book.find("span","author").text
                sku = book.find("span","sku").text
                price = book.find("span","price").text

                #checking if the sku already exists
                if sku in self.all_skus:
                    continue
                else:
                    self.all_skus[sku] = sku

                complete_book_details = {}
                complete_book_details['title'] = title
                complete_book_details['author'] = author
                complete_book_details['sku'] = sku
                complete_book_details['price'] = price
                all_book_objects.append(complete_book_details)

            return all_book_objects
        else:
            return False


    def get_json(self):
        '''
        with open('json_out', 'w') as outfile:
            json.dump(all_book_objects, outfile)
        '''
        all_book_objects = self.parse_one_page() # returns all_books_objects
        
        if all_book_objects:
            json_file = json.dumps(all_book_objects)
            return json_file
        else:
            json_file = json.dumps({})
            return json_file



new = Parse(course_dept='CIVE', course_num='440')
counter = 0
while True:
    p = new.get_json()
    dict = json.loads(p)
    if dict:
        print (dict)
        print (len(dict))
        counter += 1
    else:
        print ('No more pages to parse')
        break
