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

### 3. `linkage_for_clustering(X, threshold=0.5)`

The function takes a matrix X with observations stored in rows and features stored in columns. It returns a dataframe with linkage combinations of method and metric used for hierarchical clustering sorted by reverse order based on the absolute value of the cophenetic correlation coefficient (CCC). The CCC score ranges between -1 and 1 and measures how how faithfully a dendrogram preserves the pairwise distances between the original unmodeled data points. The cophenetic correlation is expected to be positive if the original distances are compared to cophenetic distances (or similarities to similarities) and negative if distances are compared to similarities.

It needs to be noted that CCC is calculated for the whole dendrogram. Ideally, one should calculate CCC at the specific cut point where the dendrogram's output is used to identify the clusters. It is recommended to calculate CCC at the specific cut level yielding k clusters to confirm that the correct method-metric combination has been used for hierarchical clustering.

The 'average' method generally produces the best CCC score especially with matrices with high dimensionality. Instead of relying exclusively on the CCC score, one also needs to consider what method-metric combination suits the particular dataset on which hierarchical clustering is performed by scipy's linkage function.

#### Methods for scipy's linkage function

Default method is `'ward'`.

| Method | Note |
|:---|:---|
| 'ward' | Uses the Ward variance minimization algorithm |
| 'single' | Nearest Point algorithm | 
| 'complete' | Farthest Point Algorithm or Voor Hees Algorithm |
| 'average' | UPGMA algorithm |
| 'weighted'| WPGMA algorithm |
| 'centroid' | Euclidean distance between the centroid and the centroid of a remaining cluster |
| 'median' | Merged clusters' centroid to be come the average |

#### Metrics for scipy's linkage function

Default metric is `'euclidean'`.

Possible metrics are ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, \‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulsinski’, ‘mahalanobis’, ‘matching’, ‘minkowski’, \‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’.

#### How to read the linkage matrix

Z[i] will tell us which clusters were merged in the i-th iteration.

Z[0] with an output array([ 52.     ,  53.     ,   0.04151,   2.     ])

In its first iteration the linkage algorithm decided to merge the two clusters (original samples here) with indices 52 and 53, as they only had a distance of 0.04151. This created a cluster with a total of 2 samples. We can see that each row of the resulting array has the format idx1, idx2, dist, sample_count.