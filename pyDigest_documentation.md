## "pyDigest" - General functions

The documentation describes the functions defined and stored in `pyDigest.py`. A copy of the file is stored in the user site directory at `~/.local/lib/python3.7/site-packages`.

After opening a Terminal window, the following bash commands could be used to navigate to the directory and create a copy of `pyDigest.py` which is then called by Python scripts. This is a strictly temporary solution for a privately managed module.

```bash
$ path=`python3 -m site --user-site`
$ cd $path
$ cp [path_for_pyDigest.py] .
```

These functions can be called in other Python scripts of the repository in two forms:

1. Importing a specific function

```python
from pyDigest import function_name
function_name()
```

The function is imported directly and can be called by typing `function_name()` with any required parameters passed in the brackets.
 
2. Importing the whole pyDigest module
 
```python
import pyDigest
pyDigest.function_name()
```

The function can be called in the script prefixed by the module's name as `pyDigest.function_name`.

### 1. `similar(id, corpus, size=10)`

The function returns the most similar documents to the one passed into it. The cosine similarity score used here is calculated from the Tfidf ("Term frequency-inverse document frequency") matrix of a given corpus.

`id`: the index of the "document" in the corpus queried for its most similar documents

`corpus`: a list of plain word strings ("documents"), the position of the "document" in the list is the id where indexing runs from 0 until len(corpus)-1

`size`: the number of documents returned, default value is set to 10.'''

The function is used, for example,  in `NLP_sections_002.py` incorporated into the more specific `similar_sections()` function to identify the most similar items among the _Digest_'s 432 thematic sections 

### 2. `similar_sections(id, size=10)`

The function returns a dataframe with the most similar thematic sections to the one passed into it. The function is based on `similar` and the information stored in `Ddf_Section_IDs_v001.csv`, `D_doc_sections_001.csv`, and `Ddf_v105.csv`. For this reason, the function **must be updated** when information could be loaded from an independently maintained relational database. 

`id`: the thematic section's id

`size`: the number of documents returned, default value is set to 10.

The function is used, for example, in `NLP_sections_002.py` to identify the most similar items among the _Digest_'s 432 thematic sections.