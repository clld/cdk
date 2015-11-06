from __future__ import unicode_literals
import sys
import re
from collections import Counter

from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import UnicodeReader

import cdk
from cdk import models


DIS_ROMAN_PATTERN = re.compile('\s+(?P<marker>I+)\s*$')
DIS_ARABIC_PATTERN = re.compile('(?P<marker>[0-9]+)\.\s+')
DONOR_PATTERN = re.compile('\s*<(?P<name>[a-z]+)\.\s*>\s*')
DIALECT_PATTERN = re.compile('\s*\((?P<names>[a-z]+\.(,\s*[a-z]+\.)*)\s*\)\s*')

LOC_PATTERN = re.compile('\s*(?P<name>[a-z]+)\.\s+')
SOURCE_PATTERN = re.compile('\s*\((?P<id>[^:]+):\s*(?P<pages>[^\)]+)\)\s*$')


def get_examples(s):
    text, source, pages, loc = '', None, None, None

    for chunk in re.split(',\s+', s):
        #
        # FIXME: must also split on LOC_PATTERN!
        #
        lmatch = LOC_PATTERN.match(chunk)
        if lmatch:
            if text:
                yield text, source, pages, loc
            text, source, pages, loc = '', None, None, None
            loc = lmatch.group('name')
            chunk = chunk[lmatch.end():]

        if text:
            text += ', '
        text += chunk

        smatch = SOURCE_PATTERN.search(text)
        if smatch:
            source, pages = smatch.group('id'), smatch.group('pages')
            text = text[:smatch.start()]
            yield text, source, pages, loc
            text, source, pages, loc = '', None, None, None

    if text:
        yield text, source, pages, loc


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=cdk.__name__,
        name="CDK",
        description="Comprehensive Dictionary of Ket",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='cdk.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    contrib = common.Contribution(id='ket', name=dataset.name)
    DBSession.add(contrib)
    for i, (id, name) in enumerate([
        ('kotorov', 'E.G. Kotorova'), ('nefedov', 'A.V. Nefedov'),
    ]):
        dataset.editors.append(
            common.Editor(contributor=common.Contributor(id=id, name=name), ord=i))

    ket = common.Language(id='ket', name='Ket', latitude=63.76, longitude=87.55)
    add_language_codes(data, ket, 'ket', glottocode='kett1243')
    stats = Counter()

    with UnicodeReader(args.data_file('..', '..', 'cdk-data', 'Ket_verbs_table.docx.csv')) as reader:
        for i, (headword, pos, aspect, russian, german, english, description) in enumerate(reader):
            #
            # FIXME: detect in headword:
            # dialect: " (sket.)"
            # source for loanword: "<rus.>"
            # tonal variants separated by slash?
            # turn position markers into superscripts!
            #
            disambiguation = ''
            match = DIS_ROMAN_PATTERN.search(headword)
            if match:
                disambiguation = match.group('marker')
                headword = headword[:match.start()]
            match = DIS_ARABIC_PATTERN.match(russian)
            if match:
                disambiguation = disambiguation or 'I'
                disambiguation += ' %s' % match.group('marker')
                russian = russian[match.end():]

            donor, dialect = None, None
            match = DONOR_PATTERN.search(headword)
            if match:
                donor = match.group('name')
                headword = headword[:match.start()] + headword[match.end():]
            match = DIALECT_PATTERN.search(headword)
            if match:
                dialect = match.group('names')
                headword = headword[:match.start()] + headword[match.end():]

            entry = models.Entry(
                id=str(i + 1),
                name=headword,
                donor=donor,
                dialect=dialect,
                disambiguation=disambiguation,
                description=description,
                pos=pos,
                aspect=aspect,
                russian=russian,
                german=german,
                english=english,
                language=ket)

            for text, source, pages, loc in get_examples(description):
                rus = ''
                if '  ' in text:
                    text, rus = text.split('  ', 1)
                entry.examples.append(
                    models.Example(language=ket, name=text, description=rus, location=loc))
                #
                # FIXME: handle references!
                #

            DBSession.add(entry)

    print(stats)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
