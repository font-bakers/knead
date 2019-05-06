from absl import flags, app
from glob import glob

FLAGS = flags.FLAGS

flags.DEFINE_string("dir", None, "Directory.")
flags.mark_flags_as_required("dir")
flags.DEFINE_string("mode", None, "Mode.")
flags.mark_flags_as_required("mode")


def main(argv):
    pass


if __name__ == "__main__":
    app.run(main)
