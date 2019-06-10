from os.path import join
from glob import glob
from re import sub

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

_FILE_EXTENSIONS = {
    "ttf": ".ttf",
    "ttx": ".ttx",
    "json": ".json",
    "proto": ".proto",
    "samples": None,
}


def get_filenames(directory, conversion):
    convert_from, convert_to = conversion.split("_to_")
    extension_from = _FILE_EXTENSIONS[convert_from]
    extension_to = _FILE_EXTENSIONS[convert_to]

    files_from = glob(join(directory, convert_from, "*" + extension_from))
    files_to = [
        sub(
            "\/{}\/".format(convert_from),
            "/{}/".format(convert_to),
            sub("{}$".format(extension_from), extension_to, file_from),
        )
        for file_from in files_from
    ]

    return zip(files_from, files_to)
