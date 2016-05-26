# coding: utf8
from __future__ import unicode_literals, print_function, division
import re
from collections import defaultdict
from itertools import groupby, chain, combinations
import io

from clld.db.meta import DBSession
from clld.db.models import common

from cdk import models


SOURCE_MAP = {
    'WΕR2': 'WER2',
    'CHCC81': 'СНСС81',
    'СНCC81': 'СНСС81',
    'МКД': 'МКД1',
    'CHCC76': 'СНСС76',
    'WΕR1': 'WER1',
    'СНСC72': 'СНСС72',
    'CНCC72': 'СНСС72',
    'CHCC72': 'СНСС72',
    'КС': 'КСД',
    'АК60': 'ЛЯНС11',
    'K67': 'К67',
    'КТФ': 'КФТ',
    'КСб13': 'КСб',
}


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
    'pron intens/refl': 'intensive/reflexive pronoun',
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
    'vt': 'transitive verb',
    'vt irr': 'irregular transitive verb',
    'vt1': 'vt1 - transitive verb',
    'vt2': 'vt2 - transitive verb',
    'vt2/4': 'vt2/4 - transitive verb',
    'vt3': 'vt3 - transitive verb',
    'vt4': 'vt4 - transitive verb',
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
    'bajk': 'Bajkit',
    'bakht': 'Bakhta',
    'bakh': 'Bakhta',
    'baxt': 'Bakhta',
    'bacht': 'Bakhta',
    'el': 'Yelogui settlements',
    'e.-o': 'Yenisei Ostyak',
    'kel': 'Kellog',
    'ke': 'Kellog',
    'kur': 'Kurejka',
    'mad': 'Madujka',
    'pak': 'Pakulikha',
    'al': 'Alinskoe',
    '\u0430l': 'Alinskoe',
    'ak': 'Baklanikha',
    'ver': 'Vereshchagino',
    'v-imb': 'Verkhne-Imbatsk',
    'sul': 'Sulomaj',
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

LOC_PATTERN = re.compile('(?:(?:\]|\?|!|,|\s\s)\s*|^)(%s)\.,?\s+' %
                         '|'.join(string2regex(s)
                                  for s in chain(LOCATIONS.keys(), DIALECTS.keys())))

SOURCE_PATTERN = re.compile('\s*\((?P<src>[^:\s\(\)]+):\s*(?P<pages>[^\)]+)(?:\)\s*$|\),?\s*)')
SOURCE_MARKER = re.compile('\s*\((?P<src>[^:\s\(\)]+):\s*(?P<pages>[^\)]+)\),?\s*')

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
            assert prev_dialects and form
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
        for res in yield_cited_examples(chunks[0]):
            yield res

    local_examples = [chunks[i:i + 2] for i in range(1, len(chunks), 2)]

    for i, (dialect, chunk) in enumerate(local_examples):
        parts = chunk.split('  ', 2)
        if len(parts) == 1:
            PROBLEMS.append(s)
            parts.append('')

        src_match = SOURCE_MARKER.search(parts[1])
        if src_match:
            src, pages = src_match.group('src'), src_match.group('pages')
            rus = parts[1][:src_match.start()]
            if parts[1][src_match.end():].strip():
                parts.insert(2, parts[1][src_match.end():].strip())
        else:
            src, pages = None, None
            rus = parts[1]
        text = parts[0]
        match = DIALECT_MARKER_PATTERN.match(text)
        if match:
            text = text[match.end():].strip()
            yield match.group('name'), text, rus, src, pages
        yield dialect, text, rus, src, pages
        if len(parts) > 2:
            for res in yield_cited_examples('  '.join(parts[2:])):
                yield res


def yield_cited_examples(s):
    done = False
    chunks = [ss.strip() for ss in SOURCE_PATTERN.split(s)]
    if len(chunks) == 1:
        cchunks = chunks[0].split('  ')
        if len(cchunks) % 2 == 0:
            for text, rus in [cchunks[i:i + 2] for i in range(0, len(cchunks), 2)]:
                yield None, text, rus, None, None
            done = True

    if not done:
        count, rem = divmod(len(chunks), 3)
        try:
            assert rem == 1 and not chunks[-1]
        except AssertionError:
            PROBLEMS.append(s)
            yield None, chunks[-1], None, None, None

        for chunk, src, pages in [chunks[i:i + 3] for i in range(0, count * 3, 3)]:
            parts = chunk.split('  ')
            if len(parts) == 4:
                yield None, parts[0], parts[1], None, None
                parts = parts[2:]
            try:
                assert len(parts) == 2
                yield None, parts[0], parts[1], src, pages
            except AssertionError:
                PROBLEMS.append(s)
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
        kw = dict(
            donor=headword.donor,
            disambiguation=headword.disambiguation,
            pos=pos,
            aspect=aspect_or_plural if verbs else None,
            plural=None if verbs else aspect_or_plural,)

        if headword.dialects:
            for dialect in headword.dialects:
                entries.append(get_entry(
                    name=headword.form,
                    language=data['Language'][dialect],
                    **kw))
        else:
            entries.append(get_entry(name=headword.form, language=ket, **kw))

        for dialect, forms in headword.variants.items():
            for form in forms:
                entries.append(get_entry(
                    name=form,
                    language=ket if dialect is None else data['Language'][dialect],
                    **kw))

        DBSession.flush()
        for e1, e2 in combinations(entries, 2):
            DBSession.add(models.Variants(entry1=e1, entry2=e2))

        for j, row in enumerate(meanings):
            headword, pos, aspect, russian, german, english, description = row
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

            for entry in entries:
                counterpart = common.UnitValue(
                    id='%s-%s' % (entry.id, j + 1),
                    name=entry.name,
                    description='%s / %s / %s' % (english, russian, german),
                    contribution=contrib,
                    unit=entry,
                    unitparameter=meaning)

                for k, (loc, text, rus, source, pages) in enumerate(yield_examples(description)):
                    example = data['Sentence'].get((text, rus, loc))
                    if example is None:
                        EXAMPLE_ID += 1
                        example = data.add(
                            common.Sentence,
                            (text, rus, loc),
                            id='%s' % EXAMPLE_ID,
                            language=data['Language'].get(loc, ket),
                            name=text,
                            description=rus)
                        if source:
                            source = SOURCE_MAP.get(source, source)
                            src = data['Source'].get(source)
                            if not src:
                                print(source)
                                raise ValueError(source)
                                SOURCE_ID += 1
                                src = data.add(
                                    common.Source, source,
                                    id=str(SOURCE_ID),
                                    name=source,
                                    description=None)
                            DBSession.add(common.SentenceReference(
                                sentence=example, source=src, description=pages))
                    models.CounterpartExample(
                        location=LOCATIONS.get(loc, DIALECTS.get(loc)),
                        counterpart=counterpart,
                        sentence=example)

        for entry in entries:
            DBSession.add(entry)

        with io.open('context-problems.txt', 'w', encoding='utf8') as fp:
            fp.write('\n\n'.join(PROBLEMS))
