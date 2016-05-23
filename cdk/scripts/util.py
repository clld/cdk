# coding: utf8
from __future__ import unicode_literals, print_function, division
import re
from collections import defaultdict
from itertools import groupby

from clld.db.meta import DBSession
from clld.db.models import common

from cdk import models


POS = {
    '?': '?',
    'adj': 'adjective',
    'adp': 'postposition',
    'adv': 'adverb',
    'anom': 'action nominal',
    'an': 'animate',
    'an pl': 'animate plural',
    'conj': 'conjunction',
    'f': 'feminine class',
    'inan': 'inanimate',
    'inan pl': 'inanimate plural',
    'interj': 'interjection',
    'm': 'masculine class',
    'mn': 'masculine/neuter class',
    'n': 'neuter class',
    'n?': 'neuter class?',
    'n/m': 'masculine/neuter class',
    'm/n': 'masculine/neuter class',
    'm/f': 'masculine/feminine class',
    'm/f/n': 'masculine/feminine/neuter class',
    'f/m': 'masculine/feminine class',
    'f/n': 'feminine/neuter class',
    'n/f': 'feminine/neuter class',
    'no pl': 'no plural form',
    'num': 'numeral',
    'num an': 'animate numeral',
    'num inan': 'inanimate numeral',
    'pron attr': 'attributive pronoun',
    'pron dem': 'demonstrative pronoun',
    'pron indef': 'indefinite pronoun',
    'pron indef m': 'masculine indefinite pronoun',
    'pron indef f': 'feminine indefinite pronoun',
    'pron indef an pl': 'animate plural indefinite pronoun',
    'pron inter': 'interrogative pronoun',
    'pron inter f': 'feminine interrogative pronoun',
    'pron inter m': 'masculine interrogative pronoun',
    'pron intens/refl': 'intens/refl pronoun',
    'pron pers': 'personal pronoun',
    'pron poss': 'possesive pronoun',
    'pron rel': 'relative pronoun',
    'prtc': 'particle',
    'prt\u0441': 'particle',
    'pl': 'plural',
    'pron': 'pronoun',
    'suf': 'suffix',
    'v': 'intransitive verb',
    'v irr': 'irregular intransitive verb',
    'v1': 'v1 - intransitive verb',
    'v1/4': 'v1/4 - intransitive verb',
    'v2': 'v2 - intransitive verb',
    'v2/5': 'v2/5 - intransitive verb',
    'v3': 'v3 - intransitive verb',
    'v3~v5': 'v3~v5 - intransitive verb',
    'v4': 'v4 - intransitive verb',
    'v5': 'v5 - intransitive verb',
    'vk': 'verb with incorporated subjects',
    'vpred': 'verbal predicate',
    'vt': 'tranbsitive verb',
    'vt irr': 'irregular tranbsitive verb',
    'vt1': 'vt1 - tranbsitive verb',
    'vt2': 'vt2 - tranbsitive verb',
    'vt2/4': 'vt2/4 - tranbsitive verb',
    'vt3': 'vt3 - tranbsitive verb',
    'vt4': 'vt4 - tranbsitive verb',
}

ASPECTS = {
    'caus mom': 'causative momentaneous verb',
    'caus iter': 'causative iterative verb',
    '': '',
}

DIALECTS = {
    'cket': 'Central Ket',
    'sket': 'Southern Ket',
    'nket': 'Northern Ket',
}

DONORS = {
    'nen': 'Nenets',
    'rus': 'Russian',
    'selk': 'Selkup',
    'evenk': 'Evenk',

}

LOCATIONS = {
    'leb': 'Lebed',
    'imb': 'Imbat',
    'bak': 'Baklanikha',
    'baikh': 'Baikha',
    'baikn': 'Baikha',
    'baix': 'Baikha',
    'bajk': 'Baikit',
    'bakht': 'Bakhta',
    'bakh': 'Bakhta',
    'baxt': 'Bakhta',
    'bacht': 'Bakhta',
    'el': 'Yelogui settlements',
    'e.-o': 'Yenisei Ostyak',
    'kel': 'Kellog',
    'ke': 'Kellog',
    'kur': 'Kureika',
    'mad': 'Maduika',
    'pak': 'Pakulikha',
    'al': 'Alinskoe',
    '\u0430l': 'Alinskoe',
    'ak': 'Alinskoe',
    'ver': 'Vereshchagino',
    'v-imb': 'Verkhne-Imbatsk',
    'sul': 'Sulomai',
    'sum': 'Sumarokovo',
    'sur': 'Surgutikha',
}


