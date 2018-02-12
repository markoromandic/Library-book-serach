import re

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
    def __init__(self, record_code=''):
        self.record_code = record_code
        self.subfields = []

    def prepareSubfields(self):
        line = ''

        for s in self.subfields:
            line = line + '| Subfield code: ' + s.subfield_code + ' Subfield data: ' + s.data

        return line

    def __str__(self):
        return 'Record code: ' + self.record_code + ' Subfields: ' + self.prepareSubfields()


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
    def __init__(self, prefix_code='', record_code=''):
        self.prefix_code = prefix_code
        self.record_code = record_code

    def __str__(self):
        return 'Prefix code: ' + self.prefix_code + ' Record code: ' + self.record_code


def parse_book_file(ln=''):
    global books

    new_book = Book()
    books.append(new_book)

    records = re.split(chr(30), ln)

    for r in records:
        subfields = re.split(chr(31), r)
        new_record = Record(subfields[0][0:3])
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

    prefix = Prefix(prefix_code=ln[0][0:2], record_code=ln[1][0:4])

    prefixes.append(prefix)


def parse_prefix_names_file(ln=''):
    global prefix_names

    ln = re.split('=', ln)

    prefix_name = PrefixName(prefix_code=ln[0][0:2], prefix_name=ln[1][0:len(ln[1]) - 1])

    prefix_names.append(prefix_name)


with open(file='fajlovi/knjige.txt', encoding='utf8') as fp:
    count = 0
    for line in fp:
        parse_book_file(ln=line)

with open(file='fajlovi/prefiksi.txt', encoding='utf8') as fp:
    for line in fp:
        parse_prefix_file(ln=line)

with open(file='fajlovi/PrefixNames_sr.properties', encoding='utf8') as fp:
    for line in fp:
        parse_prefix_names_file(ln=line)

# for b in books:
#     print(b)
#
# for p in prefixes:
#     print(p)
#
# for p_n in prefix_names:
#     print(p_n)
