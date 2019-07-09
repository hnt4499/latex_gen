'''
This script was highly inspired from this code:
    https://github.com/calebrob6/latexify/blob/master/latexify.py
However, I rewrite the script from the scratch for readability and
functionalities. I also keep the author's comments, because I find it useful.

Author: Hoang Nghia Tuyen
'''

import sys
import os
import argparse
from utils.tex_util import tex_to_img
from tqdm import tqdm


# Mimics the `which` unix command
# Taken from: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def main(args):
    # Test for dependencies.
    if which("latex") == None or which("dvipng") == None:
        print("Error! The commands `latex` and `dvipng` are required and "
              "could not be found in your environment.")
        return
    # Read arguments
    text_input = os.path.abspath(args.text_input)
    output_dir = os.path.abspath(args.output_dir)
    img_prefix = args.img_prefix
    dpi = args.dpi
    tmp_dir = os.path.abspath(args.tmp_dir)
    encoding = args.encoding

    success = False
    generate_filepath = lambda x: os.path.join(output_dir,
                                               "{}_{}.png".format(img_prefix, x)
                                               )
    for encoder in encoding:
        if success:
            break
        try:
            print("Try decoding input data by {}...".format(encoder))
            # Try to capture error beforehand.
            with open(text_input, "r", encoding=encoder) as lines:
                lines.readlines()
            # Actual reading input.
            with open(text_input, "r", encoding=encoder) as lines:
                i = 0
                for line in tqdm(lines):
                    tex_to_img(text=line,
                               output_path=generate_filepath(i),
                               dpi=dpi,
                               tmp_dir=tmp_dir)
                    i += 1
                success = True
                print("...Success!")
        except Exception as e:
            print("...Failed!")
            print(e)


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text_input', type=str,
        help='Path to the input text file.')
    parser.add_argument('output_dir', type=str,
        help='Path to the output png.')
    parser.add_argument('img_prefix', type=str,
        help='Image prefix. Images will be saved in `output_dir` '
             'and named `prefix`_`index`.png')
    parser.add_argument('--dpi', type=int,
        help='DPI (resolution) of output png.', default=120)
    parser.add_argument('--tmp_dir', type=str, help='Directory to which '
        'all temporary file(s) will be saved.', default="/tmp")
    parser.add_argument('--encoding', nargs='+',
        default=["UTF-8", "ISO-8859-15"],
        help='Decoder(s) to try for input data.')

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
