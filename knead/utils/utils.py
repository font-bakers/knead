from os.path import join
from glob import glob
from re import sub
from absl import flags

FLAGS = flags.FLAGS

UPPERCASES = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

LOWERCASES = {character.lower() for character in UPPERCASES}

NUMERALS = {
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
}

SPECIALS = {
    "exclam",
    "numbersign",
    "dollar",
    "percent",
    "ampersand",
    "asterisk",
    "question",
    "at",
}

CHARACTER_SET = UPPERCASES.union(LOWERCASES, NUMERALS, SPECIALS)


def get_filenames(directory, conversion):
    convert_from, convert_to = conversion.split("_to_")
    extension_from = "." + convert_from
    extension_to = "." + convert_to

    files_from = glob(join(directory, convert_from, "*" + extension_from))
    sub_with = (
        "/{}_with_{}_samples/".format(convert_to, FLAGS.num_samples)
        if convert_to == "npy"
        else "/{}/".format(convert_to)
    )

    files_to = [
        sub(
            "\/{}\/".format(convert_from),
            sub_with,
            sub("{}$".format(extension_from), extension_to, file_from),
        )
        for file_from in files_from
    ]

    return list(zip(files_from, files_to))
