## "Ddf" - Core _Digest_ dataframes

The documentation describes the creation of the core dataframes of the `pyDigest` project. It documents the data manipulation steps leading to the core `Ddf` ("_Digest_ daraframe") which includes the text of the _Digest_ in structured machine-ready format. It also describes the creation of supporting structured data related to the text of the _Digest_, for example, authors of passages, legal themes covered in the Digest's 432 sections, and reconstructed characteristics of passages which aim to explain how the _Digest_ was originally created. These dataframes are used to create [the _Digest_'s relational database](link).

### 1. Creation of the base dataframes

The dcumentation follows the order of output files stored in the prject's `dump` folder. The title of individual steps include the method and the name of the output file in the format of `[Method] > [outputFile]`. The `[Method]` is either (1) manual or (2) executed in Pyhton files which are stored in the `script` folder. The `[Method]` and `[outputFile]` correspond with elements in `Ddf_flowchart`. These steps document the data manipulation pipeline from the raw text of the _Digest_ to its [relational database](link).

![Ddf_flowchart](https://raw.githubusercontent.com/mribary/pyDigest/master/images/Ddf_flowchart.graphml)

1. Manual editing > ROMTEXT.txt

Raw text is copied from the graphical interface of the [Amanuensis V4.0](http://www.riedlberger.de/08amanuensis.html) software developed by Peter Riedlberger and Günther Rosenbaum. Amanuensis incorporates the ROMTEXT database created by the University of Linz under the supervision of Josef Menner.[<sup id="inline1">1</sup>](#fn1)

![Amanuensis screenshot](https://raw.githubusercontent.com/mribary/pyDigest/master/images/amanuensis_v04.jpg)

The entire text is selected in the Amanuensis window which was then copied onto the clipboard. The raw text file is used to create `ROMTEXT.txt`.

2. Manual editing > Digest.txt

`ROMTEXT.txt` was opened in the vim text editor for manual editing. The final line of the _Digest_ (which constitues about 49% of `ROMTEXT.txt`) was identified with a search command in vim. Subsequently, text which does not belong to the Digest was selected in vim's visual mode and got deleted. The new file `Digest.txt` containing the text of the _Digest_ only was renamed and saved.

3. Ddf_001.py > Ddf_v001.csv

Python scripts include in-line comments to document the steps. `Ddf_001.py` takes `Digest.txt` as input and splits the raw text into a list of lines. The copyright notice (2 lines), the _Digest_'s introductory notice (2 lines), and the erroneous line including the words `LIBER SEPTIMUS` are deleted. 

A set of regular expression patterns are initialized to identify the different types of lines in the _Digest_ text. The three types are section titles (`section_ref_pattern`), reference headings of individual text units (`heading_ref_pattern`) and the text units themselves (`textunit_pattern`).

Cleaning and pre-processing are performed by identifying line types with regular expressions in a one-dimensional (1D) numpy array created from the list, and by locating lines which are not captured. These so-called _error lines_ point to a possible typographical error in the text, or indicate that the initial regular expressions need to be modified. 

As far as section titles are concerned, manual counting of these titles in the print edition of the _Digest_ confirmns that there should be a total of 432. An anomalous section title imported from ROMTEXT (1) may include an accidental line break which breaks the section title into two lines, (2) may include a lower-case "r" instead of "R" which marks the beginning of the section. These anomalies are amended inside the script. Nine anomalous section titles are noted for manual editing. 

4. Manual editing > Ddf_v002.csv

The table below summarises the 9 anomalous section titles and the corrections made. Manual editing was carried out by consulting the print edition of the _Digest_ published by Theodor Mommsen and Paul Krüger in 1889.[<sup id="inline2">2</sup>](#fn2)


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

The script creates a pandas dataframe which includes the index and content of _error lines_ in the 1D numpy array. The dataframe is exported as an _error file_ with the trailing "x" notation as `Ddf_v002x.csv` for manual editing.

6. Manual editing > Ddf_v003.csv

Anomalies in the `Ddf_v002.csv` file are manually amended according to _error lines_ noted in `Ddf_v002x.csv`. Corrections are extensively documented in `Ddf_v003x.csv`. Anomalies include accidental line breaks, broken reference headings, inconsistent diacritical marks, verbose notation of gaps in the manuscript. The corrected file is `Ddf_v003.csv`.

In addition to correcting the 50 anomalous lines, manual inspection has identified some characteristics which hinder the successful pattern matching of the three different line types in the _Digest_. 

The chevron `^` indicates an alternative reading. This sign is retained in text units in the format `^[text]^`. Lone chevrons are closed after manual inspection of Mommsen's print copy to identify which word should be marked. White space between chevrons is removed. Alternative readings marked by the double chevron are retained, but will be ignored during text analytics. 

In one instance in `D. 19, 5, 26, 1`, angular brackets `<>` indicate a suggested reading. The reading is retained and the angular brackets are removed. The notation does not appear elsewhere in the _Digest_.

The _Digest_ includes some excessively long text units. Mommsen's print addition addresses this issue by splitting them up and, in some cases, renumbering the text unit. 

- When the text unit in question stands at the end of a passage, that is, a set of text units originating from the same locus and constituting one quoted text, the number for split text units in the reference heading is incremented. For example, `D. 47, 3, 1, 1` is a quoted passage with only one text unit. In this case, Mommsen's edition splits the long text unit into two, and marks the second as `D. 47, 3, 1, 1^`. In this case, the chevron is removed and the reference heading is amended to `D. 47, 3, 1, 2`.

- When renumbering the split text unit would mess up the consolidated numbering in the section, Mommsen's print edition applies letters such as `D. 4, 3, 9, 4a`. Handling references as strings such as `4a` instead of integers such as `4` would cause unwarranted complications in machine processing. For this reason, text units split by Mommsen and marked with a trailing letter in the reference heading are merged into one long text unit. Mommsen's break is retained inside the text by quoting the reference letter inside chevrons such as `^a^`. Therefore, the text units as split by Mommsen remain identifiable and recoverable, but will not affect machine processing of the reference headings. As text within chevrons will be ignored during text processing (see above), the inserted in-line reference will not affect text analysis.

- Where the reference heading was missing some information in ROMTEXT, instances were checked against Mommsen's print edition. Apart from the _Digest_ book, section, passage and text unit numbers, reference headings include information about the source of the quoted text in the following pattern: `[jurist] [book number] [work title]` as in `Ulp. 55 ad ed.` where "Ulp." stands for the jurist Ulpian, "55" for the 55th book in Ulpian's work the title of which is abbreviated as "ad ed." which stands for "as edictum". If one or more value is missing in the `[jurist] [book number] [work title]` pattern, it is replaced in the form of `X. 0 x.`. The format guarantees that `[book number]` will be extracted as an integer, `[jurist]` and `[work title]` as strings.

7. Ddf_003.py > Ddf_v100.csv

`Ddf_003.py` reads data from the manually corrected `Ddf_v003.csv`. The script creates a 1D numpy array with a reset index from the `csv` file. Regular expressions have been updated to capture the three different types of lines: _section titles_, _reference headings_, and _text units_. As reference headings and text units come strictly in pairs, `textunit_pattern` has been dismissed. The check does not return any _error lines_, so the array is ready to be transformed into a structured pandas dataframe.

An empty Python dictionary is created with keys serving as column heads of the dataframe. Associated values are loaded systematically into a list.

```python
# Create dictionary with keys as column names
Ddict = {"Section_title":[], "Book_no": [], "Section_no": [], "Passage_no":
    [], "TextUnit_no": [], "TextUnit_ref": [], "TextUnit": []}
```

A set of regular expressions are defined to extract data from strings in the _section title_ and _reference heading_ lines. Reference headings have generally four levels, that is, (1) `Book_no`, (2), `Section_no`, (3) `Passage_no` and (4) `TextUnit_no`. Books 30-32 constitute an exception with reference headings with only three levels, that is, they only include book, section and passage number, but no text unit number. For this reason, an alternative `heading3032_pattern` is defined for capturing reference headings in Books 30-32. An alterntive `ref_alt_pattern` extracts information in these cases. Section titles appear as book titles in these three books. All other books are handled with `heading_pattern` and `ref_pattern`.

Data extracted from _section title_ and _reference heading_ lines are loaded into the Python dictionary by a nested loop which processes items of the 1D numpy array one by one. An empty `index_list_error` is initiated to collect the indices of any lines in the 1D numpy array which is not sorted by the loop. The fact that no item is added to the `index_list_error` confirms that all lines are successfully captured and sorted.

The Python dictionary is transformed into a pandas dataframe and exported as **`Ddf_v100.csv`**. This is the first version of the the master `csv` file, the core of the future _Digest_ database. It has 21055 rows corresponding to the number of text units in the _Digest_.

### 2. Creation and linking of the "BKO" dataframe

Friedrich Bluhme's seminal article published in 1820 set out a theory about the compositional history of the _Digest_.[<sup id="inline3">3</sup>](#fn3) Bluhme examined the order of passages in the thematic sections and discovered a pattern. He suggested that Tribonian, who was charged with the editing of the _Digest_ by Byzantine Roman emperor Justinian (525-565 CE), created three committees to review and excerpt juristic works from the history of Roman law. According to Bluhme's theory, passages supplied by the committee responsible for works in the so-called "Sabinian mass" were put in the beginning of thematic sections, passages excerpted from the "edictal mass" by another committee were recorded in the middle, and passages excerpted form the "Papinian mass" by a third committee were recorded at the end. Bluhme numbered the works in the three masses which were revised by Paul Krüger and published in the appendix of Mommsen's print edition of the _Digest_ (pp. 874-878) as the _Ordo librorum iuris veteris in compilandis Digestis observatus_ ("The order of old juristic books observed in the compilation of the _Digest_").

Tony Honoré,[<sup id="inline4">4</sup>](#fn4) Dario Mantovani[<sup id="inline5">5</sup>](#fn5) and other scholars scrutinised the Bluhme-Krüger Ordo (BKO) and amended some errors. Bluhme's theory stands to be true, but unproven. Honoré supplemented the BKO with a second tier by identifying sub-groups within the three masses according to a common genre, author or subject. The current BKO dataframe has been created according to Honoré's revision.

1. Manual editing > BKO_v001.txt > BKO_v002.txt

Honore's revised BKO table is copied from the `pdf` copy of his article published in _Roman Legal Tradition_ in 2006. Headers, footers, footnote numbers and footnotes are removed. Numbering has been found erroneous in three instances. Errors are checked against the BKO published in Mommsen and corrected manually to create `BKO_v002.txt`.

| Error | Correction made |
|:---|:---|
| 69. Paulus 3 ad legem Aeliam Sentiam | number changed to 70 |
| 70. Ulpianus 4 ad legem Aeliam Sentiam | number changed to 71 |
| (xxii) SC Trebellianum group. | changed to: (xxi) SC Tertullianum group. |

2. Ddf_BKO.py > BKO_v001.csv

The script reads `BKO_v002.txt` and extracts structured information by a regular expression pattern. An empty Python dictionary is initiated with keys serving as column heads of the BKO dataframe. Associated values are loaded systematically into a list.

```python
# Create an empty python dictionary with keys as column labels
BKO_dict = {'BKO_no':[], 'bis':[], 'Jurist_name':[], 'Number_of_books':[], 'Work_title':[]}
```

The dictionary is transformed into a dataframe which, in turn, is exported as `BKO_v001.csv` for further manual editing.

3. Manual editing > BKO_v002.csv

`BKO_v001.csv` is opened in libreoffice_calc to enter and edit data manually in a graphical environment. The spreadsheet inlcudes the follwing column labels:

| Column label | Description |
|:---|:---|
| BK_Ordo_no | BKO number according to Honore's revision
| Honore_group_name | name of the sub-group of works identified by Honore |
| Honore_group_type | sub-group's type: author ("a"), genre ("g"), subject ("s") or unattached ("u") |
| Honore_group_no | sub-group's number |
| BK_Ordo_no_rev | unrevised BKO number |
| Jurist_name | name of jurist associated with a work |
| Number_of_books | number of books in the work |
| Work_title | title of the work |
| Work_ref | abbreviated reference in the format used in the reference headings of Digest text units |
| BK_mass | work's mass: Sabinian ("S"), edictal ("E") or Papinian ("P")
| Note | any additional information |

In addition to the works listed in the BKO revised and supplemented by Honoré, the spreadsheet includes reference headings of works which the BKO does not include by systamtically examining `Ddf_v100.csv`. Honoré's revised BKO has 275 numbered works, the number of works listed here is 299. Some of these works are defined as parts of a larger multi-book work. For example, Ulpian's commentary on the _Perpetual Edict_ (_ad edictum_) has 81 books of which, acording to the BKO, books 26-51 constitute one item in the Sabinian mass. This item's abbreviated title is "Ulp. 26-51 ad ed." which follows the format of reference headings in ROMTEXT. Long strokes ("–") are replaced with short ones ("-") throughout the dataframe.

4. Ddf_004.py > Ddf_v101.csv

The Python script in `Ddf_004.py` reads `Ddf_v100.csv` and manipulates its data to create a link between the `Ddf` and the `BKO` dataframes.

The script removes the book number from items stored in the `TextUnit_ref` column, so that "Ulp. 1 inst." becomes "Ulp. inst." where "Ulp." stands for the jurist called Ulpian and "inst." for the title of his work "institutiones". The manipulated series is inserted into the `Ddf` dataframe with the label `Work`.

While in most cases work is equivalent with the item stored and listed in the `BKO` dataframe, split multi-volume works are exceptions. For example, a text unit quoted from the 31st book of Ulpian's commentary on the _Perpetual Edict_ ("Ulp. 31 ad ed." in the `TextUnit_ref` column) provides the work reference "Ulp. ad ed." in the `Work` column. However, the `BKO` considers that the 81 books of Ulpian's commentary were not processed as one item, but rather in parts such as the one constituted by books 26-51. Therefore, the `BKO` reference is not "Ulp. ad ed." as shown in the `Work` column, but "Ulp. 26-51 ad ed."

For this reason, affected multi-volume works in the `Work` column is manipulated further to create a column `BKO_key` where items correspond to the `BKO` references stored in the `Work_ref` column in the `BKO` dataframe. The following items in `Work` are split and manipulated with regular expressions in the Python script.

1. "Paul ad ed."
2. "Paul sent."
3. "Gaius. ad ed. provinc."
4. "Ulp. ad ed."
5. "Paul ad Plaut."
6. "Marcian. reg."
7. "Paul. resp."
8. "Scaev. resp."
9. "Ulp. fideicomm."
10. "Valens. fideicomm."
11. "Maec. fideicomm."
12. "Hermog. iuris epit."
13. "Tryph. disp."
14. "Proc. epist."

It should be noted that in three instances, `BKO` splits the work in the middle of a book which means it cannot be decided to which `BKO` reference the particular text unit belongs on the evidence of `TextUnit_ref` itself which only provides the book number.

**Paul. 1 sent. - 80 instances**: 
The text unit belongs either to "Paul. 1 sent." standing for the beginning of the 1st book of Paul's _sententiae_, or to "Paul 1-2 sent." standing for the end of the 1st book together with the 2nd book. These text units are stored with "Paul. 1 sent." as their `BKO_key` and require manual examination.

**Paul. 48 ad ed. - 36 instances**: 
The text unit belongs either to "Paul. 28-48 ad ed." standing for books 28-47 together with the beginning of book 48 in Paul's commentary on the _Perpetual Edict_, or to "Paul 48-49 ad ed." standing for the end of book 48 book together with book 49. These text units are stored with "Paul. 48 ad ed." as their `BKO_key` and require manual examination.
	
**Ulp. 55 ad ed. - 49 instances**: 
The text unit belongs either to "Ulp. 54-55 ad ed." standing for book 54 together with the beginning of book 55 in Ulpian's commentary on the _Perpetual Edict_, or to "Ulp. 55 ad ed." standing for the rest of book 55. These text units are stored with "Ulp. 55 ad ed." as their `BKO_key` and require manual examination.

5. Manual editing > Ddf_v102.csv

References in the `TextUnit_ref`, `Work` and `BKO_key` columns of `Ddf_v101.csv` associated with "Valens" are modified so that a full stop is added after the name "Valens." This ensures consistency and good data capture in the next processing phase. The file `Ddf_v102.csv` is saved in the `dump` folder. Long strokes ("–") are replaced with short ones ("-") throughout the dataframe.

6. Ddf_BKO_check_1.py > BKO_errors_1.txt

The script checks the consistency of reference formats in the `Ddf` and `BKO` dataframes. It reads the `BKO_key` column from `Ddf_v102.csv` and the `Work_ref` column from `BKO_v002.csv` and strips trailing whitespaces. There are 403 unique entries in the `BKO_key` column of `Ddf` which are checked against the items of the `Work_ref` column in `BKO`. Matching entries (251) follow the predefined format. The list of non-matching entries (152) are written into a txt file for manual investigation and editing. Such entries may need to be amended in `Ddf` or a matching entry needs to be added to the `BKO` dataframe. There needs to be full one-to-one correspondence between `Ddf` and `BKO`.

7. Manual editing > Ddf_v103.csv and BKO_v003.csv

`Ddf` dataframe is inspected according to the list of 152 anomalous entries in `BKO_errors_1.txt`. Typographical errors and inconsistent entries are manually corrected in `Ddf` while entries in the `BKO` are updated when necessary.

8. Ddf_BKO_check_2.py > BKO_errors_2.txt

The same script is run on the manually corrected `Ddf_v103.csv` and `BKO_v003.csv` files. Matching entries (285) follow the predefined format and found in `BKO`. The list of non-matching entries (24) are elements in the `BKO_key` columns of `Ddf` which do not appear in the `BKO`. These anomalous entries are written to `BKO_errors_2.txt` and used for a second round of manual editing.

9. Manual editing > Ddf_v104.csv and BKO_v004.csv

There are three inherently ambiguous references for which separate `BKO` entries have been created:

| BKO entry name | Ambiguity | Notes |
| :--- | :--- | :--- |
| Paul. ?1 sent. | the text unit either belongs to “Paul. 1 sent.” (BKO 205) or “Paul. 1-2 sent.” (BKO 207) | alternatives belong to the same BKO mass (edictal) and Honore group (sententiae-iuris epitomae, 16); this information is retained | 
| Ulp. ?55 ad ed. | the text unit either belongs to “Ulp. 54-55 ad ed.” (BKO 112) or “Ulp. 55 ad ed.” (BKO 116) | alternatives belong to the same BKO mass (edictal) and Honore group (transferred edictal commentaries, 28); this information is retained | 
| Paul. ?48 ad ed. | the text unit either belongs to “Paul. 28-48 ad ed. (BKO 5) or “Paul. 48-49 ad ed.” (BKO 121) | alternatives belong to different BKO masses (Sabinian and edictal) and Honore groups, this information is removed |

For now, this ambiguity of the Bluhme-Krüger Ordo is left unsolved. 

10. Ddf_BKO_check_3.py

The same script is run a third time on the manually corrected `Ddf_v104.csv` and `BKO_v004.csv` files. Matching entries (293) follow the predefined format and they are found in `BKO`. There are no non-matching entries which means that all elements in the `BKO_key` columns of `Ddf` correspond to an item in the `Work_ref` column of `BKO`. 

Some `BKO` items do not appear in `Ddf`. Two of these references ("Ulp. de off. consularium." and "Gai. l. s. ad ed. pu.") might have been absorbed by mistake by another work with a very similar title. "Ulp. 55 ad ed." and "Paul. 1 sent." are inherently ambiguous titles which may belong to one of two alternatives. There are two missing values in the `Work_ref` column of `BKO` at (1) Callistratus' de edicti monitori which appear twice in the Ordo by Bluhme and Kruger, and hence one is dropped here (BKO 99), and (2) book 19 of Gaius' ad edictum provinciale (BKO 122) which overlaps with "Gai. 1-8, 19 ad ed. provinc." (BKO 98).

The manually corrected `Ddf_v104.csv` and `BKO_v004.csv` files are free from errors and any remaining ambiguous entries have been documented. These files are copied into the output folder.

11. Ddf_005.py > Ddf_v106.csv

Manual inspection has revealed that Greek script had been lost during manual editing in step 7 above. The Python file recovers the `TextUnit` column from `Ddf_v102.csv` and inserts them into `Ddf_v105.csv`. The output `csv` file is streamlined to keep the index, the four-level _Digest_ reference and the text only. These columns will be used to create the SQL database.

12. Manual editing > BKO_v006.csv

Based on `Work_ref`, a verbose `title` is added to the `BKO` dataframe which includes the title of the work in an unabbreviated format and drops the book numbers where the work in the `BKO` dataframe is split. Where the verbose title could not be verified by checking against Mommsen's print edition, a `?` mark is added to the title to indicate that the data may need to be updated at a later point.

### 3. Additional dataframes

1. Sections dataframes

Ddf_sections.py > Ddf_sections.csv, Ddf_Section_IDs.csv

The script initiates a dataframe `df` with the `Section_title` and `Book_no` columns from `Ddf_v104.csv`. It counts the number of thematic sections (432) with 0 indexing and adds a section_id to each of the 21055 lines associated with a _Digest_ text unit. All items in the anomalous books 30-32 of the _Digest_ bear the same section title. Here a new thematic section is forced to start at the beginning of each book even though the section title stays the same. The `section_id` is inserted into the `df` as a new column while column `Book_no` is dropped. The dataframe is exported as `Ddf_sections_v001.csv`.

An additional dataframe including section_IDs with their corresponding section titles is created and exported as `Ddf_Section_IDs_v001.csv`.

2. ID dataframes

`Ddf_IDs_001.py > Ddf_IDs_001.csv, Ddf_BKO_IDs_001.csv, Ddf_Work_IDs_001.csv, Ddf_Book_IDs_001.csv`

The script initiates a dataframe `df` with the `BKO_key`, `Work` and `TextUnit_ref` columns from `Ddf_v104.csv`. It creates separate dataframes for unique `BKO_key` (294), `Work` (251), and `TextUnit_ref` values (1352) where values are sorted alphabetically and associated with a unique ID. These dataframes are exported as `Ddf_BKO_IDs_v001.csv`, `Ddf_Work_IDs_v001.csv` and `Ddf_Book_IDs_v001.csv`.

The script links the reference IDs above with the 21055 text units of the Digest by merging dataframes on unique values. The dataframe is streamlined and arranged for comfortable reading before it is exported as `Ddf_IDs_001.csv`.

3. Jurists dataframes

> 3.1. `Ddf_jurists.py > Jurists_v001.csv`

The script initiates a dataframe `df` with the `Jurist_name` column from `BKO_v004.csv`. It strips whitespace, orders the list of unique values, associates items with unique IDs and outputs the `Jurists_v001.csv` file to be enriched with data manually.

> 3.2. `Manual editing: Jurists_v001.csv > Jurists_v002.csv, Ddf_v105.csv`

Jurists are associated with a date range of their lifetime according to information available in Adolf Berger's _Dictionary of Roman law_[<sup id="inline6">6</sup>](#fn6) consulted in conjunction with _Paulys Realencyclopädie der classischen Altertumswissenschaft_[<sup id="inline7">7</sup>](#fn7). The manually edited `Jurists_v002.csv` includes a `Note` which explains how the date range is estimated and a column with `Reference` information to _Berger_ and the _RE_. `Start_date` corresponds to the (estimated) birth of the jurist, `Mid_date` to his (estimated) most active period (_floruit_) at the age of 40, and `End_date` to his (estimated) death at the age of 60. Where exact dates are available for any of the three dates from _Berger_ and the _RE_, it is entered into the appropriate column instead of the estimate.

For those jurists who are dated only by rough estimates in the _RE_ or _Berger_, the differnce between the start and end date of his life is capped at **60 years**. This is on the assumption that, apart from extreme cases, a well-educated wealthy Roman could expect no more than 60 years to live. The figure is derived from the life expectancy model created by Bruce Frier on the basis of a Roman legal rule which calculates lifetime support due to a legatee from the inheritance.[<sup id="inline8">8</sup>](#fn8) The rule was preserved by the 3rd century CE jurist Aemilius Macer (D.36.2.68.0) who cites his predecessor Ulpian on the matter. Ulpian contrasts his own (more generous) calculation with a customary lifetable in which no support is provided for a legatee beyond the age of 60. This upper limit in Ulpian's customary lifetable is the justification for capping the age of a well-educated wealthy Roman at 60. Despite Walter Scheidel's call for caution regarding variations in lifetable models according to space, time and cultural practice,[<sup id="inline9">9</sup>](#fn9) the figure derived from Frier remains justified. When _Berger_ and the _RE_ only provide one estimate date, it is assumed (1) that it refers to the most active period of the jurist's life (his _floruit_) and (2) that this most active period is at the age of 40.

Minor typos and alternative versions of headings are corrected in Ddf which is updated manually in `Ddf_v105.csv`. The consistency of the `Ddf` and `BKO` dataframes are checked in `Ddf_BKO_check_4.py`.

> 3.3. `Ddf_IDs_002.py > Ddf_IDs_002.csv, Ddf_BKO_IDs_002.csv, Ddf_Work_IDs_002.csv, Ddf_Book_IDs_002.csv`

ID dataframes are updated according to manually edited files in the previous step.

> 3.4. `Ddf_IDs_003.py > BKO_v005.csv, Ddf_IDs_003.csv, Ddf_BKO_IDs_003.csv, Ddf_Work_IDs_003.csv, Ddf_Book_IDs_003.csv`

`Jurist_id` and `Mid_date` columns are inserted into the `BKO`, `BKO_IDs` and `Ddf_IDs` dataframes by merging. The Work_IDs and Book_IDs dataframes are updated by removing duplicate values in the Book_id and Work_id columns in the new Ddf_Ids dataframe. All text units in Ddf, all elements in BKO, and all elements in the ID dataframes are now associated with a date which is stipulated to be the most active period of the corresponding jurist.

4. BKO dataframe alignment

`Ddf_IDs_004.py > BKO_v007.csv`

A new column `BKO_id` is added to the `BKO` dataframe which aligns `Work_ref` in the `BKO` daraframe with `BKO_label` in the `Ddf_BKO_IDs` dataframe. `None` is entered where `Work_ref` cannot be mathced with a `BKO_label`.

### Footnotes

[<sup id="fn1">1</sup>](#inline1) Georg Klingenberg, "Die ROMTEXT-Datenbank," _Informatica e diritto_ 4 (1995): 223-232.

[<sup id="fn2">2</sup>](#inline2) Theodor Mommsen & Paul Kruger, _Corpus Iuris Civlis. Editio stereotypa quinta. Vol 1: Institutiones. Digesta._ Berlin: Weidmann, 1889.

[<sup id="fn3">3</sup>](#inline3) Friedrich Bluhme, "Die Ordnung der Fragmente in den Pandectentiteln: Ein Beitrag der Entstehungsgeschichte der Pandecten," _Zeitschrift der Savigny-Stiftung für Rechtsgeschichte_ 4 (1820): 257-472.

[<sup id="fn4">4</sup>](#inline4) Tony Honore, "Justinian's Digest: The distribution of authors and works to the three committees," _Roman Legal Tradition_ 3 (2006): 1-47.

[<sup id="fn5">5</sup>](#inline5) Dario Mantovani, _Digesto e masse bluhmiane_. Milan: Giuffré, 1987.

[<sup id="fn6">6</sup>](#inline6) Adolf Berger, "Encyclopedic dictionary of Roman law," _Transactions of the American Philosophical Society_ 43 (1953): 333-809.

[<sup id="fn7">7</sup>](#inline7) Georg Wissowa, Wilhelm Kroll, Karl Mittelhaus, Konrat Ziegler and Hans Gärtner, eds.,_Paulys Realencyclopädie der classischen Altertumswissenschaft: Neue Bearbeitung_. Stuttgart: Metzler, 1893-1980.

[<sup id="fn8">8</sup>](#inline8) Bruce Frier, "Roman life expectancy: Ulpian's evidence," _Harvard Studies in Classical Philology_, 86 (1982): 213-251.

[<sup id="fn9">9</sup>](#inline9) Walter Scheidel, "Roman age structure: Evidence and models," _The Journal of Roman Studies_ 91 (2001): 1-26.