# Developer Guide

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
