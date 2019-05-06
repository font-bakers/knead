#!/bin/python

import os
from absl import flags, app
from glob import glob

FLAGS = flags.FLAGS
MODES = [
    "font2ttx",  # Convert font files to ttx files
    "ttx2proto",  # Convert ttx files to protobufs
    "proto2samples",  # Convert protobufs to Bezier samples
    "render",  # Render glyphs
]

flags.DEFINE_string("dir", None, "Directory.")
flags.mark_flag_as_required("dir")
flags.DEFINE_enum("mode", None, MODES, "Mode.")
flags.mark_flag_as_required("mode")


def main(argv):
    pass


if __name__ == "__main__":
    app.run(main)
