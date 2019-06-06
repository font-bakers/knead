import subprocess


def font_to_ttx(file_from, file_to):
    subprocess.call("ttx -q -o {} {}".format(file_to, file_from).split())
