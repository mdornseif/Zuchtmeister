#!/usr/bin/env python
# encoding: utf-8
"""
parser.py

Created by Maximillian Dornseif on 2010-03-29.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import re

testtext = [
"Ask Nicole to look into \"nicht angemeldetes europäisches Gebrauchsmuster\"",
"Remember Brian McElroy's home phone is (503) 555-1212",
"Remember I work at the book store Tue 9-11:30am @work",
"Remember Melissa Valiant (415) 555-1212 melissa@example.com",
"Remember the parenting blog http://www.parenthacks.com",
"Remember to add login functionality to selected parts of the site.",
"Remember to check in Taskmaster code",
"Remember to sign up for extra credit hours at the Psych lab on Friday afternoon.",
"Remind Daniel Lerose to give back the old iPhone to Eike Dornseif",
"Remind Heiko Dahlke to check archive scanning with lebenshilfe ang give me back a status.",
"Remind Maximillian Dornseif to add a natural language interface",
"Remind Vanessa Wiemann to write an article about Plagiatism on our Homepage",
"Remind me to call Mom on her birthday on 9/16/07 @yearly @birthday",
]

# Patterns
# Peep = [A-Z][a-z+]\s+[A-Z][a-z+]
# (Remind|Ask) (me|peep) to job
#


op_re = re.compile(r"""^(?P<action>remind|ask)
                        \s+
                        (?P<peep>me|([A-Z][a-z]+(\s+[A-Z][a-z]+)?))
                        \s+
                        (?P<filler1>to)
                        \s+
                        (?P<task>.+)
                        $""",
                   re.IGNORECASE|re.VERBOSE)


def parse(line):
    line = line.strip()
    m = op_re.match(line)
    if m:
        return {'peep': m.group('peep'), 'task': m.group('task'),
                'task': m.group('action'), 'task': m.group('filler1')}
    return {}


def unparse(op):
    return ' '.join([op['action'], op['peep'], op['filler'], op['task']])


if __name__ == '__main__':
    for line in testtext:
        parse(line)
