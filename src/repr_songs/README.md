# About repr_songs

This is a module which try to get the most representive songs of each singer.

The data file should be a csv file that has format `(artist, song, lyrics)`.

Since this module uses `nltk`, `pandas`, you should install them, and use nltk
to download the *stopwords*. For downloading stopwords try
'''python
import nltk
nltk.download('stopwords')
'''

There is only one public function in this module: `get_rep_songs()`, you can
set the number of representive songs you want and use how much representive
terms to select the songs.

I have not done the arguments validation yet, so plz do not use number_of_terms
that not too big.

The return value of this function is a dictionary with format `{singer: {song:
lyrics, ...}}`. This function also use `pickle` to serialize the dictionary, so
you don't need to run this module everytime.

The usage of `pickle` is:
```python
import pickle

# object you want to serialize
a = {'hello': 'world'}

# store it into file
with open('filename.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

# restore it back to python object
with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)
'''
