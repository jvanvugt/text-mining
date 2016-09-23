"""
Extract dates from http://www.biography.com/ and
convert them to ISO 8601 dates (yyyy-mm-dd)

Author: Joris van Vugt, s4279589
"""

import sys
import os
import re
import nlp

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
    ]
MONTHS_REGEX = '|'.join(MONTHS)

# An (ordered) list of tupples mapping regex patterns 
# to lambdas to convert them to ISO 8601 dates
PATTERNS = [
    # E.g., January 5, 2016
    ('(%s) (\d\d?),? (\d\d\d\d)' % MONTHS_REGEX,
        lambda r: '%s-%02d-%02d' % (r.group(3), int(MONTHS.index(r.group(1)) + 1), int(r.group(2)))),
    # E.g., January, 2016
    ('(%s),? (\d\d\d\d)' % MONTHS_REGEX,
        lambda r: '%s-%02d' % (r.group(2), MONTHS.index(r.group(1)) + 1)),
    # E.g., 2016-01-05 (already ISO date)
    ('\d\d\d\d-\d\d?-\d\d?',
        lambda r: r.group(0)),
    # E.g., 2016 (just a year)
    ('\d\d\d\d', 
        lambda r: r.group(0)),
]
    


def convert_dates(filename):
    nlp.clean(filename)
    dates = []
    with open(filename + '.out', 'r') as file:
        for line in file:
            # Save the original line, so we can remove already
            # matched dates so we don't match them again
            # We also remove the newline at the end of the line
            original_line = line[:-1]
            done = False

            # Keep trying all rules on the sentence until none
            # matched
            while True:
                for pattern, convert in PATTERNS:
                    found = False
                    date = re.search(pattern, line)
                    if date is not None:
                        # Remove found date from the sentence
                        line = line.replace(date.group(0), '')
                        iso_date = convert(date)
                        dates.append((iso_date, original_line))
                        found = True
                        break
                if not found:
                    break
    os.remove(filename + '.out')
    dates = sorted(dates, key=lambda d: d[0])
    for date in dates:
        print(' | '.join(date))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        convert_dates(sys.argv[1])
    else:
        print('Usage: convert_dates.py [file]')