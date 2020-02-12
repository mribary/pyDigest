## Documenting steps of data manipulation

The documentation describes the creation of the base dataframe including the text of the Digest in structured machine-ready format. It also describes the creation of supporting structured data related to the text of the Digest, for example, authors of passages, legal themes covered in the Digest's 432 sections, and reconstructed characteristics of passages which aim to explain how the Digest was originally created.

### Creation of the base "Ddf" dataframe
Step numbers in the current documentation correspond with those in "Ddf_flowchart". They document the data manipulation pipeline from the raw text to the relational database of the Digest. Steps are names according to the output they produce.

1. ROMTEXT.txt

*from Amanuensis V4.0 to ROMTEXT.txt*

2. Digest.txt

*some text*

3. Ddf_001.py

*some text*

4. Ddf_v001.csv

*some text*


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
D. 7, 7, 0 R: missing title -> reconstruct from Mommsen's print edition, p. 108.: De operis servorum
D. 14, 2, 0 R: chevron/hat (^) in section title -> update section_ref_pattern
D. 18, 7, 0 R: colon in section title
D. 29, 5, 0 R: colon in section title
D. 30, 0 R: one missing "0" -> "D. 30, 0, 0 R"
D. 33, 9, 0 R: missing full stop at the end of the title -> full stop added
D. 43, 12, 0 R: additional full stop in title -> replace with colon


