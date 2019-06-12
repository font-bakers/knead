#!/bin/python

import os
import logging
from absl import flags, app
from tqdm import tqdm
import knead

FLAGS = flags.FLAGS
DATA_PIPELINE = ["ttf", "ttx", "json", "pb", "npy"]
LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

flags.DEFINE_enum("input", None, DATA_PIPELINE, "Input data format.")
flags.mark_flag_as_required("input")
flags.DEFINE_enum("output", None, DATA_PIPELINE, "Output data format.")
flags.mark_flag_as_required("output")
flags.DEFINE_string("directory", None, "Directory.")
flags.mark_flag_as_required("directory")
flags.DEFINE_integer(
    "num_samples",
    640,
    "Number of samples per Bezier curve. Defaults to 640.",
    lower_bound=1,
)
flags.DEFINE_integer(
    "max_num_points_in_contour",
    60,
    "Maximum number of control points to allow in each contour. Defaults to 60.",
    lower_bound=3,
)
flags.DEFINE_enum(
    "loglevel", "critical", LOG_LEVELS, "Logging level. Defaults to `logging.CRITICAL`."
)


def setup_logging():
    logger = logging.getLogger("knead")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    file_handler = logging.FileHandler("knead.log")
    file_handler.setLevel(logging.DEBUG)  # Lowest logging level.

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, FLAGS.loglevel.upper(), None))

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


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
    logger = setup_logging()
    conversions = determine_conversions(FLAGS.input, FLAGS.output)

    for conversion in conversions:
        print("Converting {} to {}...".format(*conversion.split("_to_")))
        filenames = knead.utils.get_filenames(FLAGS.directory, conversion)
        convert = getattr(knead.conversions, conversion, None)

        # Check that directories exist.
        dir_from = os.path.split(filenames[0][0])[0]
        dir_to = os.path.split(filenames[0][1])[0]
        if not os.path.exists(dir_from):
            raise RuntimeError("{} does not exist.".format(dir_from))
        if not os.path.exists(dir_to):
            os.mkdir(dir_to)

        # Run all data conversions, counting successful conversions and logging
        # any errors,
        num_conversions = 0
        num_exceptions = 0
        for file_from, file_to in tqdm(filenames):
            try:
                convert(file_from, file_to)
                num_conversions += 1
            except:
                logger.exception(
                    "Failed to convert {} to {}:".format(file_from, file_to)
                )
                num_exceptions += 1

        msg = "Successfully converted {} ({:.2f}%) {} file(s). See log file for details.\n".format(
            num_conversions,
            100 * num_conversions / (num_conversions + num_exceptions),
            conversion.split("_to_")[0],
        )
        print(msg)


def main():
    """ Main entry point of knead. """
    app.run(convert)
