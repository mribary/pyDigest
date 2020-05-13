"""
Code written by Carlos Fonseca
https://gist.github.com/carlosefonseca/8334277

A bash script to export all tables from an SQLite database
to TSV files in a directory named after the input database.

The directory name is the base name of the database (the last
dot and everything after it is discarded) with -tables
appended to it.

The directory is created if it doesn'talready exist.
Existing files named as tables from the db plus the extension .tab
are overwritten. Other files wont be touched.
"""

#!/usr/bin/env bash

# obtains all data tables from database
TS=`sqlite3 $1 "SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name not like 'sqlite_%';"`

# exports each table to csv
for T in $TS; do

sqlite3 $1 <<!
.headers on
.mode csv
.output $T.csv
select * from $T;
!

done