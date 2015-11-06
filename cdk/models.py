from itertools import groupby

from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Unit, Sentence


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.IUnit)
class Entry(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)

    donor = Column(Unicode)
    dialect = Column(Unicode)
    disambiguation = Column(Unicode)
    pos = Column(Unicode)
    aspect = Column(Unicode)
    english = Column(Unicode)
    russian = Column(Unicode)
    german = Column(Unicode)

    def grouped_examples(self):
        return groupby(self.examples, lambda e: e.location)


@implementer(interfaces.ISentence)
class Example(CustomModelMixin, Sentence):
    pk = Column(Integer, ForeignKey('sentence.pk'), primary_key=True)
    entry_pk = Column(Integer, ForeignKey('entry.pk'))
    location = Column(Unicode)

    @declared_attr
    def entry(cls):
        return relationship(Entry, backref=backref('examples', order_by=cls.location))
