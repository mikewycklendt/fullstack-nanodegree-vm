#!/usr/bin/env python

from Project1_db import part1, part2, part3
import datetime

part_1 = part1()
part_2 = part2()
part_3 = part3()


answer1 = []

textfile = open("answers.txt", "w")

for article in part_1:
    answer = str('\"' + article[0].title() + '\"' + ' -- '
                 + str(article[3]) + ' views\r\n')
    answer1.append(answer)

for answer in answer1:
    print(answer)
    textfile.write(answer)


textfile.write('\r\n \r\n')

print("\n\n")

answer2 = []

for author in part_2:
    answer = str(author[0] + " -- " + str(author[1]) + " views\r\n")
    answer2.append(answer)

for answer in answer2:
    print(answer)
    textfile.write(answer)

textfile.write('\r\n \r\n')

print("\n\n")

answer3 = []

for error in part_3:
    thedate = error[0]
    answer = str(thedate.strftime("%B %d, %Y") + " -- " +
                 str(round(error[1], 1)) + "% errors\r\n")
    answer3.append(answer)

for answer in answer3:
    print(answer)
    textfile.write(answer)


textfile.close()
