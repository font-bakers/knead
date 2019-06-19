# Quickstart

For more information on how `knead` works, refer to [the user
guide](https://font-bakers.github.io/knead/user-guide/).

## Installation

The latest release of `knead` can be installed from PyPI:

```bash
pip install knead
```

The bleeding edge development branch of `knead` can be installed from GitHub:

```bash
pip install git+https://github.com/font-bakers/knead.git
```

## Usage

On the command line:

```bash
knead --input INPUT_FORMAT --output OUTPUT_FORMAT --directory PATH/TO/DATA/
```

1. The `--input` and `--output` flags must be one of:
    - `ttf`: a `.ttf` font file.
    - `ttx`: a `.ttx` XML format of the font. For more details, refer to
      the [`fonttools`
      documentation](https://github.com/fonttools/fonttools#ttx--from-opentype-and-truetype-to-xml-and-back).
    - `json`: a `.json` format of the font.
    - `pb`: a `.pb` serialized protobuf format of each glyph in each font.
    - `npy`: a `.npy` format of samples from quadratic Bezier curves in each
      glyph in each font.

2. The `--directory` must have the following structure:

```
data
└── ttf
    ├── Georgia.ttf
    └── ...
```

_In other words, `--directory` is not the directory containing the `.ttf` files.
It is a directory that contains a subdirectory (called `ttf`) containing the
`.ttf` files._

As `knead` does each conversion, a new subdirectory will be made in `data/`,
each with the corresponding file extension.Ultimately, after `.ttf` files are
completely converted and sampled to `.npy` files, the `data/` directory will
have the following structure:

```
data
├── json
│   ├── Georgia.json
│   └── ...
├── npy_with_640_samples
│   ├── Georgia.A_upper.npy
│   ├── Georgia.B_upper.npy
│   ├── Georgia.C_upper.npy
│   └── ...
├── pb
│   ├── Georgia.A_upper.pb
│   ├── Georgia.B_upper.pb
│   ├── Georgia.C_upper.pb
│   └── ...
├── ttf
│   ├── Georgia.ttf
│   └── ...
└── ttx
    ├── Georgia.ttx
    └── ...
```

In the event of a fatal error during the data preprocessing, `knead` will simply
catch the exception and write the error message (along with a stack trace) to a
`knead.log` file.

## Optional Flags

Optional flags only matter if certain values are passed for the required flags
(e.g.  if `--output npy` is passed), and always default to some value.

1. `--normalize`: Whether or not to normalize the `x` and `y` coordinates of the
   control points by the em box size. Pass `--normalize` to set to True, and
   pass `--nonormalize` to set to False. Defaults to True. Only relevant if
   `--output json` is passed.

2. `--num_samples`: The number of samples to evaluate per quadratic Bezier
   curve. Defaults to 640. Only relevant if `--output npy` is passed.

3. `--max_num_points_in_contour`: The maximum allowable number of control points
   per contour. Any glyphs containing contours with more than this number of
   control points will raise a `RuntimeError` upon conversion. Defaults to 60.
   Only relevant if `--output npy` is passed.
