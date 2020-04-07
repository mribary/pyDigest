### "NLP" - Natural Language Processing

### Tokens and lemmas

1. Ddf_lemmas_sections_1.py > Ddf_Section_lemmas_v001.csv

The script imports the necessary packages, models and modules from the Classical Language Toolkit (cltk), a Python-based NLP framework for classical languages inspired by the Natural Language Toolkit (nltk).[<sup id="inline1">1</sup>](#fn1) The script initializes cltk's [`BackoffLatinLemmatizer`](http://docs.cltk.org/en/latest/latin.html#lemmatization-backoff-method) which combines multiple lemmatizer tools in a backoff chain, that is, if one tool fails to return a lemma, the token is passed on to the next tool in the chain until a lemma is returned or the chain runs out of options. The backoff method has been developed by Patrick Burns (University of Texas at Austin) and described in a presentation[<sup id="inline2">2</sup>](#fn2) and a review article with code snippets available as a pre-publication draft on GitHub.[<sup id="inline3">3</sup>](#fn3)

It creates a bag-of-words (`bow`) column which includes includes lower case linguistic tokens of the section titles stored in the `Section_title` column. Based on `bow`, the script creates a `lemmas` column which include lists of tuples where the first element of the tuple is the token and the second is its corresponding lemma. The dataframe's index is set to `Section_id` and the upper-case `Section_title` column is dropped. The dataframe is exported as `Ddf_Section_lemmas_v001.csv`.

2. Stopwords

A list of stopwords to be ignored in semantic analysis ("stoplist") is constructed specifically for the _Digest_ corpus by [cltk's `Stop` module](https://github.com/cltk/cltk/blob/master/cltk/stop/stop.py) developed by Patrick Burns. Burns discusses the module in the context of general challenges of stoplist construction in a research article published in 2018.[<sup id="inline4">4</sup>](#fn4) The module's `build-stoplist` method is highly customizable which takes parameters such as `texts`, `size`,  `remove_punctuation`, `remove_numbers` and `basis`. The latter parameter defines how stopwords are measured with the default value being `zou` which stands for the composite measure proposed by Feng Zou and his colleagues.[<sup id="inline5">5</sup>](#fn5) Their measure, whih is adopted here, is calculated from mean probability, variance  probability and entropy which are some of the other possible measure to be passed for `basis`.

Extracted stopwords are checked against Aurelien Berra's extensive list of Latin stopwords with 4,001 items.[<sup id="inline6">6</sup>](#fn6)


The module is 

aurelberra's list of stopwords tranformed into a Python dictionary

Burns

"domain-specific list construction, preprocessing, and stoplist size ... recent trends in stoplist research favor the development of generalizable methods that can construct lists on-the-fly for any given domain" (Burns 2018:7)

"Lo et al. (2005) 17 note in their stoplist study: “Each collection of documents is unique. It is therefore sen-sible to automatically fashion a different stopword list for different collections in order to maximise the performance of an IR system.”" (Burns 2018:7n22)

"two extremes: nine and Berra's 4,000"

cltk's Stop module

3. Ddf_lemmas_1.py > Ddf_lemmas_v001.csv

The script uses the same methods as `Ddf_lemmas_sections_1.py`. An additional pre-processing step removes punctuation (full stop, colon, comma, question mark) from the text. The full stop and the colon sticks to the word in the tokenization step and prevents the lemmatizer to recognise the appropriate lemma. The comma is returned as a word token and the lemmatizer attempts to process it. Series of question marks replace Greek words in the Digest text. With no semantic value, these words are ignored.

The script creates a bag-of-words (`bow`) column of the filtered text unit. The `lemmas` column includes a series of token-lemma tuples based on the list of tokens in `bow`. The dataframe is exported as `Ddf__lemmas_v001.csv`.

### Word2Vec beta

as a keyword expander: "Keyword expansion is the taking of a query term, finding synonyms, and searching for those, too."

[link](http://docs.cltk.org/en/latest/latin.html#word2vec)


### Footnotes

[<sup id="fn1">1</sup>](#inline1) Patrick J. Burns, "Building a text analysis pipeline for classical languages," in _Digital classical philology: Ancient Greek and Latin in the digital revolution_, edited by Monica Berti. Berlin: Walter de Gruyter, 2019, 159-176.

[<sup id="fn2">2</sup>](#inline2) Patrick J. Burns, "[Multiplex lemmatization with the Classical Language Toolkit](https://lila-erc.eu/wp-content/uploads/2019/06/burns-lemmatisation.pdf)," presented at the _First LiLa Workshop: Linguistic Resources & NLP Tools for Latin_ on 3 June 2019.

[<sup id="fn3">3</sup>](#inline3) Patrick J. Burns, "[Latin lemmatization: Tools, resources & future directions](https://github.com/diyclassics/lemmatizer-review/blob/master/lemmatizer-review.ipynb)," pre-publication draft available on GitHub, last updated on 3 June 2019.

[<sup id="fn4">4</sup>](#inline4) Patrick J. Burns, "[Constructing stoplists for histroical languages](https://journals.ub.uni-heidelberg.de/index.php/dco/article/view/52124/48812)," _Digital Classics Online_ 4:2 (2018): 4-20.

[<sup id="fn5">5</sup>](#inline5) Feng Zou, Fu Lee Wang, Xiaotie Deng, Song Han, and Lu Sheng Wang, "[Automatic Construction of Chinese Stop Word List](https://pdfs.semanticscholar.org/c543/8e216071f6180c228cc557fb1d3c77edb3a3.pdf),” In _Proceedings of the 5th WSEAS International Conference on Applied Computer Science_, 1010–1015.

[<sup id="fn6">6</sup>](#inline6) Aurélien Berra, "[Ancient Greek and Latin stopwords for textual analysis](https://github.com/aurelberra/stopwords)," Version according to the last commit on 11 November 2019 (git hash: cdf917c) published on GitHub.