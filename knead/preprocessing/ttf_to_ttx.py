import subprocess


def ttf_to_ttx(file_from, file_to):
    return_code = subprocess.call("ttx -q -o {} {}".format(file_to, file_from).split())

    if return_code != 0:
        raise RuntimeError("Failed to convert {}.".format(file_from))
