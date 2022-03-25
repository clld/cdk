from sqlalchemy.orm import joinedload

from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol
from clld.web.datatables.unit import Units
from clld.web.datatables.unitvalue import Unitvalues
from clld.web.datatables.sentence import Sentences
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML

from cdk.models import Entry, Meaning, CounterpartExample
from cdk import util


class RefsCol(Col):
    def search(self, qs):
        return common.Source.name == qs

    def order(self):
        return common.Source.name

    def format(self, item):
        return HTML.ul(*[HTML.li(link(self.dt.req, ref.source), ': ', ref.description) for ref in item.references], class_='unstyled')


class LocationCol(Col):
    def search(self, qs):
        return CounterpartExample.location == qs

    def order(self):
        return CounterpartExample.location

    def format(self, item):
        return HTML.ul(*[HTML.li(ex.location) for ex in item.examples], class_='unstyled')


class Examples(Sentences):
    def base_query(self, query):
        query = query.outerjoin(common.Sentence.examples)
        query = query.outerjoin(common.Sentence.references, common.Source)
        query = query.options(
            joinedload(common.Sentence.examples),
            joinedload(common.Sentence.references).joinedload(common.SentenceReference.source))
        return query.distinct()

    def col_defs(self):
        res = Sentences.col_defs(self)
        return [
            res[1],
            res[4],
            LocationCol(self, 'settlement', choices=get_distinct_values(CounterpartExample.location)),
            RefsCol(self, 'source', choices=get_distinct_values(common.Source.name)),
            res[6]]


class WordCol(LinkCol):
    def get_attrs(self, item):
        item = self.get_obj(item)
        form = util.form(item.name)
        if item.variant:
            form = HTML.i(form)
        return {'label': HTML.span(form, ' ', HTML.sup(item.disambiguation))}


class DialectCol(Col):
    def search(self, qs):
        return common.Language.id == qs

    def order(self):
        return common.Language.pk

    def format(self, item):
        item = self.get_obj(item)
        return item.name


class VariantCol(Col):
    def __init__(self, dt, name, **kw):
        kw['sDescription'] = 'If "yes" the word is a dialectal variant.'
        kw['sFilter'] = '2'
        kw['model_col'] = Entry.variant
        kw['choices'] = [('1', 'yes'), ('2', 'no')]
        Col.__init__(self, dt, name, **kw)

    def search(self, qs):
        if qs == '1':
            return Entry.variant == True
        if qs == '2':
            return Entry.variant == False

    def format(self, item):
        item = self.get_obj(item)
        return 'yes' if item.variant else 'no'


class Entries(Units):
    def col_defs(self):
        return [
            WordCol(self, 'name'),
            VariantCol(self, 'variant'),
            Col(self, 'pos', model_col=Entry.pos, choices=get_distinct_values(Entry.pos)),
            Col(self, 'aspect', model_col=Entry.aspect, choices=get_distinct_values(Entry.aspect)),
            Col(self, 'plural', model_col=Entry.plural, choices=get_distinct_values(Entry.plural)),
            Col(self, 'donor', sTitle='loan from', model_col=Entry.donor, choices=get_distinct_values(Entry.donor)),
            DialectCol(
                self,
                'variety',
                model_col=common.Language.name,
                choices=[(l.id, l.name) for l in DBSession.query(common.Language)]),
        ]


class Counterparts(Unitvalues):
    def base_query(self, query):
        query = query \
            .join(common.Unit) \
            .join(common.Unit.language) \
            .join(common.UnitParameter) \
            .options(
                joinedload(common.UnitValue.unit).joinedload(common.Unit.language),
                joinedload(common.UnitValue.unitparameter))

        if self.unit:
            return query.filter(common.UnitValue.unit_pk == self.unit.pk)

        if self.unitparameter:
            return query.filter(
                common.UnitValue.unitparameter_pk == self.unitparameter.pk)

        if self.contribution:
            return query.filter(common.UnitValue.contribution_pk == self.contribution.pk)

        return query

    def toolbar(self):
        return self._toolbar.render(no_js=True)

    def col_defs(self):
        return [
            DetailsRowLinkCol(self, '#'),
            WordCol(
                self,
                'form',
                get_obj=lambda i: i.unit,
                model_col=common.Unit.name),
            VariantCol(self, 'variant', get_object=lambda u: u.unit),
            Col(
                self,
                'english',
                get_obj=lambda i: i.unitparameter,
                model_col=common.UnitParameter.name),
            Col(
                self,
                'russian',
                get_obj=lambda i: i.unitparameter,
                model_col=Meaning.russian),
            Col(self, 'pos', get_object=lambda u: u.unit, model_col=Entry.pos),
            Col(self, 'aspect', get_object=lambda u: u.unit, model_col=Entry.aspect),
            Col(self, 'plural', get_object=lambda u: u.unit, model_col=Entry.plural),
            Col(
                self,
                'donor',
                choices=get_distinct_values(Entry.donor),
                get_object=lambda u: u.unit,
                model_col=Entry.donor),
            DialectCol(
                self,
                'variety',
                get_object=lambda u: u.unit.language,
                choices=[(l.id, l.name) for l in DBSession.query(common.Language)]),
        ]


def includeme(config):
    config.register_datatable('unitvalues', Counterparts)
    config.register_datatable('sentences', Examples)
    config.register_datatable('units', Entries)
