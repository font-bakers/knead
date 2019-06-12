import subprocess


def ttf_to_ttx(file_from, file_to):
    command = "ttx -q -o {} {}".format(file_to, file_from).split()
    return_code = subprocess.call(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    if return_code != 0:
        raise RuntimeError("fonttools ttx utility failed on {}.".format(file_from))
