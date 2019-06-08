#!/bin/python

from absl import flags, app
from tqdm import tqdm
from knead.preprocessing import ttf_to_ttx, ttx_to_json, json_to_proto
from knead.utils import get_filenames


FLAGS = flags.FLAGS
DATA_PIPELINE = ["ttf", "ttx", "json", "proto", "samples"]

flags.DEFINE_enum("input", None, DATA_PIPELINE, "Input data format.")
flags.mark_flag_as_required("input")
flags.DEFINE_enum("output", None, DATA_PIPELINE, "Output data format.")
flags.mark_flag_as_required("output")
flags.DEFINE_string("directory", None, "Directory.")
flags.mark_flag_as_required("directory")


def determine_conversions(input_format, output_format):
    """
    Determines the required data conversions, given an input and output data
    format.

    Parameters
    ----------
    input_format, output_format : string
        One of the data formats in the data pipeline.

    Returns
    -------
    conversions : list
        A list of strings, each describing one required data conversion.
    """
    input_idx = DATA_PIPELINE.index(input_format)
    output_idx = DATA_PIPELINE.index(output_format)

    if input_idx == output_idx:
        msg = "Expected different input and output data formats, got identical data formats."
        raise ValueError(msg)

    if output_idx < input_idx:
        msg = "Conversion of data formats back the pipeline is not implemented yet."
        raise NotImplementedError(msg)

    conversions = [
        "{}_to_{}".format(first_format, second_format)
        for first_format, second_format in zip(
            DATA_PIPELINE[input_idx:output_idx],
            DATA_PIPELINE[input_idx + 1 : output_idx + 1],
        )
    ]
    return conversions


def convert(argv):
    conversions = determine_conversions(FLAGS.input, FLAGS.output)

    for conversion in conversions:
        print("Converting {} to {}...".format(*conversion.split("_to_")))

        if conversion == "ttf_to_ttx":
            convert = ttf_to_ttx
        elif conversion == "ttx_to_json":
            convert = ttx_to_json
        elif conversion == "json_to_proto":
            convert = json_to_proto
        elif conversion == "proto_to_samples":
            pass

        for file_from, file_to in tqdm(get_filenames(FLAGS.directory, conversion)):
            convert(file_from, file_to)

        print()  # Print new lint


def main():
    """ Main entry point of knead. """
    app.run(convert)
