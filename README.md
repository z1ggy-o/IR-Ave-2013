# Find Similarity Between Singers Through Lyrics Analysis

Team: ave-2013

## Directory Structure

- src: All source codes
- data: Input data and intermedia data
- material: Materials for representation and data virsulization

In `src` directory, different approach's codes are stored in compare_versions
directory.

In repr_songs, there is the code which select the representative terms and
songs.

## Dependency

- Python: 3.5 or higher
- NLTK: for stemming and tokenization
- matplotlib: for data virsulization
- numpy

## Usage

*You may need to modify the file path for each src code*

### repr_songs

You can chose to use `repr_songs` directly to get the representative terms and
representative songs. It will serialize the result dictionary into a `.picle`
file. Or you can combine it with other modules.

The input file is `.csv` file which format is `song, artist, lyrics`.

You can change number of representative terms and songs in function
`get_repr_songs` as you wish. 

### main

The `main.ipynb` uses representative songs that selected by `repr_songs`, then
build VSM to compute the similarity between singers.

It will plot a networking graph and print out the most sililar and non-similar
singers.

You can change the argument to modify the networking graph.

### compare_versions

In this directory, there are codes we have tried to compare results of
different approach. You can just leave them alone, or check results of other
approach. (ps. these codes are not refactoried)

### single_lyrics_compare

In this directory we create some simple code to let you compute the similarity
between single lyrics file and the singers from your given `.csv` file
previously.

Each file uses different approach correspond to `compare_versions`. (Need to be
refactoried)
