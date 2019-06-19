# Developer Guide

## The TrueType standard and the `.ttx` file format

Briefly, the [TrueType font standard](https://en.wikipedia.org/wiki/TrueType)
encodes all of the information discussed in [the user
guide](https://font-bakers.github.io/knead/user-guide/#glyphs-contours-and-bezier-curves).

The `.ttx` file format is simply an XML file that encodes a font, specified by
`fonttools`. In a `.ttx` file, each glyph is contained within a `<ttGlyph>` tag.
This tag has several `<contour>` definitions.

Within each contour we have successive `<pt>` tags which define control points.
Each control point specifies its location (i.e., x and y coordinates) and
whether the point is "on curve" or "off curve".

There are some important rules on how to understand these points.

1. If two successive points are "on" this means that they form a line.
2. If three points are "on", "off", "on" then this defines a quadratic Bezier
   curve.
3. If there are several "off" points with no "on" point in between them, there
   is a virtual "on" point in the middle of the two "off" points. This is a form
   of data compression.
4. If the first point in a contour is an "off" point go to the last point and
   start from there. If the last point is also "off" start with a virtual "on"
   in between the first and the last one.

For more information, refer to:

- [The `fonttools`
  documentation](https://github.com/fonttools/fonttools#ttx--from-opentype-and-truetype-to-xml-and-back).
- [_Glyph Hell_ by David Turner](http://chanae.walon.org/pub/ttf/ttf_glyphs.htm)
- [The _FreeType Glyph Conventions_
  documentation](https://www.freetype.org/freetype2/docs/glyphs/glyphs-6.html)
- [This StackOverflow thread on parsing `.ttf`
  files](https://stackoverflow.com/q/20733790)

## Protocol buffers (protobufs)

In the words of [the Google
documentation](https://developers.google.com/protocol-buffers/docs/overview),
protocol buffers are

> a language-neutral, platform-neutral, extensible way of serializing structured
> data for use in communications protocols, data storage, and more. 

For more information on protobufs, please refer to [the protobuf developer
guide](https://developers.google.com/protocol-buffers/docs/overview), and [the
protobuf tutorial for
Python](https://developers.google.com/protocol-buffers/docs/pythontutorial).
Here, we describe how `knead` uses protobufs.

The
[`glyph_batch.proto`](https://github.com/font-bakers/knead/blob/master/knead/utils/glyph_batch.proto)
file specifies the protobuf for a batch of glyphs, and the
[`glyph_batch_pb2.py`](https://github.com/font-bakers/knead/blob/master/knead/utils/glyph_batch_pb2.py)
is the [corresponding output of the protobuf
compiler](https://developers.google.com/protocol-buffers/docs/pythontutorial#compiling-your-protocol-buffers).

To compile a `glyph_batch.proto` file to a Python file, you will need to install
the protobuf compiler (`protoc`). See the [protobuf compiler installtion
instructions](https://github.com/protocolbuffers/protobuf/#protocol-compiler-installation).
Then, run the following command from the project root directory:

```bash
protoc --proto_path=knead/utils/ --python_out=knead/utils/ knead/utils/glyph_batch.proto
```

## Miscellaneous notes

- Since `knead` relies heavily on `fonttools` (specifically, the `ttx` command
  line tool) to convert `.ttf` files to `.ttx`, correct and reproducible
  behavior is contingent on having the correct version of `fonttools`.
  Therefore, the `fonttools` version number is pinned in `knead`'s
  [`requirements.txt`](https://github.com/font-bakers/knead/blob/master/requirements.txt).
