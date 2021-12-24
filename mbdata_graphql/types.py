from graphene import ObjectType, Field, Int
from graphene_sqlalchemy.converter import convert_sqlalchemy_composite

from mbdata import types as mbt


class PartialDate(ObjectType):
    year = Int()
    month = Int()
    day = Int()


@convert_sqlalchemy_composite.register(mbt.PartialDate)
def convert_partial_data(composite, registry):
    return Field(PartialDate)
