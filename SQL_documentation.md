## "SQL" - Relational database

SQLite with sqlite3 command line and sqlite3 Python package

### 1. Create database: digest.db

1. D_sql_create_db.py > digest.db

The Python script imports `sqlite3` and its `Error` function and creates an empty database stored in the `sql` folder of the repository.

2. Manual schema > D_sql.graphml

The core structure of the `digest` database is drafted in the yEd graph editor and stored in the `images` folder of the repository. It includes the name and datatype of the fields in the various tables and notes their primary (PK) and foreign keys (FK). The graph's edges uses the arrow symbols to indicate one-and-only-one to many-or-one relations between the tables.

![D_sql_graph](https://raw.githubusercontent.com/mribary/pyDigest/master/images/D_sql.png)

3. D_sql_create_tables.py > digest.db

The Python script imports `sqlite3` and its `Error` function. It defines a `Connection` object for accessing `digest.db` and a `cursor` object to create tables in it. The file's `main` function defines six tables with their primary keys, fields and datatypes as well as their foreign key restrictions which create connections between tables. The structure follows the structure drafted in the `D_sql` graph above.

Running the file creates the tables which are checked by looking at `digest.db` in the command line by `sqlite3` with `> .tables`. Fields and datatypes are checked by the following sequence of commands: `> .header on > .mode column > pragma table_info('text');`.