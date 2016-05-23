from sqlalchemy.orm import joinedload, joinedload_all
from markupsafe import Markup

from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol
from clld.web.datatables.unit import Units
from clld.web.datatables.unitvalue import Unitvalues
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values
from clld.web.util.htmllib import HTML

from cdk.models import Entry, Meaning
from cdk import util


class WordCol(LinkCol):
    def get_attrs(self, item):
        item = self.get_obj(item)
        return {'label': HTML.span(util.form(item.name), ' ', HTML.sup(item.disambiguation))}


class DialectCol(LinkCol):
    def search(self, qs):
        return common.Language.id == qs

    def order(self):
        return common.Language.pk


class Entries(Units):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, '#'),
            WordCol(self, 'name'),
            Col(self, 'pos', model_col=Entry.pos, choices=get_distinct_values(Entry.pos)),
            Col(self, 'aspect', model_col=Entry.aspect, choices=get_distinct_values(Entry.aspect)),
            Col(self, 'plural', model_col=Entry.plural, choices=get_distinct_values(Entry.plural)),
            Col(self, 'donor', sTitle='loan from', model_col=Entry.donor, choices=get_distinct_values(Entry.donor)),
            DialectCol(
                self,
                'variety',
                get_object=lambda u: u.language,
                choices=[(l.id, l.name) for l in DBSession.query(common.Language)]),
        ]


class Counterparts(Unitvalues):
    def base_query(self, query):
        query = query \
            .join(common.Unit) \
            .join(common.Unit.language) \
            .join(common.UnitParameter) \
            .options(
                joinedload_all(common.UnitValue.unit, common.Unit.language),
                joinedload(common.UnitValue.unitparameter))

        if self.unit:
            return query.filter(common.UnitValue.unit_pk == self.unit.pk)

        if self.unitparameter:
            return query.filter(
                common.UnitValue.unitparameter_pk == self.unitparameter.pk)

        if self.contribution:
            return query.filter(common.UnitValue.contribution_pk == self.contribution.pk)

        return query

    def col_defs(self):
        return [
            DetailsRowLinkCol(self, '#'),
            WordCol(
                self,
                'form',
                get_obj=lambda i: i.unit,
                model_col=common.Unit.name),
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
    config.register_datatable('units', Entries)
