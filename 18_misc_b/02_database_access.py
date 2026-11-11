import sqlite3
import tempfile
from pathlib import Path

# DB-API 2.0: every Python database driver works the same way:
#   connect() -> connection;  connection.cursor() / execute() -> cursor;
#   cursor.execute(sql, parameters);  fetchone() / fetchall();  commit() / rollback();  close()
# sqlite3 ships with Python and stores a database in ONE file (or in memory).

HERE = Path(__file__).parent
SQL = HERE / "sql"
schema_sql = (SQL / "schema.sql").read_text(encoding="utf-8")
seed_sql = (SQL / "seed.sql").read_text(encoding="utf-8")


def load_queries(path):
    """Read 'name -> SQL' pairs from a file whose queries start with '-- name: xxx'."""
    queries, name, lines = {}, None, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name:"):
            if name:
                queries[name] = "\n".join(lines).strip()
            name, lines = line.split(":", 1)[1].strip(), []
        elif name:
            lines.append(line)
    if name:
        queries[name] = "\n".join(lines).strip()
    return queries


q = load_queries(SQL / "queries.sql")
print(sqlite3.paramstyle)                       # qmark       (the placeholder style is ?)

# 1. Connect, create the tables, load the sample data
conn = sqlite3.connect(":memory:")              # a database that lives only in memory
conn.execute("PRAGMA foreign_keys = ON")        # SQLite does not check foreign keys unless asked
conn.executescript(schema_sql)                  # executescript runs MANY statements
conn.executescript(seed_sql)

# 2. SELECT
print(conn.execute(q["count"]).fetchone())      # (4,)
print(conn.execute(q["all_employees"]).fetchall())
# [(1, 'Ann', 'IT', 5000), (2, 'Bob', 'IT', 4000), (3, 'Cy', 'HR', 3500), (4, 'Di', 'Ops', 4500)]

# 3. Parameters: ? (by position) or :name (by name). NEVER build SQL with f-strings.
print(conn.execute(q["by_dept"], ("IT",)).fetchall())                   # [('Ann',), ('Bob',)]
print(conn.execute(q["by_dept_named"], {"dept": "IT", "min_salary": 4500}).fetchall())
# [('Ann', 5000)]
print(conn.execute(q["stats_by_dept"]).fetchall())
# [('HR', 1, 3500.0), ('IT', 2, 4500.0), ('Ops', 1, 4500.0)]
print(conn.execute(q["with_floor"]).fetchall())
# [('Ann', 3), ('Bob', 3), ('Cy', 1), ('Di', 2)]

# 4. INSERT, UPDATE, DELETE and what the cursor tells you
cur = conn.execute(q["insert_employee"], ("Ed", "Ops", 3000))
print(cur.lastrowid, cur.rowcount)              # 5 1       the new id and the rows changed

cur = conn.executemany(q["insert_employee"], [("Fay", "HR", 3600), ("Gus", "IT", 4100)])
print(cur.rowcount)                             # 2

cur = conn.execute(q["raise_salary"], (100, "IT"))
print(cur.rowcount)                             # 3         Ann, Bob and Gus
print(conn.execute(q["salary_of"], ("Ann",)).fetchone())                # (5100,)

cur = conn.execute(q["delete_employee"], ("Ed",))
print(cur.rowcount, conn.execute(q["count"]).fetchone()[0])             # 1 6
conn.commit()                                   # make the changes permanent

# 5. A TRANSACTION is all-or-nothing. "with conn" commits, or rolls back on an error.
try:
    with conn:
        conn.execute(q["insert_employee"], ("Hal", "IT", 1000))
        conn.execute(q["insert_employee"], ("Ann", "IT", 1000))         # the name is UNIQUE
except sqlite3.IntegrityError as e:
    print(type(e).__name__, conn.execute(q["count"]).fetchone()[0])     # IntegrityError 6
    # Hal was rolled back too

# 6. The database enforces its rules (NOT NULL, UNIQUE, CHECK, FOREIGN KEY)
for row in [("Zed", "IT", -5), ("Yan", "XX", 100)]:
    try:
        conn.execute(q["insert_employee"], row)
    except sqlite3.IntegrityError as e:
        print(e)
# CHECK constraint failed: salary > 0
# FOREIGN KEY constraint failed
conn.rollback()

# 7. Fetching: one, many, all, or loop over the cursor
cur = conn.execute(q["all_employees"])
print(cur.fetchone())                           # (1, 'Ann', 'IT', 5100)
print(cur.fetchmany(2))                         # [(2, 'Bob', 'IT', 4100), (3, 'Cy', 'HR', 3500)]
print(len(cur.fetchall()))                      # 3
print([d[0] for d in cur.description])          # ['id', 'name', 'dept', 'salary']

for row in conn.execute(q["by_dept"], ("HR",)):
    print(row)
# ('Cy',)
# ('Fay',)

# 8. Rows you can read by column name
conn.row_factory = sqlite3.Row
row = conn.execute(q["by_name"], ("Di",)).fetchone()
print(row["name"], row["salary"], row.keys())   # Di 4500 ['id', 'name', 'dept', 'salary']
print(dict(row))                                # {'id': 4, 'name': 'Di', 'dept': 'Ops', 'salary': 4500}
conn.row_factory = None

# 9. SQL INJECTION: why you must use parameters
evil = "x' OR '1'='1"
unsafe = "SELECT name FROM employees WHERE name = '" + evil + "'"       # NEVER do this
print(len(conn.execute(unsafe).fetchall()), len(conn.execute(q["by_name"], (evil,)).fetchall()))
# 6 0       the unsafe query returned EVERY row

# 10. Look at the structure
print(conn.execute(q["list_tables"]).fetchall())                        # [('departments',), ('employees',)]
print([r[1] for r in conn.execute(q["columns"])])                       # ['id', 'name', 'dept', 'salary']
conn.close()

# 11. A database FILE keeps its data between runs
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "demo.db"
    db = sqlite3.connect(path)
    db.executescript(schema_sql)
    db.executescript(seed_sql)
    with db:
        db.execute(q["insert_employee"], ("Ed", "Ops", 3000))
    db.close()

    again = sqlite3.connect(path)               # a new connection, later
    print(again.execute(q["count"]).fetchone()[0])                      # 5
    again.close()

# OTHER DATABASES use the same pattern (only the driver and the placeholder differ):
#   PostgreSQL  psycopg ("%s" placeholders)        MySQL  mysql-connector-python
#   Big projects often use SQLAlchemy (an ORM) on top of these drivers.
# RULES: parameters always, commit what you want to keep, close the connection,
#        keep SQL in .sql files or one module, never store passwords in the code.