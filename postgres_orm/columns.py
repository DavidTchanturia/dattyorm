class Column:
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        self.type = None
        self.unique = unique
        self.nullable = nullable
        self.default = default

    def __repr__(self):
        constraints = ''
        if self.nullable:
            if self.default is not None:
                constraints += f'DEFAULT {self.default}'
        else:
            constraints += 'NOT NULL'
        if self.unique:
            constraints += ' UNIQUE'
        return f'{self.type} {constraints.strip()}'


class PrimaryKey(Column):
    def __init__(self, auto_increment: bool = True) -> None:
        super().__init__(unique=True, nullable=False, default=None)
        self.type = 'SERIAL'
        self.auto_increment = auto_increment

    def __repr__(self):
        constraints = 'PRIMARY KEY'
        return f'{self.type} {constraints}'


class Integer(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'INTEGER'


class Text(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'TEXT'


class VarChar(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'VARCHAR(255)'


class Double(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'DOUBLE'


class Float(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'FLOAT'


class Boolean(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'BOOLEAN'


class Date(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'DATE'


class DateTime(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'DATETIME'