# Import packages
import sqlite3
from sqlite3 import Error
import pandas as pd 
import numpy as np
import re

# Load dataframes
path_jurists = '/home/mribary/Dropbox/pyDigest/dump/Jurists_v002.csv'
jurists = pd.read_csv(path_jurists, index_col=0)
path_ids = '/home/mribary/Dropbox/pyDigest/dump/Ddf_IDs_v003.csv'
ids = pd.read_csv(path_ids, index_col=0)
path_BKO = '/home/mribary/Dropbox/pyDigest/dump/BKO_v007.csv'
BKO = pd.read_csv(path_BKO, index_col=0)
path_texts = '/home/mribary/Dropbox/pyDigest/dump/Ddf_v106.csv'
texts = pd.read_csv(path_texts, index_col=0)
path_sections = '/home/mribary/Dropbox/pyDigest/dump/Ddf_sections_v001.csv'
sections = pd.read_csv(path_sections, index_col=0)

# Give path for the skeleton database
db_file = '/home/mribary/Dropbox/pyDigest/sql/digest.db'

# Create connection to datbase file
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# Create functions to load data to the tables of the database
def create_jurist(conn, jurist):
    """
    Create a new jurist in the jurist table
    :param conn:
    :param jurist:
    :return: jurist id
    """
    sql = ''' INSERT INTO jurist(id, name, birth, date, death, note, reference)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, jurist)
    return cur.lastrowid

def create_work(conn, work):
    """
    Create a new work in the work table
    :param conn:
    :param work:
    :return: work id
    """
    sql = ''' INSERT INTO work(id, jurist_id, title, ref)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, work)
    return cur.lastrowid

def create_book(conn, book):
    """
    Create a new book in the book table
    :param conn:
    :param book:
    :return: book id
    """
    sql = ''' INSERT INTO book(id, work_id, book_no, ref)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, book)
    return cur.lastrowid

def create_section(conn, section):
    """
    Create a new section in the section table
    :param conn:
    :param section:
    :return: section id
    """
    sql = ''' INSERT INTO section(id, title, start_of_section)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, section)
    return cur.lastrowid

def create_bko(conn, bko):
    """
    Create a new bko reference in the BKO table
    :param conn:
    :param bko:
    :return: bko id
    """
    sql = ''' INSERT INTO bko(id, jurist_id, ref, mass, bko_no, bko_rev_no, group_type, group_no, group_name, title, number_of_books, note)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, bko)
    return cur.lastrowid

def create_text(conn, text):
    """
    Create a new text unti in the text table
    :param conn:
    :param text:
    :return: text id
    """
    sql = ''' INSERT INTO text(id, text, section_id, jurist_id, book_no, section_no, passage_no, textunit_no, bko_id, book_id)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, text)
    return cur.lastrowid

# Create temporary dataframes
work_dict = {'id':[], 'jurist_id':[], 'title':[], 'ref':[]}
for i in set(ids.Work_id.values): 
    work_id = i
    work_jurist_id = ids.Jurist_id[min(ids.index[ids.Work_id == i])]
    work_BKO_id = ids.BKO_id[min(ids.index[ids.Work_id == i])]
    work_title = BKO.title[BKO.BKO_id == work_BKO_id].values[0]
    work_ref = str(ids.Work[min(ids.index[ids.Work_id == i])])
    work_dict['id'].append(work_id)
    work_dict['jurist_id'].append(work_jurist_id)
    work_dict['title'].append(work_title)
    work_dict['ref'].append(work_ref)
work_df = pd.DataFrame(work_dict)

book_dict = {'id':[], 'work_id':[], 'book_no':[], 'ref':[]}
for i in set(ids.Book_id.values):
    book_id = i
    book_work_id = ids.Work_id[min(ids.index[ids.Book_id == i])]
    book_no = re.search('\d+', ids.TextUnit_ref[min(ids.index[ids.Book_id == i])])
    if book_no is not None:
        book_no = int(book_no.group())
    else:
        book_no = 0
    book_ref = str(ids.TextUnit_ref[min(ids.index[ids.Book_id == i])])
    book_dict['id'].append(book_id)
    book_dict['work_id'].append(book_work_id)
    book_dict['book_no'].append(book_no)
    book_dict['ref'].append(book_ref)
book_df = pd.DataFrame(book_dict)

section_dict = {'id':[], 'title':[], 'start_of_section':[]}
for i in set(sections.Section_id.values):
    section_id = i
    section_title = str(sections.Section_title[min(sections.index[sections.Section_id == i])]).lower()
    section_start_of_section = min(sections.index[sections.Section_id == i])
    section_dict['id'].append(section_id)
    section_dict['title'].append(section_title)
    section_dict['start_of_section'].append(section_start_of_section)
section_df = pd.DataFrame(section_dict)

