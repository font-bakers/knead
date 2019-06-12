# Developer Guide

## Project structure

```
knead
├── __init__.py
├── __main__.py
├── conversions
│   ├── __init__.py
│   ├── json_to_pb.py
│   ├── pb_to_npy.py
│   ├── ttf_to_ttx.py
│   └── ttx_to_json.py
└── utils
    ├── __init__.py
    ├── glyph_batch.proto
    ├── glyph_batch_pb2.py
    └── utils.py
```

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
