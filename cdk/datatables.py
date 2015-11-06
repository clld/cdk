from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol
from clld.web.datatables.unit import Units
from clld.db.util import get_distinct_values
from clld.web.util.htmllib import HTML

from cdk.models import Entry


class WordCol(LinkCol):
    def get_attrs(self, item):
        return {'label': HTML.span(item.name, ' ', HTML.sup(item.disambiguation))}


class Entries(Units):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, '#'),
            WordCol(self, 'name'),
            Col(self, 'pos', model_col=Entry.pos, choices=get_distinct_values(Entry.pos)),
            Col(self, 'aspect', model_col=Entry.aspect, choices=get_distinct_values(Entry.aspect)),
            Col(self, 'donor', sTitle='loan from', model_col=Entry.donor, choices=get_distinct_values(Entry.donor)),
            Col(self, 'dialect', model_col=Entry.dialect, choices=get_distinct_values(Entry.dialect)),
            Col(self, 'english', model_col=Entry.english),
            Col(self, 'german', model_col=Entry.german),
            Col(self, 'russian', model_col=Entry.russian),
        ]


def includeme(config):
    config.register_datatable('units', Entries)
