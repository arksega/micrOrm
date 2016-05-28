tables = []


class Mapper(dict):

    def __init__(self, *args, **kwargs):
        super(Mapper, self).__init__(*args, **kwargs)
        self.__dict__.update(self)


def create_schema():
    pass


def engine_factory():
    pass


class EntityMeta(type):
    '''Metaclass to register entities'''

    def __init__(cls, name, bases, attr_dict):
        super(EntityMeta, cls).__init__(name, bases, attr_dict)
        if name != 'Entity':
            assert hasattr(cls, '__tablename')
            print('Register {}'.format(name))
            tables.append(name)


class Entity():
    __metaclass__ = EntityMeta

    def dump(self):
        print (self.__dict__)
        sqlstr = 'CREATE TABLE {} '.format(self._tablename)
        sqlstr += '( \n'
        for attr_name in [atr for atr in dir(self) if not atr.startswith('__')]:
            attr = getattr(self, attr_name)
            if isinstance(attr, Column):
                sqlstr += '{} {},\n'.format(attr_name, attr._type)
        sqlstr += ');'
        return sqlstr

    def create(self):
        self.dump()


class EntityType:
    pass


class Integer(EntityType):
    pass


class String(EntityType):
    pass


class Lob(EntityType):
    pass


class Column(object):
    def __init__(self, _type, primary_key=False, nullable=True):
        self._type = _type
        self.primary_key = primary_key
        self.nullable = nullable
        assert issubclass(_type, EntityType)