def string2regex(s):
    return s.replace('.', '\\.').replace('-', '\\-')


DIS_ROMAN_PATTERN = re.compile('\s+(?P<marker>I+)\s*$')
DIS_ARABIC_PATTERN = re.compile('(?P<marker>[1-9]+)$')
DONOR_PATTERN = re.compile('\s*<(?P<name>%s)\.\s*>\s*' % '|'.join(DONORS.keys()))

# dialectal variants in braces:
VARIANTS_PATTERN = re.compile('\((%s)(\.|\s+)' % '|'.join(DIALECTS.keys()))

DIALECT_MARKER_PATTERN = re.compile('(?P<name>ket|%s)(\.\s*|\.?\s+)' % '|'.join(DIALECTS.keys()))

DIALECT_CHUNK_PATTERN = re.compile(',\s*(?:%s)\.\s*' % '|'.join(DIALECTS.keys()))

LOC_PATTERN = re.compile('(?:(?:\]|\?|,|\s\s)\s*|^)(%s)\.\s+' % '|'.join(string2regex(s) for s in LOCATIONS.keys()))

SOURCE_PATTERN = re.compile('\s*\((?P<src>[^:\(\)]+):\s*(?P<pages>[^\)]+)(?:\)\s*$|\),?\s*)')
SOURCE_MARKER = re.compile('\s*\((?P<src>[^:\(\)]+):\s*(?P<pages>[^\)]+)\)$')

MEANING_ID = 0
ENTRY_ID = 0
EXAMPLE_ID = 0
SOURCE_ID = 0
PROBLEMS = []


def in_brackets(s):
    depth = 0
    for index, c in enumerate(s):
        if c == '(':
            depth += 1
        if c == ')':
            depth -= 1
            if depth == 0:
                return s[1:index].strip(), s[index + 1:].strip()
    return '', s


def yield_variants(s):
    dialects, prev_dialects = [], []
    for chunk in s.split(','):
        chunk = chunk.strip()
        if chunk in DIALECTS:
            chunk += '.'
        if DIALECT_MARKER_PATTERN.match(chunk):
            dialect, form = [ss.strip() for ss in chunk.split('.', 1)]
            dialects.append(dialect)
            if form:
                for dialect in dialects:
                    yield dialect, form
                prev_dialects = dialects[:]
                dialects = []
        else:
            # additional form for the last encountered dialect!
            form = chunk
            try:
                assert prev_dialects and form
            except:
                print(s)
                raise
            for dialect in prev_dialects:
                yield dialect, form
    for dialect in dialects:
        yield dialect, None


class Headword(object):
    def __init__(self, headword):
        self.donor, self.dialects, self.variants = None, [], defaultdict(list)
        match = DONOR_PATTERN.search(headword)
        if match:
            self.donor = match.group('name')
            headword = headword[:match.start()] + headword[match.end():]
        match = VARIANTS_PATTERN.search(headword)
        if match:
            # get matching closing bracket!
            variants, rem = in_brackets(headword[match.start():])
            for i, (dialect, form) in enumerate(yield_variants(variants)):
                if not form:
                    self.dialects.append(dialect)
                else:
                    self.variants[dialect].append(form)

            headword = headword[:match.start()] + rem

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


def yield_examples(s):
    chunks = [ss.strip() for ss in LOC_PATTERN.split(s)]
    if chunks[0]:
        #try:
        #    assert len(chunks) == 1
        #except AssertionError:
        #    print(chunks[0])
        #    raise
        for res in yield_cited_examples(chunks[0]):
            yield res

    local_examples = [chunks[i:i + 2] for i in range(1, len(chunks), 2)]

    for i, (dialect, chunk) in enumerate(local_examples):
        parts = chunk.split('  ', 2)
        if len(parts) == 1:
            PROBLEMS.append(1)
            parts.append('')

        src_match = SOURCE_MARKER.search(parts[1])
        if src_match:
            src, pages = src_match.group('src'), src_match.group('pages')
            rus = parts[1][:src_match.start()]
        else:
            src, pages = None, None
            rus = parts[1]
        yield dialect, parts[0], rus, src, pages
        if len(parts) > 2:
            for res in yield_cited_examples(parts[2]):
                yield res


