class TableMeta(type):
    """this is a metaclass that will turn class variables to fields
    so tht I can iterate over them and use them in a query"""
    def __new__(cls, name, bases, dct):
        fields = {k: v for k, v in dct.items() if not k.startswith("__")}
        dct['fields'] = fields

        return super().__new__(cls, name, bases, dct)


class BaseModel(metaclass=TableMeta):
    pass
