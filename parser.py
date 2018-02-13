import re
import MySQLdb
import time

books = []
prefixes = []
prefix_names = []


class Book(object):
    def __init__(self):
        self.records = []

    def __str__(self):
        print('START_BOOK_RECORDS')
        for r in self.records:
            print(r)
        return 'END_BOOK_RECORDS'


class Record(object):
    def __init__(self, record_code='', first_indicator='',second_indicator=''):
        self.record_code = record_code
        self.first_indicator = first_indicator
        self.second_indicator = second_indicator
        self.subfields = []

    def prepareSubfields(self):
        line = ''

        for s in self.subfields:
            line = line + '| Subfield code: ' + s.subfield_code + ' Subfield data: ' + s.data

        return line

    def __str__(self):
        return 'Record code: ' + self.record_code + ' First indicator: ' + self.first_indicator \
               + ' Second indicator: ' + self.second_indicator + ' Subfields: ' + self.prepareSubfields()


class SubfieldRecord(object):
    def __init__(self, subfield_code='', data=''):
        self.subfield_code = subfield_code
        self.data = data

    def __str__(self):
        return 'Subfield code: ' + self.subfield_code + ' Data: ' + self.data


class PrefixName(object):
    def __init__(self, prefix_code='', prefix_name=''):
        self.prefix_code = prefix_code
        self.prefix_name = prefix_name

    def __str__(self):
        return 'Prefix code: ' + self.prefix_code + ' Prefix name: ' + self.prefix_name


class Prefix(object):
    def __init__(self, prefix_code='', field_code='', subfield_code=''):
        self.prefix_code = prefix_code
        self.field_code = field_code
        self.subfield_code = subfield_code

    def __str__(self):
        return 'Prefix code: ' + self.prefix_code + ' Field code: ' + self.field_code + ' Subfield code: ' \
               + self.subfield_code


def parse_book_file(ln=''):
    global books

    new_book = Book()
    books.append(new_book)

    records = re.split(chr(30), ln)

    for r in records:
        subfields = re.split(chr(31), r)
        new_record = Record(subfields[0][0:3], first_indicator=subfields[0][3], second_indicator=subfields[0][4])
        new_book.records.append(new_record)

        for i in range(1, len(subfields)):
            if subfields[i][len(subfields[i]) - 1] is not '\n':
                new_subfield = SubfieldRecord(subfield_code=subfields[i][0],
                                              data=subfields[i][1:(len(subfields[i]))])
            else:
                new_subfield = SubfieldRecord(subfield_code=subfields[i][0],
                                              data=subfields[i][1:(len(subfields[i]) - 1)])
            new_record.subfields.append(new_subfield)


def parse_prefix_file(ln=''):
    global prefixes

    ln = re.split('-', ln)

    prefix = Prefix(prefix_code=ln[0][0:2], field_code=ln[1][0:3], subfield_code=ln[1][3])

    prefixes.append(prefix)


def parse_prefix_names_file(ln=''):
    global prefix_names

    ln = re.split('=', ln)

    prefix_name = PrefixName(prefix_code=ln[0][0:2], prefix_name=ln[1][0:len(ln[1]) - 1])

    prefix_names.append(prefix_name)


with open(file='fajlovi/knjige.txt', encoding='utf8') as fp:
    count = 0
    for line in fp:
        count = count + 1
        if count < 100:
            parse_book_file(ln=line)

# with open(file='fajlovi/prefiksi.txt', encoding='utf8') as fp:
#     for line in fp:
#         parse_prefix_file(ln=line)
#
# with open(file='fajlovi/PrefixNames_sr.properties', encoding='utf8') as fp:
#     for line in fp:
#         parse_prefix_names_file(ln=line)


# for b in books:
#     print(b)
#
# for p in prefixes:
#     print(p)
#
# for p_n in prefix_names:
#     print(p_n)


def insert_prefexes_into_database(cursor):
    global prefixes
    add_prefix = ("INSERT INTO prefix "
                    "(prefix_code, field_code, subfield_code ) "
                    "VALUES (%(prefix_code)s, %(field_code)s, %(subfield_code)s))")
    for prefix in prefixes:
        data_prefix = {
            'prefix_code': prefix.prefix_code,
            'field_code': prefix.field_code,
            'subfield_code': prefix.subfield_code,
        }
        try:
            cursor.execute(add_prefix, data_prefix)
        except MySQLdb.Error as err:
            print("Something went wrong5: {}".format(err))
            return

def insert_prefex_names_into_database(cursor):
    global prefix_names
    add_prefix_names = ("INSERT INTO prefix_names "
                    "(prefix_code, prefix_name ) "
                    "VALUES (%(prefix_code)s, %(prefix_name)s)")
    for prefix_name in prefix_names:
        data_prefix_names = {
            'prefix_code': prefix_name.prefix_code,
            'prefix_name': prefix_name.prefix_name.encode('utf-8'),
        }
        try:
            cursor.execute(add_prefix_names, data_prefix_names)
        except MySQLdb.Error as err:
            print("Something went wrong6: {}".format(err))
            return

def add_subfield_into_database(subfield, id_field, cursor):
    add_subfield = ("INSERT INTO subfield "
                  "(code, content, id_field ) "
                  "VALUES (%(code)s, %(content)s, %(id_field)s)")
    data_subfield = {
        'code': subfield.subfield_code,
        'content': subfield.data.encode('utf-8'),
        'id_field': id_field,
    }
    try:
        cursor.execute(add_subfield, data_subfield)
    except MySQLdb.Error as err:
        print("Something went wrong3: {}".format(err))
        return

def add_record_into_database(record, id_book,cursor):
    add_field = ("INSERT INTO field "
                  "(code, id_book, first_indicator, second_indicator) "
                  "VALUES (%(code)s, %(id_book)s, %(first_indicator)s, %(second_indicator)s)")
    data_field = {
        'code': record.record_code,
        'id_book': id_book,
        'first_indicator': record.first_indicator,
        'second_indicator': record.second_indicator,
    }
    try:
        cursor.execute(add_field, data_field)
    except MySQLdb.Error as err:
        print("Something went wrong2: {}".format(err))
        return

    id_field = cursor.lastrowid
    for subfield in record.subfields:
        add_subfield_into_database(subfield=subfield,id_field=id_field,cursor=cursor)


def insert_books_into_database():
    time_start = int(round(time.time() * 1000))
    global books
    conn = MySQLdb.connect(host= "localhost",
                      user="root",
                      passwd="admin",
                      db="mydb")
    cursor = conn.cursor()
    for book in books:
        try:
            pass
            cursor.execute("INSERT INTO BOOK () VALUES ()")
        except MySQLdb.Error as err:
            print("Something went wrong1: {}".format(err))
            return

        id_book = cursor.lastrowid

        for record in book.records:
            add_record_into_database(record=record,id_book=id_book,cursor=cursor)
    insert_prefex_names_into_database(cursor=cursor)
    insert_prefexes_into_database(cursor=cursor)
    try:
        conn.commit()
    except MySQLdb.Error as err:
        print("Something went wrong4: {}".format(err))
        conn.rollback()
    conn.close()
    total_time = int(round(time.time() * 1000)) - time_start
    print(total_time)

insert_books_into_database()