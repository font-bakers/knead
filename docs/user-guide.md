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

```
ttf -> ttx -> dict -> proto -> samples
```

`ttf_to_ttx`: will be handled by the `ttx` utility in `fonttools`. `knead` will
probably just use a `subprocess.call` to do this.

`ttx_to_dict`: https://github.com/ccurro/font-bakers/blob/master/src/serialization/parsettx.py#L226

`dict_to_proto`: https://github.com/ccurro/font-bakers/blob/master/src/serialization/writer.py#L124

`proto_to_samples`: https://github.com/ccurro/font-bakers/blob/master/sandbox/rendering/main.py#L16

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

## The `.ttf` and `.ttx` Data Formats

TTF stands for "TrueType Font", whereas TTX stands for "TrueType XML".

Here we will go over the basics of how TrueType represents a glyph.

In a TTX file each glyph is contained within a `<ttGlpyh>` tag. This tag has
several `<contour>` definitions.

> "Each contour delimits an outer or inner region of the glyph, and can be made
> of either line segments and/or second-order Beziers (also called "conic
> Beziers" or "quadratics")."
>
> - [_Glyph Hell_, David Turner](http://chanae.walon.org/pub/ttf/ttf_glyphs.htm)

In other words it defines a specific region of the font.

Within each contour we have successive `<pt>` tags which define points. They
include the $$x, y$$ location and whether the point is on curve or off curve.

Now, there are some important rules on how to understand these points.

1. If two successive points are "on" this means that they form a line.
2. If three points are "on", "off", "on" then this defines a quadratic Bezier
   curve.
3. If there are several "off" points with no "on" point in between them, there
   is a virtual "on" point in the middle of the two "off" points. This is a form
   of data compression.
4. If the first point in a contour is an "off" point go to the last point and
   start from there. If the last point is also "off" start with a virtual "on"
   in between the first and the last one.

### References

1. [_Glyph Hell_ by David
   Turner](http://chanae.walon.org/pub/ttf/ttf_glyphs.htm)
2. [The _FreeType Glyph Conventions_
   documentation](https://www.freetype.org/freetype2/docs/glyphs/glyphs-6.html)
3. [This StackOverflow
   thread](https://stackoverflow.com/questions/20733790/truetype-fonts-glyph-are-made-of-quadratic-bezier-why-do-more-than-one-consecu)
