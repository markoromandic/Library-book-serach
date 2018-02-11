import re

count = 0
books = []

class Book(object):
    def __init__(self):
        self.book_name = ''
        self.author_name = ''
        self.author_surname = ''
        self.release = ''
        self.publisher = ''

    def __str__(self):
        return 'Naziv knjige: ' + self.book_name + ' Author: ' + self.author_name + ' ' + self.author_surname + \
               ' Izdanje: ' + self.release


def parse_book_file(ln=''):
    global count, books

    book = Book()

    books.append(book)

    count += 1

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

        if len(book_author_name) == 1:
            return

        for i in range(0, len(book_author_name[1])):
            if book_author_name[1][i] == chr(30) or book_author_name[1][i] == chr(31) \
                    or book_author_name[1][i] == '\n':
                break
            book.author_name = book.author_name + book_author_name[1][i]

    # PARSING RELEASE

    book_release = re.split(chr(30) + '205..' + chr(31) + 'a', ln)

    if len(book_release) == 1:
        return

    for i in range(0, len(book_release[1])):
        if book_release[1][i] == chr(30) or book_release[1][i] == chr(31) or book_release[1][i] == '\n':
            break
        book.release = book.release + book_release[1][i]

    # PARSING PUBLISHER

    # print(count, book)


with open(file='fajlovi/knjige.txt', encoding="utf8") as fp:
    for line in fp:
        parse_book_file(ln=line)

    for b in books:
        print(b)