bko_dict = {'id':[], 'jurist_id':[], 'ref':[], 'mass':[], 'bko_no':[], 'bko_rev_no':[], 'group_type':[], 'group_no':[], 'group_name':[], 'title':[], 'number_of_books':[], 'note':[]}
for i in BKO.BKO_id:
    bko_id = int(i)
    bko_jurist_id = int(BKO.Jurist_id[i])
    bko_ref = str(BKO.Work_ref[i])
    bko_mass = str(BKO.BK_mass[i])
    bko_no = BKO.BK_Ordo_no[i]
    if np.isnan(bko_no):
        bko_no = None
    else:
        bko_no = int(bko_no)
    bko_rev_no = BKO.BK_Ordo_no_rev[i]
    if np.isnan(bko_rev_no):
        bko_rev_no = None
    else:
        bko_rev_no = int(bko_rev_no)
    bko_group_type = BKO.Honore_group_type[i]
    if bko_group_type is not None:
        bko_group_type = str(bko_group_type)
    else:
        bko_rev_no = None
    bko_group_no = BKO.Honore_group_no[i]
    if np.isnan(bko_group_no):
        bko_group_no = None 
    else:
        bko_group_no = int(bko_group_no)
    bko_group_name = str(BKO.Honore_group_name[i])
    bko_title = str(BKO.title[i])
    bko_number_of_books = BKO.Number_of_books[i]
    if np.isnan(bko_number_of_books):
        bko_number_of_books = None    
    else:
        bko_number_of_books = int(bko_number_of_books)
    bko_note = BKO.Note_x[i]
    bko_dict['id'].append(bko_id)
    bko_dict['jurist_id'].append(bko_jurist_id)
    bko_dict['ref'].append(bko_ref)
    bko_dict['mass'].append(bko_mass)
    bko_dict['bko_no'].append(bko_no)
    bko_dict['bko_rev_no'].append(bko_rev_no)
    bko_dict['group_type'].append(bko_group_type)
    bko_dict['group_no'].append(bko_group_no)
    bko_dict['group_name'].append(bko_group_name)
    bko_dict['title'].append(bko_title)
    bko_dict['number_of_books'].append(bko_number_of_books)
    bko_dict['note'].append(bko_note)
bko_df = pd.DataFrame(bko_dict)

# Main function to load data to the tables
def main():
    database = r"/home/mribary/Dropbox/pyDigest/sql/digest.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        
        # Populate the jurist table
        for i in set(ids.Jurist_id.values): 
            jurist_id = int(jurists.Jurist_id[i])
            jurist_name = str(jurists.Jurist[i])
            jurist_birth = int(jurists.Start_date[i])
            jurist_date = int(jurists.Mid_date[i])
            jurist_death = int(jurists.End_date[i])
            jurist_note = str(jurists.Note[i])
            jurist_reference = str(jurists.Reference[i])
            jurist = (
                jurist_id,
                jurist_name,
                jurist_birth,
                jurist_date,
                jurist_death,
                jurist_note,
                jurist_reference
                )
            create_jurist(conn, jurist)

        # Populate the work table
        for i in work_df.id: 
            work_id = int(work_df.id[i])
            work_jurist_id = int(work_df.jurist_id[i])
            work_title = str(work_df.title[i])
            work_ref = str(work_df.ref[i])
            work = (
                work_id,
                work_jurist_id,
                work_title,
                work_ref
                )
            create_work(conn, work)

        # Populate the book table
        for i in book_df.id:
            book_id = int(book_df.id[i])
            book_work_id = int(book_df.work_id[i])
            book_no = int(book_df.book_no[i])
            book_ref = str(book_df.ref[i])
            book = (
                book_id,
                book_work_id,
                book_no,
                book_ref
                )
            create_book(conn, book) 

        # Populate the section table
        for i in section_df.id:
            section_id = int(section_df.id[i])
            section_title = str(section_df.title[i])
            section_start_of_section = int(section_df.start_of_section[i])
            section = (
                section_id,
                section_title,
                section_start_of_section
                )
            create_section(conn, section)

        # Populate the BKO table
        for i in bko_df.id:
            bko_id = i
            bko_jurist_id = int(bko_df.jurist_id[i])
            bko_ref = bko_df.ref[i]
            bko_mass = bko_df.mass[i]
            bko_no = bko_df.bko_no[i]
            bko_rev_no = bko_df.bko_rev_no[i]
            bko_group_type = bko_df.group_type[i]
            bko_group_no = bko_df.group_no[i]
            bko_group_name = bko_df.group_name[i]
            bko_title = bko_df.title[i]
            bko_number_of_books = bko_df.number_of_books[i]
            bko_note = bko_df.note[i]
            bko = (
                bko_id,
                bko_jurist_id,
                bko_ref,
                bko_mass,
                bko_no,
                bko_rev_no,
                bko_group_type,
                bko_group_no,
                bko_group_name,
                bko_title,
                bko_number_of_books,
                bko_note
                )
            create_bko(conn, bko)

        # Populate the text table
        for i in texts.index:
            text_id = int(i)
            text_text = str(texts.TextUnit[i])
            text_section_id = int(sections.Section_id[i])
            text_jurist_id = int(ids.Jurist_id[i])
            text_book_no = int(texts.Book_no[i])
            text_section_no = int(texts.Section_no[i])
            text_passage_no = int(texts.Passage_no[i])
            text_textunit_no = int(texts.TextUnit_no[i])
            text_bko_id = int(ids.BKO_id[i])
            text_book_id = int(ids.Book_id[i])
            text = (
                text_id,
                text_text,
                text_section_id,
                text_jurist_id,
                text_book_no,
                text_section_no,
                text_passage_no,
                text_textunit_no,
                text_bko_id,
                text_book_id
                )
            create_text(conn, text)

# Run the program
if __name__ == '__main__':
    main()