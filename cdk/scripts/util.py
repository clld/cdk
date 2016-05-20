# coding: utf8
from __future__ import unicode_literals, print_function, division
import re
from collections import defaultdict

"""
adj
adp
adv
al
anom
an
an pl
bak
baikh
bajk
bakht
ket
conj
el
e.-o.
evenk
f
imb.
inan
inan pl
interj
kel
ket.
kur
leb
mn
nen.
nket
mad
no pl
num
pak
pron inter
pron pers
pron poss
prtc
pl
pron
rus
selk
sket
sul
sum.
sur
v
ver
v-imb.
vk
vpred
vt
"""

DIS_ROMAN_PATTERN = re.compile('\s+(?P<marker>I+)\s*$')
DIS_ARABIC_PATTERN = re.compile('(?P<marker>[1-9]+)$')
DONOR_PATTERN = re.compile('\s*<(?P<name>[a-z]+)\.\s*>\s*')
DIALECT_PATTERN = re.compile('\((?P<names>(n|c|s)ket\.[^\)]+)\)')
DIALECT_CHUNK_PATTERN = re.compile(',(c|k|s)ket\.\s*')

LOC_PATTERN = re.compile('\s*(?P<name>[a-z]+)\.\s+')
SOURCE_PATTERN = re.compile('\s*\((?P<id>[^:]+):\s*(?P<pages>[^\)]+)\)\s*$')


def yield_variants(s):
    for i, variant in enumerate(DIALECT_CHUNK_PATTERN.split(s)):
        variant = variant.strip()
        if variant:
            try:
                dialect, form = [ss.strip() for ss in variant.split('.', 1)]
            except:
                print(s)
                raise ValueError(variant)
            yield dialect, form


class Headword(object):
    def __init__(self, headword):
        self.donor, self.dialects, self.variants = None, [], defaultdict(list)
        match = DONOR_PATTERN.search(headword)
        if match:
            self.donor = match.group('name')
            headword = headword[:match.start()] + headword[match.end():]
        match = DIALECT_PATTERN.search(headword)
        if match:
            for i, (dialect, form) in enumerate(yield_variants(match.group('names'))):
                if not form:
                    self.dialects.append(dialect)
                else:
                    self.variants[dialect].append(form)

            headword = headword[:match.start()] + headword[match.end():]
            # TODO: parse dialect info!

        headword = re.sub('\s+', ' ', headword.strip())

        self.disambiguation = ''
        match = DIS_ROMAN_PATTERN.search(headword)
        if match:
            self.disambiguation = match.group('marker')
            headword = headword[:match.start()].strip()
        match = DIS_ARABIC_PATTERN.search(headword)
        if match:
            if self.disambiguation:
                self.disambiguation = ' ' + self.disambiguation
            self.disambiguation = match.group('marker') + self.disambiguation
            headword = headword[:match.start()].strip()
        variants = headword.split(' also ')
        if len(variants) > 1:
            headword = variants[0]
            assert len(self.dialects) <= 1
            self.variants[self.dialects[0] if self.dialects else None].extend(variants[1:])
        self.form = headword
