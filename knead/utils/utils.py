from os.path import join
from glob import glob
from re import sub


CHARACTER_SET = {
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
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
    "exclam",
    "numbersign",
    "dollar",
    "percent",
    "ampersand",
    "asterisk",
    "question",
    "at",
}

_FILE_EXTENSIONS = {
    "font": ".ttf",
    "ttx": ".ttx",
    "dict": ".pkl",
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
