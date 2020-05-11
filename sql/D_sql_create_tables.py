import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r'/home/mribary/Dropbox/pyDigest/sql/digest_skeleton.db'

    sql_create_jurist_table = """ \
        create table if not exists jurist (
            -- id of the jurist running from 0 to 36
            id tinyint primary key,
            -- name of the jurist
            name varchar(64) not null,
            -- estimated year of birth (BCE dates as negative)
            birth tinyint not null,
            -- estimated year when the jurist was most active, used for dating
            date tinyint not null,
            -- estimated year of death
            death tinyint not null,
            -- note made when estimating dates
            note text,
            -- reference in Berger's Roman law dictionary and Paulys Realenziklopädie
            reference text
            );
        """
    
    sql_create_work_table = """
        create table if not exists work (
            -- id of the (multi-volume) work
            id smallint primary key,
            -- id of the jurist athoring the work (see table "jurist")
            jurist_id tinyint,
            -- title of the (multi-volume) work
            title varchar(64),
            -- shorthand reference of the work
            ref varchar(64),
            foreign key (jurist_id) references jurist (id)
            );
        """

    sql_create_book_table = """
        create table if not exists book (
            -- id of the book from which the a _Digest_ text unit is excerpted
            id smallint primary key,
            -- id of the work (with potentially multiple books) to which the book belongs (see table "work")
            work_id smallint not null,
            -- number of the book in a multi-volume work 
            book_no tinyint,
            -- shorthand reference of the book
            ref varchar(64),
            foreign key (work_id) references work (id)
            );
        """
    
    sql_create_section_table = """
        create table if not exists section (
            -- id of the section running from 0 to 431
            id smallint primary key,
            -- title of the section
            title text,
            -- id of the text unit (see table "text") where the section starts
            start_of_section smallint
            );
        """

    sql_create_bko_table = """
        create table bko (
            -- id of the reference in the expanded Bluhme-Krüger Ordo
            id smallint primary key,
            -- id of the jurist auhtoring the work (see table "jurist")
            jurist_id tinyint,
            -- shorthand reference of the work or part of work
            ref varchar(64),
            -- letter reference of one of three masses ("S" - Sabinian, "P" - Papinian, "E" - edictal)
            mass char(1),
            -- number of the reference in the original Bluhme-Krüger Ordo published in Mommsen's print edition of the _Digest_ 
            bko_no smallint,
            -- number of the reference in the revised Bluhme-Krüger Ordo published in Honoré's 2006 article
            bko_rev_no smallint,
            -- type of the group in Honoré's second-tier classification of juristic works
            group_type varchar(10),
            -- number of the group in Honoré's second-tier classification of juristic works
            group_no tinyint,
            -- name of the group in Honoré's second-tier classification of juristic works
            group_name varchar(64),
            -- title of the juristic work
            title varchar(64),
            -- number of books within the work
            number_of_books tinyint,
            -- note made when creating the BKO table
            note text,
            foreign key (jurist_id) references jurist (id)
            );
        """

    sql_create_text_table = """
        create table text (
            -- primary key of text units running from 0 to 21054	
            id smallint primary key,
            -- text of text units in the _Digest_
            text text not null,
            -- id of the section where the text unit belongs
            section_id smallint,
            -- id of the jurist authoring the text unit (see table "jurist")
            jurist_id tinyint,
            -- four-level numbering of text units in the Digest
            -- #1 level: Book (a total of 50)
            book_no tinyint,
            -- #2 level: Section (with a title, see table "section")
            section_no tinyint,
            -- #3 level: Passage (corresponding to a jurist-work-book reference)
            passage_no tinyint,
            -- #4 level: TextUnit (longer passages split into smaller units)
            textunit_no smallint,
            -- id of the reference in the Blhume-Krüger Ordo (see table "bko")
            bko_id smallint,
            -- id of the juristic book where the text unit belongs (see table "book")
            book_id smallint,
            foreign key (section_id) references section (id),
            foreign key (jurist_id) references jurist (id),
            foreign key (bko_id) references bko (id),
            foreign key (book_id) references book (id)
            );
        """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create jurist table
        create_table(conn, sql_create_jurist_table)
        # create work table
        create_table(conn, sql_create_work_table)
        # create book table
        create_table(conn, sql_create_book_table)
        # create section table
        create_table(conn, sql_create_section_table)
        # create bko table
        create_table(conn, sql_create_bko_table)
        # create text table
        create_table(conn, sql_create_text_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()