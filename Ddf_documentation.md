## Documenting steps of data manipulation

The documentation describes the creation of the base dataframe including the text of the Digest in structured machine-ready format. It also describes the creation of supporting structured data related to the text of the Digest, for example, authors of passages, legal themes covered in the Digest's 432 sections, and reconstructed characteristics of passages which aim to explain how the Digest was originally created.

### Creation of the base "Ddf" dataframe
Documentation follows the order of output files. The title of individual steps include the method and the name of the output file in `[Method] > [outputFile]` format. `[Method]` and `[outputFile]` correspond with elements in `Ddf_flowchart`. These steps document the data manipulation pipeline from the raw text of the Digest to its relational database.

1. Manual editing > ROMTEXT.txt

Raw text is copied from the graphical interface of the [Amanuensis V4.0](http://www.riedlberger.de/08amanuensis.html) software developed by Peter Riedlberger and Gunther Rosenbaum. Amanuensis incorporates the ROMTEXT database created by the University of Linz under the supervision of Josef Menner.[<sup id="inline1">1</sup>](#fn1)

![Amanuensis screenshot](./images/amanuensis_v04.jpg)

The entire text is selected in the Amanuensis window which was then copied onto the clipboard. The raw text file is used to create `ROMTEXT.txt`.

2. Manual editing > Digest.txt

ROMTEXT.txt was opened in the vim text editor for manual editing. The final line of the Digest (which constitues about 49% of ROMTEXT.txt) was identified with a search command in vim. Subsequently, text which does not belong to the Digest was selected in vim's visual mode and got deleted. The new file containing the text of the Digest only was renamed and saved.

3. Ddf_001.py > Ddf_v001.csv

Python scripts are include in-line comments to help following the steps. `Ddf_001.py` takes `Digest.txt` as input and splits the raw text into a list of lines. The copyright notice (2 lines), the Digest's introductory notice (2 lines), and the erroneous line including the words `LIBER SEPTIMUS` are deleted. 

A set of regular expression patterns are initialised to identify the different types of lines in the Digest text. The three types are section titles (`section_ref_pattern`), reference headings of individual text units (`heading_ref_pattern`) and the text units themselves ('textunit_pattern).

Cleaning and pre-processing are performed by identifying line types with regular expressions in a 1D numpy array created from the list, and by locating lines which are not captured. These so-called _error lines_ point to a possible typographical error in the text, or indicate that the initial regular expressions need to be modified. 

As far as section titles are concerned, manual counting of these titles in the print edition of the Digest suggests that there should be a total of 432. An anomalous section title imported from ROMTEXT (1) may include an accidental line break which breaks the section title into two lines, (2) may include a lower-case "r" instead of "R" which marks the beginning of the section. These anomalies are amended inside the script. Nine anomalous section titles are noted for manual editing. 

4. Manual editing > Ddf_v002.csv

The table below summarises the 9 anomalous section titles and the correction made.


| Reference | Anomaly | Correction made |
|:---|:---|:---|
| D. 4, 8, 0 R | colon, accidental line break | remove line break, update section_ref_pattern |
| D. 5, 1, 0 R | colon | update section_ref_pattern |
| D. 7, 7, 0 R | missing title | reconstruct from Mommsen's p. 108.: De operis servorum |
| D. 14, 2, 0 R | chevron/hat (^) in section title | remove chevron indicating alternative reading |
| D. 18, 7, 0 R | colon | see above |
| D. 29, 5, 0 R | colon | see above |
| D. 30, 0 R | one missing "0" | amend to "D. 30, 0, 0 R" |
| D. 33, 9, 0 R | missing full stop at the end of the title | full stop added |
| D. 43, 12, 0 R | additional full stop in title | replace with colon |

5. Ddf_002.py > Ddf_002x.csv

`Ddf_002.py` reads data from the manually corrected `Ddf_v002.csv`. The script creates a 1D numpy array with a reset index from the `csv` file. Updated regular expressions are used to check _error lines_ in the three different types of _section titles_, _reference headings_, and _text units_. The updated `section_ref_pattern` captures all 432 section titles, but there are 50 lines which are not captured by either `heading_ref_pattern` or `textunit_pattern`.

The script creates a pandas dataframe which includes the index and content of _error lines_ in the 1D numpy array. The dataframe is exported as a so-called _error file_ with the trailing "x" notation as `Ddf_v002x.csv` for manual editing.

6. Manual editing > Ddf_v003.csv

Anomalies in the `Ddf_v002.csv` file are manually amended according to _error lines_ noted in `Ddf_v002x.csv`. Corrections are extensively documented in `Ddf_v003x.csv`. Anomalies include accidental line breaks, broken reference headings, inconsistent diacritical marks, verbose notation of gaps in the manuscript. The corrected file is `Ddf_v003.csv`.

In addition to correcting the 50 anomalous lines, manual inspection has identified some characteristics which hinder the successful pattern matching of the three different line types in the Digest. 

The chevron `^` indicates an alternative reading. This sign is retained in text units in the format `^[text]^`. Lone chevrons are closed after manual inspection of Mommsen's print copy to identify which word should be marked. White space between chevrons is removed. Alternative readings marked by the double chevron are retained, but will be ignored during text analytics. 

In one instance in `D. 19, 5, 26, 1`, angular brackets `<>` indicate a suggested reading. The reading is retained and the angular brackets are removed. The notation does not appear elsewhere in the Digest.

The Digest includes some excessively long text units. Mommsen's print addition addresses this issue by splitting up and, in some cases, renumbering the text unit. 

- When the text unit in question stands at the end of a passage, that is, a set of text units originating from the same locus and constituting one quoted text, the number for split text units in the reference heading is incremented. For example, `D. 47, 3, 1, 1` is a quoted passage with only one text unit. In this case, Mommsen's edition splits the long text unit into two, and marks the second as `D. 47, 3, 1, 1^`. In this case, the chevron is removed and the reference heading is amended to `D. 47, 3, 1, 2`.

- When renumbering the split text unit would mess up the consolidated numbering in the section, Mommsen's print addition applies letters such as `D. 4, 3, 9, 4a`. Handling references as strings such as `4a` instead of integers such as `4` would cause unwarranted complications in machine processing. For this reason, text units split by Mommsen and marked with a trailing letter in the reference heading are merged into on long text unit. Mommsen's break is retained inside the text by quoting the reference letter inside chevrons such `^a^`. Therefore, the text units as split by Mommsen remain searchable, but will not affect machine processing of the reference headings. As text withon chevrons will be ignored during text processing (see above), the inserted in-line reference will not affect text analytics.

Where the reference heading was missing some information in ROMTEXT, instances were checked against Mommsen's print edition. Apart from the Digest book, section, passage and text unit numbers, reference headings include information about the source of the quoted text in the following pattern: `[jurist] [book number] [work title]` as in `Ulp. 55 ad ed.` where "Ulp." stands for the jurist Ulpian, "55" for the 55th book in Ulpian's work the title of which is abbreviated as "ad ed." which stands for "as edictum". If one or more value is missing in the `[jurist] [book number] [work title]` pattern, it is replaced in the form of `X. 0 x.`. The format guarantees that `[book number]` will be extracted as an integer, `[jurist]` and `[work title]` as strings.

7. Ddf_003.py > Ddf_v100.csv

`Ddf_003.py` reads data from the manually corrected `Ddf_v003.csv`. The script creates a 1D numpy array with a reset index from the `csv` file. Regular expressions have been updated to capture the three different types of lines: _section titles_, _reference headings_, and _text units_. As reference headings and text units come strictly in pairs, `textunit_pattern` has been dismissed. The check does not return any _error lines_, so the array is ready to be transformed into a structured pandas dataframe.

An empty Python dictionary is initiated with keys serving as column heads of the dataframe. Associated values are loaded systematically into a list.

```python
# Create dictionary with keys as column names
Ddict = {"Section_title":[], "Book_no": [], "Section_no": [], "Passage_no":
    [], "TextUnit_no": [], "TextUnit_ref": [], "TextUnit": []}
```

A set of regular expressions are defined to extract data from strings in the _section title_ and _reference heading_ lines. Please note that reference headings in Books 30-32 have only three levels, that is, they only include book, section and passage number, but no text unit number. For this reason, an alternative `heading3032_pattern` is defined for capturing reference headings in Books 30-32. An alterntive `ref_alt_pattern` extracts information in these cases. All other books are handled with `heading_pattern` and `ref_pattern`.

Data extracted from _section title_ and _reference heading_ lines are loaded into the Python dictionary by a nested loop which runs processes items of the 1D numpy array one by one. An empty `index_list_error` is initiated to collect the indices of any lines in the 1D numpy array which is not sorted by the loop. The fact that no item is added to the `index_list_error` suggests that all lines are successfully captured and sorted.

The Python dictionary is transformed into a pandas dataframe and exported as **`Ddf_v100.csv`**. This is the master file, the core of the future Digest database. It has 21055 rows corresponding to the number of text units in the Digest.

### Creation of the "BKO" dataframe


1. *list_item2* in italics
2. **list_item1** in bold
3. ***list_item3*** in bold italics
4. ~~ist_item4~~ struck through

### Unordered list of hyperlinks

- Include a link by passing [linked text with URL](https://swcarpentry.github.io/python-novice-gapminder/setup/).
- Include a link by passing [linked text pointing an internal header](#list-of-string-formatting).

Have a block of code:
```python # code_language
print('Hi') # some code
```

Or have `some code` in line

Have a block of quote:
> "Romeo, Romeo, wherefore art thou Romeo?"
> (block quote in one paragraph)

Insert an image by ![image_of_dog](link)


Amanuensis from riedlberger.de/amanuenis
copy all from Amanuenis window -> ROMTEXT.txt
create a copy of ROMTEXT.txt -> Digest.txt
open Digest.txt with vim and search for the last unit of the Digest ("/D. 50, 17, 211")
note line number (^g) just below the last line of Digest #64198 out of total of 129900 lines at 49% of the entire file
enter visual mode in vim and select all lines below the end of the Digest and delete: vGd -> Digest.txt

Manual editing of 9 anomalous section titles in Ddf_v001.csv
D. 4, 8, 0 R: colon in section title, section title with accidental line break -> remove line break
D. 5, 1, 0 R: colon in section title -> update section_ref_pattern
D. 7, 7, 0 R: missing title -> reconstruct from Mommsen's pryint edition, p. 108.: De operis servorum
D. 14, 2, 0 R: chevron/hat (^) in section title -> update section_ref_pattern
D. 18, 7, 0 R: colon in section title
D. 29, 5, 0 R: colon in section title
D. 30, 0 R: one missing "0" -> "D. 30, 0, 0 R"
D. 33, 9, 0 R: missing full stop at the end of the title -> full stop added
D. 43, 12, 0 R: additional full stop in title -> replace with colon

### Footnotes

[<sup id="fn1">1</sup>](#inline1) Georg Klingenberg, Die ROMTEXT-Datenbank, Informatica e diritto 4 (1995): 223-232.
