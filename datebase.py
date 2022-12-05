import psycopg2


class Datebase:
    def __init__(self, name, host, user):
        self.name = name
        self.host = host
        self.user = user
        self.tables = []
        self.quiet = False

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.host, user=self.user, database=self.name)
        self.cursor = self.connection.cursor()
        print(self.name, "starts")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def set_tables(self, tables):
        self.tables.extend(tables)

    def do(self, quiet=False):
        self.quiet = quiet
        for table in self.tables:
            table.create()

    def execute(self, sql):
        try:
            if (not self.quiet):
                print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
            if (not self.quiet):
                print("SUCCESS\n")
        except (psycopg2.errors.DuplicateTable, psycopg2.errors.DuplicateColumn) as e:
            self.connection.rollback()
            print("FAILED: ", e)
        except psycopg2.errors.InvalidTableDefinition as e:
            self.connection.rollback()
            print("FAILED: ", e)


class Column:
    def __init__(self, name, table, data_type, is_unq=False, is_pkey=False, is_nullable=False, default=None, fkey=None):
        self.name = name
        self.table = table
        self.data_type = data_type
        self.is_unq = is_unq
        self.is_pkey = is_pkey
        self.is_nullable = is_nullable
        self.default = default
        self.fkey = fkey

    def add(self):
        self.table.execute(
            f"ALTER TABLE {self.table.name} ADD COLUMN {self.name} {self.data_type}")
        if (self.is_unq):
            self.add_unq()
        if (self.is_pkey):
            self.add_pkey()
        if (not self.is_nullable):
            self.add_nullable()
        if (self.default):
            self.add_default()
        if (self.fkey):
            self.add_fkey()

    def add_unq(self):
        self.table.execute(
            f"ALTER TABLE {self.table.name} ADD CONSTRAINT \"{self.table.name}_{self.name}_unq\" UNIQUE({self.name})")

    def add_pkey(self):
        self.table.execute(
            f"ALTER TABLE {self.table.name} ADD CONSTRAINT \"{self.table.name}_{self.name}_pkey\" PRIMARY KEY({self.name})")

    def add_nullable(self):
        self.table.execute(
            f"ALTER TABLE {self.table.name} ALTER COLUMN {self.name} SET NOT NULL")

    def add_default(self):
        if (self.data_type in ['TEXT', 'TIME', 'DATE', 'INTERVAL']):
            self.default = f"\'{self.default}\'"
        self.table.execute(
            f"ALTER TABLE {self.table.name} ALTER COLUMN {self.name} SET DEFAULT {self.default}")

    def add_fkey(self):
        self.table.execute(
            f"ALTER TABLE {self.table.name} ADD FOREIGN KEY ({self.name}) REFERENCES {self.fkey.table.name} ({self.fkey.name})")


class Table:
    def __init__(self, name, datebase):
        self.name = name
        self.datebase = datebase
        self.columns = []

    def set_columns(self, columns):
        self.columns.extend(columns)

    def create(self):
        self.datebase.execute(f"CREATE TABLE {self.name}()")
        self.add_columns()

    def add_columns(self):
        for c in self.columns:
            c.add()

    def execute(self, sql):
        self.datebase.execute(sql)
