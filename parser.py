import re

books = []
prefixes = []
prefix_names = []


class PrefixName(object):
    def __init__(self):
        self.code = ''
        self.name = ''

    def __str__(self):
        return 'Code: ' + self.code + ' Name: ' + self.name


class Prefix(object):
    def __init__(self):
        self.name = ''
        self.code = ''

    def __str__(self):
        return 'Name: ' + self.name + ' Code: ' + self.code


class Book(object):
    def __init__(self):
        self.isbn = ''
        self.book_language = ''
        self.country_release = ''
        self.city_publisher = ''
        self.book_name = ''
        self.author_name = ''
        self.author_surname = ''
        self.release = ''
        self.publisher = ''
        self.year_release = ''
        self.number_of_pages = ''

    def __str__(self):
        return 'ISBN: ' + self.isbn + ' Naziv knjige: ' + self.book_name + ' Author: ' + self.author_name + ' ' \
               + self.author_surname + ' Izdanje: ' + self.release + ' Izdavač: ' + self.publisher \
               + ' Godina izdavanja: ' + self.year_release + ' Language: ' \
               + self.book_language + ' Country: ' + self.country_release + ' City: ' + self.city_publisher


def parse_book_file(ln=''):
    global books

    book = Book()

    books.append(book)

    # PARSING ISBN CODE
    book_isbn = re.split(chr(30) + '010..' + chr(31) + 'a', ln)

    if len(book_isbn) > 1:
        for i in range(0, len(book_isbn[1])):
            if book_isbn[1][i] == chr(30) or book_isbn[1][i] == chr(31) or book_isbn[1][i] == '\n':
                break
            book.isbn = book.isbn + book_isbn[1][i]


    # PARSING LANGUAGE OF BOOK
    book_language = re.split(chr(30) + '1010.' + chr(31) + 'a', ln)

    if len(book_language) > 1:
        for i in range(0, len(book_language[1])):
            if book_language[1][i] == chr(30) or book_language[1][i] == chr(31) or book_language[1][i] == '\n':
                break
            book.book_language = book.book_language + book_language[1][i]


    # PARSING COUNTRY OF RELEASE
    book_country_release = re.split(chr(30) + '102..' + chr(31) + 'a', ln)

    if len(book_country_release) > 1:
        for i in range(0, len(book_country_release[1])):
            if book_country_release[1][i] == chr(30) or book_country_release[1][i] == chr(31) \
                    or book_country_release[1][i] == '\n':
                break
            book.country_release = book.country_release + book_country_release[1][i]



    # PARSING BOOK NAME
    book_name = re.split(chr(30) + '200..' + chr(31) + 'a', ln)

    for i in range(0, len(book_name[1])):
        if book_name[1][i] == chr(30) or book_name[1][i] == chr(31) or book_name[1][i] == '\n':
            break
        book.book_name = book.book_name + book_name[1][i]

    # PARSING AUTHOR NAME
    book_author_surname = re.split(chr(30) + '700.1' + chr(31) + '4070' + chr(31) + 'a', ln)

    if len(book_author_surname) == 2:

        for i in range(0, len(book_author_surname[1])):
            if book_author_surname[1][i] == chr(30) or book_author_surname[1][i] == chr(31) \
                    or book_author_surname[1][i] == '\n':
                break
            book.author_surname = book.author_surname + book_author_surname[1][i]

        book_author_name = re.split(chr(31) + 'b', book_author_surname[1])

        if len(book_author_name) > 1:
            for i in range(0, len(book_author_name[1])):
                if book_author_name[1][i] == chr(30) or book_author_name[1][i] == chr(31) \
                        or book_author_name[1][i] == '\n':
                    break
                book.author_name = book.author_name + book_author_name[1][i]

    # PARSING RELEASE

    book_release = re.split(chr(30) + '205..' + chr(31) + 'a', ln)

    if len(book_release) > 1:
        for i in range(0, len(book_release[1])):
            if book_release[1][i] == chr(30) or book_release[1][i] == chr(31) or book_release[1][i] == '\n':
                break
            book.release = book.release + book_release[1][i]

    # PARSING PUBLISHER

    book_publisher = re.split(chr(30) + '210..', ln)

    if len(book_publisher) > 1:
        book_publisher_city = re.split(chr(31) + 'a', book_publisher[1])

        for i in range(0, len(book_publisher_city[1])):
            if book_publisher_city[1][i] == chr(30) or book_publisher_city[1][i] == chr(31) \
                    or book_publisher_city[1][i] == '\n':
                break
            book.city_publisher = book.city_publisher + book_publisher_city[1][i]

        book_publisher_name = re.split(chr(31) + 'c', book_publisher[1])

        if len(book_publisher_name) > 1:
            for i in range(0, len(book_publisher_name[1])):
                if book_publisher_name[1][i] == chr(30) or book_publisher_name[1][i] == chr(31) \
                        or book_publisher_name[1][i] == '\n':
                    break
                book.publisher = book.publisher + book_publisher_name[1][i]

        book_publisher_year = re.split(chr(31) + 'd', book_publisher[1])

        if len(book_publisher_year) > 1:
            for i in range(0, len(book_publisher_year[1])):
                if book_publisher_year[1][i] == chr(30) or book_publisher_year[1][i] == chr(31) \
                        or book_publisher_year[1][i] == '\n':
                    break
                book.year_release = book.year_release + book_publisher_year[1][i]


def parse_prefix_file(ln=''):
    global prefixes

    ln = re.split('-', ln)

    prefix = Prefix()

    prefixes.append(prefix)

    for i in range(0, len(ln[0])):
        if ln[0][i] == '\n':
            break
        prefix.name = prefix.name + ln[0][i]

    for i in range(0, len(ln[1])):
        if ln[1][i] == '\n':
            break
        prefix.code = prefix.code + ln[1][i]


def parse_prefix_names_file(ln=''):
    global prefix_names

    ln = re.split('=', ln)

    prefix_name = PrefixName()

    prefix_names.append(prefix_name)

    for i in range(0, len(ln[0])):
        if ln[0][i] == '\n':
            break
        prefix_name.code = prefix_name.code + ln[0][i]

    for i in range(0, len(ln[1])):
        if ln[1][i] == '\n':
            break
        prefix_name.name = prefix_name.name + ln[1][i]


with open(file='fajlovi/knjige.txt', encoding='utf8') as fp:
    for line in fp:
        parse_book_file(ln=line)


for b in books:
    print(b)


# with open(file='fajlovi/prefiksi.txt', encoding='utf8') as fp:
#     for line in fp:
#         parse_prefix_file(ln=line)
#
# for p in prefixes:
#     print(p)
#
#
# with open(file='fajlovi/PrefixNames_sr.properties', encoding='utf8') as fp:
#     for line in fp:
#         parse_prefix_names_file(ln=line)
#
#
# for p_n in prefix_names:
#     print(p_n)

