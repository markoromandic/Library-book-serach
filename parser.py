import re

count = 0
def parse_line(ln=''):
    global count
    book = re.split(chr(30) + '200..' + chr(31) + 'a', ln)
    name = re.split(chr(30) + '700.1' + chr(31) + '4070' + chr(31) + 'a', ln)
    numReprinted = re.split(chr(30) + '205' + '..' + chr(31) + 'a', ln)

    count += + 1

    if len(book) > 1:
        book = re.split(chr(31), book[1])
        # print(ln[0])
    if len(name) > 1:
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
        parse_line(ln=line)
