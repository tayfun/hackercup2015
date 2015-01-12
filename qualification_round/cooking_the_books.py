# -*- coding: utf-8 -*-
"""

Every business can make use of a good accountant and, if they're not big on
following the law, sometimes a bad one. Bad accountants try to make more money
for their employers by fudging numbers without getting caught.

Sometimes a bad accountant wants to make a number larger, and sometimes
smaller. It is widely known that tax auditors will fail to notice two digits
being swapped in any given number, but any discrepancy more egregious will
certainly be caught. It's also painfully obvious when a number has fewer digits
than it ought to, so a bad accountant will never swap the first digit of a
number with a 0.

Given a number, how small or large can it be made without being found out?

Input

Input begins with an integer T, the number of numbers that need tweaking. Each
of the next T lines contains a integer N.

Output

For the ith number, print a line containing "Case #i: " followed by the
smallest and largest numbers that can be made from the original number N, using
at most a single swap and following the rules above.

Constraints
1 ≤ T ≤ 100
0 ≤ N ≤ 999999999
N will never begin with a leading 0 unless N = 0
"""


def print_case(case, min_number, max_number):
    print "Case #%d: %s %s" % (case, min_number, max_number)


def change(line, number_to_change):
    """
    Takes a string line and int number_to_change and exchanges it with the
    first character in line.
    """
    number_char = str(number_to_change)
    index = len(line) - line[::-1].index(number_char) - 1
    line_list = list(line)
    line_list[index] = line[0]
    line_list[0] = number_char
    return "".join(line_list)


input_file = open('cooking_the_books.txt', 'r')
for case, line in enumerate(input_file):
    if case == 0:
        continue
    line = line.strip()

    number = int(line)
    if number <= 11:
        print_case(case, line, line)
        continue
    first_number = int(line[0])
    sorted_filtered = filter(lambda x: x != "0", sorted(line[1:]))
    if not sorted_filtered:
        print_case(case, line, line)
        continue
    if int(sorted_filtered[-1]) <= first_number:
        max_number = line
    else:
        max_number = change(line, sorted_filtered[-1])
    if int(sorted_filtered[0]) >= first_number:
        min_number = line
    else:
        min_number = change(line, sorted_filtered[0])
    print_case(case, min_number, max_number)

input_file.close()
