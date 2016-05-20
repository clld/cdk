from __future__ import unicode_literals
import sys
import re
from collections import Counter
from itertools import groupby

from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.dsv import UnicodeReader

import cdk
from cdk import models
from cdk.scripts.util import Headword


DIS_ARABIC_PATTERN = re.compile('(?P<marker>[0-9]+)\.\s+')

LOC_PATTERN = re.compile('\s*(?P<name>[a-z]+)\.\s+')
SOURCE_PATTERN = re.compile('\s*\((?P<id>[^:]+):\s*(?P<pages>[^\)]+)\)\s*$')

MEANING_ID = 0


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


def load(data, reader, ket, offset=0, verbs=True):
    global MEANING_ID

    for headword, meanings in groupby(reader, lambda r: (r[0], r[1], r[2])):
        headword, pos, aspect_or_plural = headword
        headword = Headword(headword)
        offset += 1

        id_ = str(offset)
        entry = models.Entry(
            id=id_,
            name=headword.form,
            donor=headword.donor,
            dialect=' '.join(headword.dialects),
            disambiguation=headword.disambiguation,
            pos=pos,
            aspect=aspect_or_plural if verbs else None,
            plural=None if verbs else aspect_or_plural,
            language=ket)

        # TODO: handle variants!

        for j, (headword, pos, aspect, russian, german, english, description) in enumerate(meanings):
            match = DIS_ARABIC_PATTERN.match(russian)
            if match:
                russian = russian[match.end():].strip()
            meaning = data['Meaning'].get((russian, german, english))
            if not meaning:
                MEANING_ID += 1
                meaning = data.add(
                    models.Meaning,
                    (russian, german, english),
                    id=str(MEANING_ID),
                    name=english,
                    russian=russian,
                    german=german,
                    english=english)

            counterpart = common.UnitValue(
                id='%s-%s' % (id_, j + 1),
                unit=entry,
                unitparameter=meaning)

            for k, (text, source, pages, loc) in enumerate(get_examples(description)):
                rus = ''
                if '  ' in text:
                    text, rus = text.split('  ', 1)
                example = models.Example(
                    id='%s-%s-%s' % (id_, j + 1, k + 1),
                    language=ket,
                    name=text,
                    description=rus,
                    location=loc)
                models.UnitValueSentence(unitvalue=counterpart, sentence=example)

                #
                # FIXME: handle references!
                #

        DBSession.add(entry)
    return offset


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

    with UnicodeReader(args.data_file('Ket_verbs_table.docx.csv')) as reader:
        offset = load(data, reader, ket)

    #Ket_nouns_and_other_pos_table.docx.csv
    #lemma, POS, plural, Russian, German, English, Contexts
    with UnicodeReader(args.data_file('Ket_nouns_and_other_pos_table.docx.csv')) as reader:
        load(data, reader, ket, offset=offset + 1, verbs=False)

    print(stats)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
