# About Knead

## Scope

The workflow of the font bakers looks something like this block diagram:

```
REAL FONTS  -->  MACHINE LEARNING  -->  GENERATED FONTS  -->  VISUALIZATION
```

`knead` targets the first arrow and last block: that is,

1. data preprocessing into some machine-learning-ready format, and
2. visualization of generated glyphs.

## Data Preprocessing

```
otf/ttf -> ttx -> dict -> proto -> samples
```

`ttf2ttx`: will be handled by the `ttx` utility in `fonttools`. `knead` will
probably just use a `subprocess.call` to do this.

`ttx2dict`: https://github.com/ccurro/font-bakers/blob/master/src/serialization/parsettx.py#L226

`dict2proto`: https://github.com/ccurro/font-bakers/blob/master/src/serialization/writer.py#L124

`proto2samples`: https://github.com/ccurro/font-bakers/blob/master/sandbox/rendering/main.py#L16

Note that it is possible to run the data pipeline in reverse: e.g. we can
convert ttx to otf/ttf, and it is theoretically possible to convert dicts back
into ttx, etc. _This is currently not a priority._

In the end, users can expect to run something command line tool like this:

```
knead --in ttx --out proto --dir myfonts/
```

with the result being that one or more new directories will be created with the
appropriate output (e.g. `myfonts_dicts` and `myfonts_protos`, or something
similar).

Optional flags can be added as required (e.g. whether or not to normalize
coordinates by the em box size, how much to pad by, the number of glyphs per
proto, etc.).

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

## Miscellaneous Details

- Target Python 3.5+ compatibility.
- Use `black` to format code.
