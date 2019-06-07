# Quickstart

To convert a directory of `.ttf` files to `.proto` files:

```bash
knead --input ttf --output proto --directory path/to/data/
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

<aside class="notice">
In other words, `--directory` is not the directory containing the `.ttf` files.
It is a directory that contains a subdirectory (called `ttf`) containing the
`.ttf` files.
</aside>

Optional flags may be added later, as required (e.g. whether or not to normalize
coordinates by the em box size, how much to pad by, the number of glyphs per
proto, etc.).
