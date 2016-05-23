# coding: utf8
from __future__ import unicode_literals, print_function, division
import re
from itertools import groupby

from markupsafe import Markup

DIGIT = re.compile('(?P<digit>\d)')


def examples_by_location(counterpart):
    for location, examples in groupby(counterpart.examples, lambda e: e.location):
        yield location, [e.sentence for e in examples]


def form(s):
    return Markup(DIGIT.sub(lambda m: '<sup>%s</sup>' % m.group('digit'), s))
