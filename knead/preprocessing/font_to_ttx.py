import os
import subprocess
from glob import glob
from tqdm import tqdm


def font_to_ttx(directory):
    fonts = glob(os.path.join(directory, "font/", "*.[ot]tf"))
    for font in tqdm(fonts):
        ttx_name = os.path.split(font)[-1].split(".")[0] + ".ttx"
        subprocess.call(
            "ttx -q -o {} {}".format(
                os.path.join(directory, "ttx/", ttx_name), font
            ).split()
        )
