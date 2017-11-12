from collections import defaultdict

import requests
from bs4 import BeautifulSoup
import os
import json
import re


class NovelQuery:
    def __init__(self):
        self.url = str()
        self.category_num = int()
        self._category = str()
        self.novel_cnt_limit = int()
        self.char_cnt_min = int()
        self.char_cnt_max = int()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        category_map = defaultdict(int)
        category_map.update({
            '異世界': 101,
            '現実世界': 102,
            'ハイファンタジー': 103,
            '純文学': 104,
            'ヒューマンドラマ': 302,
            '歴史': 303,
            '推理': 304,
            'ホラー': 305,
            'アクション': 306,
            'コメディー': 307,
            'ＶＲゲーム': 401,
            '宇宙': 402,
            '空想科学': 403,
            'パニック': 404,
            '童話': 9901,
            '詩': 9902,
            'エッセイ': 9903,
        })
        self.category_num = category_map[category]
        self._category = category

    def create_url(self):
        self.url = 'http://api.syosetu.com/novelapi/api/?' \
              'genre={genre}&' \
              'out=json&' \
              'lim={limit}&' \
              'length={min}-{max}'.format(genre=self.category_num,
                                         limit=self.novel_cnt_limit,
                                         min=self.char_cnt_min,
                                         max=self.char_cnt_max)

        return self.url


class BookInfo:
    def __init__(self):
        self.title = str()
        self.story = str()
        self.ncode = str()
        self.link = str()
        self.urls = list()


class Book:
    def __init__(self):
        self.category = str()
        self.title = str()
        self.ncode = str()
        self.chapters = list()


class BookManager:
    def __init__(self):
        self.fetching = FetchBook()
        self.base_path = 'classification/data'

    def fetch_books(self, url, category):
        books_info = self.fetching.fetch_books_info(url)
        books_info = self.fetching.get_chapters(books_info)
        books = self.fetching.get_body(books_info, category)

        return books

    def save(self, books):
        for book in books:
            category_dir = os.path.join(self.base_path, str(book.category))
            if not os.path.exists(category_dir):
                os.mkdir(category_dir)
            title_dir = os.path.join(category_dir, book.ncode)
            if not os.path.exists(title_dir):
                os.mkdir(title_dir)
            for i, chapter in enumerate(book.chapters):
                file = title_dir + '/chapter{}.txt'.format(i)
                with open(file, 'wt') as f:
                    f.write(chapter)


class FetchBook:
    def __init__(self):
        self.base_url = 'http://ncode.syosetu.com'

    def fetch_books_info(self, url):
        books_info = list()
        r = requests.get(url)
        json_data = r.json()
        for a_novel in json_data[1:]:
            book_info = BookInfo()
            book_info.title = a_novel['title']
            book_info.story = a_novel['story']
            book_info.ncode = a_novel['ncode'].lower()
            book_info.link = "http://ncode.syosetu.com/{}/".format(book_info.ncode)
            books_info.append(book_info)

        return books_info

    def get_chapters(self, books_info):
        for book_info in books_info:
            r = requests.get(book_info.link)
            content = r.content
            html = content.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            a_list = soup.find_all('a', href=re.compile(r'/n\d\d\d\d\w\w/[0-9]+/'))
            urls = [a.get('href') for a in a_list]
            urls = [self.base_url + url for url in urls]
            book_info.urls = urls

        return books_info

    def get_body(self, books_info, category):
        books = list()
        for book_info in books_info:
            book = Book()
            book.category = category
            for url in book_info.urls:
                r = requests.get(url)
                content = r.content
                html = content.decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                book.title = soup.title.text
                book.ncode = book_info.ncode
                book.chapters.append(soup.get_text())
            books.append(book)
        return books


if __name__ == '__main__':
    query = NovelQuery()
    query.category = '異世界'
    query.novel_cnt_limit = 5
    query.char_cnt_min = 4000
    query.char_cnt_max = 5000
    url = query.create_url()
    manager = BookManager()
    books = manager.fetch_books(url, query.category_num)
    manager.save(books)


