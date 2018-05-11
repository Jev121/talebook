#!/usr/bin/python
#-*- coding: UTF-8 -*-

import logging
from tornado import web
from base_handlers import BaseHandler, ListHandler
from calibre.utils.filenames import ascii_filename


class TagList(ListHandler):
    def get(self):
        title = _('All tags')
        category = "tags"
        tags = self.all_tags_with_count()
        hot_tags = []
        for tag_name, tag_count in tags.items():
            if tag_count < 5: continue
            hot_tags.append( (tag_name, tag_count) )
        hot_tags.sort(lambda x,y: cmp(y[1], x[1]))
        tags = hot_tags
        return self.html_page('tag/list.html', vars())

class TagBooks(ListHandler):
    def get(self, name):
        title = _('Books of tag: %(name)s') % vars()
        category = "tags"
        tag_id = self.cache.get_item_id(category, name)
        ids = books = []
        if tag_id:
            ids = self.db.get_books_for_category(category, tag_id)
            books = self.db.get_data_as_dict(ids=ids)
        return self.render_book_list(books, vars());

class AuthorList(ListHandler):
    def get(self):
        title = _('All authors')
        category = "authors"
        authors = self.db.all_authors()
        authors.sort(cmp=lambda x,y: cmp(ascii_filename(x[1]).lower(), ascii_filename(y[1]).lower()))
        authors.sort(cmp=lambda x,y: cmp(x[1], y[1]))
        return self.html_page('author/list.html', vars())

class AuthorBooks(ListHandler):
    def get(self, name):
        title = _('Books of author: %(name)s') % vars()
        category = "authors"
        ids = books = []
        author_id = self.cache.get_item_id(category, name)
        if author_id:
            ids = self.db.get_books_for_category(category, author_id)
            books = self.db.get_data_as_dict(ids=ids)
        return self.render_book_list(books, vars());

class PubList(ListHandler):
    def get(self):
        title = _('All publishers')
        category = "publisher"
        publishers = self.cache.get_id_map(category).items()
        return self.html_page('publisher/list.html', vars())

class PubBooks(ListHandler):
    def get(self, name):
        title = _('Books of publisher: %(name)s') % vars()
        category = "publisher"
        publisher_id = self.cache.get_item_id(category, name)
        ids = books = []
        if publisher_id:
            ids = self.cache.books_for_field(category, publisher_id)
            #ids = self.db.get_books_for_category(category, publisher_id)
            books = self.db.get_data_as_dict(ids=ids)
        return self.render_book_list(books, vars());

class AuthorBooksUpdate(ListHandler):
    def post(self, name):
        category = "authors"
        author_id = self.cache.get_item_id(category, name)
        ids = self.db.get_books_for_category(category, author_id)
        for book_id in list(ids)[:40]:
            self.do_book_update(book_id)
        self.redirect('/author/%s'%name, 302)

class PubBooksUpdate(ListHandler):
    def post(self, name):
        category = "publisher"
        publisher_id = self.cache.get_item_id(category, name)
        if publisher_id:
            ids = self.db.get_books_for_category(category, publisher_id)
        else:
            ids = self.cache.search_for_books('')
            books = self.db.get_data_as_dict(ids=ids)
            ids = [ b['id'] for b in books if not b['publisher'] ]
        for book_id in list(ids)[:40]:
            self.do_book_update(book_id)
        self.redirect('/pub/%s'%name, 302)

class RatingList(ListHandler):
    def get(self):
        title = _('All ratings')
        category = "rating"
        ratings = self.cache.get_id_map(category).items()
        ratings.sort(cmp=lambda x,y: cmp(x[1], y[1]))
        return self.html_page('rating/list.html', vars())

class RatingBooks(ListHandler):
    def get(self, name):
        title = _('Books of rating: %(name)s') % vars()
        category = "rating"
        ids = books = []
        rating_id = self.db.get_rating_id(name)
        if rating_id:
            ids = self.db.get_books_for_category(category, rating_id)
            books = self.db.get_data_as_dict(ids=ids)
        return self.render_book_list(books, vars());

def routes():
    return [
        ( r'/author',             AuthorList        ),
        ( r'/author/(.*)',        AuthorBooks       ),
        ( r'/author/(.*)/update', AuthorBooksUpdate ),
        ( r'/tag',                TagList           ),
        ( r'/tag/(.*)',           TagBooks          ),
        ( r'/pub',                PubList           ),
        ( r'/pub/(.*)',           PubBooks          ),
        ( r'/pub/(.*)/update',    PubBooksUpdate    ),
        ( r'/rating',             RatingList        ),
        ( r'/rating/(.*)',        RatingBooks       ),
        ]

