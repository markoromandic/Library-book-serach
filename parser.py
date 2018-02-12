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
    def __init__(self):
        self.record_code = ''
        self.subfields = []

    def prepareSubfields(self):
        line = ''

        for s in self.subfields:
            line = line + '| Subfield code: ' + s.subfield_code + ' Subfield data: ' + s.data

        return line

    def __str__(self):
        return 'Record code: ' + self.record_code + ' Subfields: ' + self.prepareSubfields()


class SubfieldRecord(object):
    def __init__(self, subfield_code=''):
        self.subfield_code = subfield_code
        self.data = ''

    def __str__(self):
        return 'Subfield code: ' + self.subfield_code + ' Data: ' + self.data


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


def parse_book_file(ln=''):
    global books

    book_iterator = iter(range(0, len(ln)))

    new_book = Book()

    books.append(new_book)

    # PARSE 001 RECORD - SPECIAL CASE

    new_record = Record()
    new_book.records.append(new_record)
    new_record.record_code = ln[0:3]

    special_case_iterator = iter(range(3, len(ln)))

    # OTHER RECORDS

    for i in special_case_iterator:
        if ln[i] is chr(30) or ln[i] is '\n':
            break
        if ln[i] is chr(31):
            i = next(special_case_iterator, None)
            new_subfield = SubfieldRecord(subfield_code=ln[i])

            new_record.subfields.append(new_subfield)

            if ln[i + 1] is chr(30) or ln[i + 1] is chr(31) or ln[i + 1] is '\n':
                continue

            i = next(special_case_iterator, None)
            subfield_data_iter = iter(range(i, len(ln)))

            for k in subfield_data_iter:
                if ln[k] is chr(30) or ln[k] is chr(31) or ln[k] is '\n':
                    break
                new_subfield.data = new_subfield.data + ln[k]

            for m in range(i, k - 1):
                next(special_case_iterator, None)

    for i in book_iterator:
        if ln[i] is '\n':
            break
        if ln[i] is chr(30):
            new_record = Record()
            for j in range(0, 3):
                i = next(book_iterator, None)
                if i is None:
                    print('I is None')
                new_record.record_code = new_record.record_code + ln[i]
            new_book.records.append(new_record)

            record_iterator = iter(range(i, len(ln)))

            for j in record_iterator:
                if ln[j] is chr(30) or ln[j] is '\n':
                    break
                if ln[j] is chr(31):
                    j = next(record_iterator, None)

                    new_subfield = SubfieldRecord(subfield_code=ln[j])

                    new_record.subfields.append(new_subfield)

                    if ln[j + 1] is chr(30) or ln[j + 1] is chr(31) or ln[j + 1] is '\n':
                        continue

                    j = next(record_iterator, None)
                    subfield_data_iter = iter(range(j, len(ln)))

                    for k in subfield_data_iter:
                        if ln[k] is chr(30) or ln[k] is chr(31) or ln[k] is '\n':
                            break
                        new_subfield.data = new_subfield.data + ln[k]

                    for m in range(j, k - 1):
                        next(record_iterator, None)


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
    count = 0
    for line in fp:
        parse_book_file(ln=line)

for b in books:
    print(b)


with open(file='fajlovi/prefiksi.txt', encoding='utf8') as fp:
    for line in fp:
        parse_prefix_file(ln=line)

for p in prefixes:
    print(p)


with open(file='fajlovi/PrefixNames_sr.properties', encoding='utf8') as fp:
    for line in fp:
        parse_prefix_names_file(ln=line)


for p_n in prefix_names:
    print(p_n)
