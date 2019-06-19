<p align="center">
<img src="https://raw.githubusercontent.com/font-bakers/knead/master/docs/img/logo.png" alt="Knead logo" title="Knead logo" align="center"></img>
</p>

[![Build Status](https://travis-ci.com/font-bakers/knead.svg?branch=master)](https://travis-ci.com/font-bakers/knead)
[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-352/)

---

`knead` is a command line tool for preprocessing, manipulating and serializing
font files for deep learning applications.

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Documentation](#Documentation)
- [Contributing](#Contributing)
- [License](#License)

## Installation

The latest release of `knead` can be installed from PyPI:

```bash
pip install knead
```

## Usage

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

Refer to our [quickstart](https://font-bakers.github.io/knead/quickstart/) for
more information on how to use `knead`.

## Documentation

Please refer to our [full documentation](https://font-bakers.github.io/knead/).

## Contributing

Contributions are always welcome! Please see our [issue
tracker](https://github.com/font-bakers/knead/issues) for outstanding issues,
[code of
conduct](https://github.com/font-bakers/knead/blob/master/CODE_OF_CONDUCT.md)
for community guidelines, and our [contributing
guide](https://font-bakers.github.io/knead/contributing/) for details on how to
make a contribution.

## License

`knead` is licensed under the [MIT
license](https://github.com/font-bakers/knead/blob/master/LICENSE).