def yield_cited_examples(s):
    chunks = [ss.strip() for ss in SOURCE_PATTERN.split(s)]
    count, rem = divmod(len(chunks), 3)
    try:
        assert rem == 1 and not chunks[-1]
    except AssertionError:
        PROBLEMS.append(1)
        yield None, chunks[-1], None, None, None

    for chunk, src, pages in [chunks[i:i + 3] for i in range(0, count * 3, 3)]:
        parts = chunk.split('  ')
        try:
            assert len(parts) == 2
            yield None, parts[0], parts[1], src, pages
        except AssertionError:
            PROBLEMS.append(1)
            yield None, '  '.join(parts), None, src, pages


def get_entry(**kw):
    global ENTRY_ID
    ENTRY_ID += 1
    kw['pos'] = POS[kw['pos']] if kw['pos'] else None
    kw['donor'] = DONORS[kw['donor']] if kw['donor'] else None
    return models.Entry(id=str(ENTRY_ID), **kw)


def load(data, reader, ket, contrib, verbs=True):
    dis_arabic_pattern = re.compile('(?P<marker>[0-9]+)\.\s+')
    global MEANING_ID
    global EXAMPLE_ID
    global SOURCE_ID

    for headword, meanings in groupby(reader, lambda r: (r[0], r[1], r[2])):
        meanings = list(meanings)
        if not meanings:
            continue

        headword, pos, aspect_or_plural = headword
        pos = pos.strip()
        if (not pos and not headword) or (headword == 'lemma' and pos == 'POS'):
            continue
        assert (not pos) or (pos in POS), 'pos: %s, %s' % pos

        headword = Headword(headword)
        entries = []

        if headword.dialects:
            for dialect in headword.dialects:
                entries.append(get_entry(
                    name=headword.form,
                    donor=headword.donor,
                    disambiguation=headword.disambiguation,
                    pos=pos,
                    aspect=aspect_or_plural if verbs else None,
                    plural=None if verbs else aspect_or_plural,
                    language=data['Language'][dialect]))
        else:
            entries.append(get_entry(
                name=headword.form,
                donor=headword.donor,
                disambiguation=headword.disambiguation,
                pos=pos,
                aspect=aspect_or_plural if verbs else None,
                plural=None if verbs else aspect_or_plural,
                language=ket))

        for dialect, forms in headword.variants.items():
            for form in forms:
                entries.append(get_entry(
                    name=form,
                    donor=headword.donor,
                    disambiguation=headword.disambiguation,
                    pos=pos,
                    aspect=aspect_or_plural if verbs else None,
                    plural=None if verbs else aspect_or_plural,
                    language=ket if dialect is None else data['Language'][dialect]))

        for j, row in enumerate(meanings):
            try:
                headword, pos, aspect, russian, german, english, description = row
            except:
                for l, col in enumerate(row):
                    print(l, col)
                raise
            match = dis_arabic_pattern.match(russian)
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
            #else:
            #    print('known meaning: %s, %s, %s' % (russian, german, english))

            for entry in entries:
                counterpart = common.UnitValue(
                    id='%s-%s' % (entry.id, j + 1),
                    name=entry.name,
                    description='%s / %s / %s' % (english, russian, german),
                    contribution=contrib,
                    unit=entry,
                    unitparameter=meaning)

                #try:
                #    examples = list(yield_examples(description))
                #except:
                #    print(description)
                #    raise

                for k, (loc, text, rus, source, pages) in enumerate(yield_examples(description)):
                    #if dialect == 'ket':
                    #    dialect = None
                    #rus = ''
                    #if '  ' in text:
                    #    text, rus = text.split('  ', 1)

                    example = data['Sentence'].get((text, rus))
                    if example is None:
                        EXAMPLE_ID += 1
                        example = common.Sentence(
                            id='%s' % EXAMPLE_ID,
                            language=ket,  # if dialect is None else data['Language'][dialect],
                            name=text,
                            description=rus)
                        if source:
                            src = data['Source'].get(source)
                            if not src:
                                SOURCE_ID += 1
                                src = data.add(
                                    common.Source, source,
                                    id=str(SOURCE_ID),
                                    name=source,
                                    description=None)
                            DBSession.add(common.SentenceReference(
                                sentence=example, source=src, description=pages))
                    models.CounterpartExample(
                        location=LOCATIONS[loc] if loc else None,
                        counterpart=counterpart,
                        sentence=example)

                    #
                    # FIXME: handle references!
                    #

        for entry in entries:
            DBSession.add(entry)
