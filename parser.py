import re

count = 1


class Book(object):
    def __init__(self):
        self.book_name = ''
        self.author_name = ''
        self.author_surname = ''

    def __str__(self):
        return 'Naziv knjige: ' + self.book_name + ' Author: ' + self.author_name + ' ' + self.author_surname


def parse_book_file(ln=''):
    global count

    book = Book()

    # PARSING BOOK NAME
    book_name = re.split(chr(30) + '200..' + chr(31) + 'a', ln)

    for i in range(0, len(book_name[1])):
        if book_name[1][i] == chr(30) or book_name[1][i] == chr(31):
            break
        book.book_name = book.book_name + book_name[1][i]

    # PARSING AUTHOR NAME
    book_author_surname = re.split(chr(30) + '700.1' + chr(31) + '4070' + chr(31) + 'a', ln)

    if len(book_author_surname) == 2:

        iterator = iter(range(0, len(book_author_surname[1])))

        for i in iterator:
            if book_author_surname[1][i] == chr(30) or book_author_surname[1][i] == chr(31):
                break
            book.author_surname = book.author_surname + book_author_surname[1][i]

        book_author_name = re.split(chr(31) + 'b', book_author_surname[1])

        if len(book_author_name) == 1:
            return

        iterator = iter(range(0, len(book_author_name[1])))

        for i in iterator:
            if book_author_name[1][i] == chr(30) or book_author_name[1][i] == chr(31):
                break
            book.author_name = book.author_name + book_author_name[1][i]

        print(count, book)

    count += 1



def parse_line(ln=''):
    firstPart = re.split(chr(31) + 'b', name[1])
    if len(firstPart) < 2:
        firstPart = re.split(chr(31), name[1])
        # print(firstPart)
        firstPart = re.split(chr(30), firstPart[0])
        # print(firstPart[0])
        secondPart = re.split(chr(30), firstPart[0])
    else:
        secondPart = re.split(chr(30), firstPart[1])
        if chr(31) in secondPart[0]:
            secondPart = re.split(chr(31), secondPart[0])
    print(count, firstPart[0], secondPart[0])

    # if len(numReprinted) > 1:
    #     numReprinted = re.split(chr(31), numReprinted[1])
    #     print(numReprinted[0])

with open(file='fajlovi/knjige.txt', encoding="utf8") as fp:
    for line in fp:
        parse_book_file(ln=line)


