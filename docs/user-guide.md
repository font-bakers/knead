# User Guide

## Scope

The workflow of the font bakers looks something like this block diagram:

```
------------------       ------------------------      -----------------------
|   REAL FONTS   | --->  |   MACHINE LEARNING   | ---> |   GENERATED FONTS   |
------------------       ------------------------      -----------------------
```

`knead` targets the first and last blocks: that is,

1. preprocessing raw fonts into a machine-learning-ready format, and
2. visualization of generated glyphs.

## Data Preprocessing

Under the hood, the data conversion pipeline looks like this:

```
----------      ----------     -----------     ------------     -------------
|  .ttf  | -->  |  .ttx  | --> |  .json  | --> |  .proto  | --> |  samples  |
----------      ----------     -----------     ------------     -------------
```

Note that it is possible to run the data pipeline in reverse: e.g. we can
convert ttx to ttf, and it is theoretically possible to convert dicts back into
ttx, etc. _This is currently not a priority._

Note also that `.ttf` is the only font file format currently supported: notably,
`.otf` files are not supported.

## Visualization

We cannot predict what data format the generated glyphs will be produced in.
This makes it difficult to make a tool that will automagically visualize them
for us.

The next most useful thing to do is to agree on some common data format, which
`knead` will automagically visualize, and which all generated glyphs should
eventually be converted. I think the `dict` is a good choice here (with room for
possible improvement). For an example, see
[`inconsolata.out`](https://github.com/ccurro/font-bakers/blob/master/fonts/inconsolata.out)

Dictionary, keyed by strings, valued by sub-dictionaries
Strings = glyph name (e.g. "a")
Sub-dictionaries are keyed by integers, valued by lists of lists of tuples.
Integers = contour number
Lists of lists of tuples = contours of bezier curves of 3 x,y-coords
