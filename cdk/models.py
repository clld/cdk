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
from clld.db.models.common import Unit, Sentence, UnitParameter, UnitValue, Value


class UnitValueSentence(Base):
    unitvalue_pk = Column(Integer, ForeignKey('unitvalue.pk'))
    sentence_pk = Column(Integer, ForeignKey('sentence.pk'))
    description = Column(Unicode())

    unitvalue = relationship(UnitValue, backref='sentence_assocs')
    sentence = relationship(Sentence, backref='unitvalue_assocs', order_by=Sentence.id)


@implementer(interfaces.IUnit)
class Entry(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)

    donor = Column(Unicode)
    dialect = Column(Unicode)
    disambiguation = Column(Unicode)
    pos = Column(Unicode)
    variant = Column(Boolean, default=False)
    aspect = Column(Unicode)
    plural = Column(Unicode)

    def grouped_examples(self):
        return groupby(self.examples, lambda e: e.location)


@implementer(interfaces.IUnitParameter)
class Meaning(CustomModelMixin, UnitParameter):
    pk = Column(Integer, ForeignKey('unitparameter.pk'), primary_key=True)
    english = Column(Unicode)
    russian = Column(Unicode)
    german = Column(Unicode)


@implementer(interfaces.ISentence)
class Example(CustomModelMixin, Sentence):
    pk = Column(Integer, ForeignKey('sentence.pk'), primary_key=True)
    location = Column(Unicode)
