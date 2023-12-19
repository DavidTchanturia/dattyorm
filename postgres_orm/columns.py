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
                constraints += f'DEFAULT {str(self.default)}'
        else:
            constraints += 'NOT NULL'
        if self.unique:
            constraints += ' UNIQUE'
        return f'{self.type} {constraints.strip()}'


class PrimaryKey(Column):
    def __init__(self, auto_increment: bool = True) -> None:
        super().__init__(unique=True, nullable=False, default=None)
        self.type = 'BIGSERIAL' if auto_increment else 'INTEGER'  # BIGSERIAL avoids creating seperate sequence for autoincremented id
        self.auto_increment = auto_increment

    def __repr__(self):
        constraints = 'PRIMARY KEY'
        return f'{self.type} {constraints}'


class Integer(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: int = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'INTEGER'


class Text(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'TEXT'


class VarChar(Column):
    def __init__(self, size: int = 255, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = f'VARCHAR({size})'  # either create VARCHAR(255) or any other size as your wishes


class Double(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: float = None) -> None:
        super().__init__(unique, nullable, default)
        self.type = 'DOUBLE'


class Float(Column):
    def __init__(self, unique: bool = False,
                 nullable: bool = True, default: float = None) -> None:
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

