import os
from glob import glob
import subprocess
from tqdm import tqdm


def font_to_ttx(directory):
    fonts = glob(os.path.join(directory, "font/", "*.[ot]tf"))
    for font in tqdm(fonts):
        subprocess.call("ttx {} -q".format(font).split())
