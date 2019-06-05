# Knead Specification

## Scope

The workflow of the font bakers looks something like this block diagram:

```
REAL FONTS  -->  MACHINE LEARNING  -->  GENERATED FONTS  -->  VISUALIZATION
```

`knead` targets the first arrow and the last block: that is,

1. data preprocessing into some machine-learning-ready data format, and
2. visualization of generated glyphs.

## Data Preprocessing Pipeline

```
otf/ttf -> ttx -> dict -> proto -> samples
```

ttf2ttx: will be handled by the `ttx` utility in `fonttools`. `knead` will
probably just use a `subprocess.call` to do this.

ttx2dict: https://github.com/ccurro/font-bakers/blob/master/src/serialization/parsettx.py#L226

dict2proto: https://github.com/ccurro/font-bakers/blob/master/src/serialization/writer.py#L124

proto2samples: https://github.com/ccurro/font-bakers/blob/master/sandbox/rendering/main.py#L16

It may be possible to run the data pipeline in reverse: e.g. we can convert ttx
to otf/ttf, and it is theoretically possible to convert dicts back into ttx,
etc. _This is currently not a priority._

In the end, users can expect to run something like this:

```
knead --in ttx --out proto --dir myfonts/
```

with the result being that one or more new directories will be created with the
appropriate output (e.g. `myfonts_dicts` and `myfonts_protos`, or something
similar).

Optional flags can be added as required (e.g. whether or not to normalize
coordinates by the em box size, how much to pad by, the number of glyphs per
proto, etc.).

## Visualization Pipeline

TODO

## Miscellaneous Details

- Target Python 3.5+ compatibility.
- Use `black` to format code.
