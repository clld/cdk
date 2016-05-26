from itertools import groupby

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Unit, Sentence, UnitParameter, UnitValue


class CounterpartExample(Base):
    unitvalue_pk = Column(Integer, ForeignKey('unitvalue.pk'))
    sentence_pk = Column(Integer, ForeignKey('sentence.pk'))
    location = Column(Unicode())

    @declared_attr
    def sentence(cls):
        return relationship(
            Sentence,
            backref=backref('examples', order_by=[cls.location, cls.sentence_pk]))

    @declared_attr
    def counterpart(cls):
        return relationship(
            UnitValue,
            backref=backref('examples', order_by=[cls.location, cls.sentence_pk]))


@implementer(interfaces.IUnit)
class Entry(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)

    donor = Column(Unicode)
    disambiguation = Column(Unicode)
    pos = Column(Unicode)
    variant = Column(Boolean, default=False)
    aspect = Column(Unicode)
    plural = Column(Unicode)

    @property
    def variants(self):
        res = []
        vars = [v.entry2 for v in self.variants1] + [v.entry1 for v in self.variants2]
        for lang, vars in groupby(
                sorted(vars, key=lambda v: v.language.name), lambda v: v.language.name):
            res.append((lang, list(vars)))
        return res


class Variants(Base):
    entry1_pk = Column(Integer, ForeignKey('unit.pk'))
    entry2_pk = Column(Integer, ForeignKey('unit.pk'))

    entry1 = relationship(Entry, foreign_keys=[entry1_pk], backref='variants1')
    entry2 = relationship(Entry, foreign_keys=[entry2_pk], backref='variants2')


@implementer(interfaces.IUnitParameter)
class Meaning(CustomModelMixin, UnitParameter):
    pk = Column(Integer, ForeignKey('unitparameter.pk'), primary_key=True)
    english = Column(Unicode)
    russian = Column(Unicode)
    german = Column(Unicode)
