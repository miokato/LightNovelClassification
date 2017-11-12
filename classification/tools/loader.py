import requests
from bs4 import BeautifulSoup
import os
import json
import re


def fetch_books_info(n=3):
    books = []
    url = 'http://api.syosetu.com/novelapi/api/?out=json&lim={}'.format(n)
    r = requests.get(url)
    json_data = r.json()
    for a_novel in json_data[1:]:
        book_info = dict()
        book_info['title'] = a_novel['title']
        book_info['story'] = a_novel['story']
        ncode = a_novel['ncode']
        book_info['link'] = "http://ncode.syosetu.com/{}/".format(ncode.lower())
        books.append(book_info)
    return books


def get_chapters(books):
    for book in books:
        main = 'http://ncode.syosetu.com'
        r = requests.get(book['link'])
        content = r.content
        html = content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        a_list = soup.find_all('a', href=re.compile(r'/n\d\d\d\d\w\w/[0-9]+/'))
        urls = [a.get('href') for a in a_list]
        urls = [main + url for url in urls]
        book['urls'] = urls

    return books


def get_body(books):
    for book in books:
        for chapter in book:
            pass


def store_file():
    path = 'classification/data/test.gz'


books = fetch_books_info(n=2)
books = get_chapters(books)
print(books)
