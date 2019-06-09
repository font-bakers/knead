# Quickstart

To convert a directory of data files from one format to another:

```bash
knead --input INPUT_FORMAT --output OUTPUT_FORMAT --directory PATH/TO/DATA/
```

Note that:

1. The `--input` and `--output` flags must be one of:
    - `ttf`
    - `ttx`
    - `json`
    - `proto`
    - `samples`

2. The `data/` must have the following directory structure:

```
data
└── ttf
    ├── Helvetica.ttf
    └── ...
```

_In other words, `--directory` is not the directory containing the `.ttf` files.
It is a directory that contains a subdirectory (called `ttf`) containing the
`.ttf` files._

In the event of a fatal error during the data preprocessing, `knead` will simply
swallow the exception and write the error message (along with a stack trace) to
a `knead.log` file.

Optional flags may be added later, as required (e.g. whether or not to normalize
coordinates by the em box size, how much to pad by, the number of glyphs per
proto, etc.).
