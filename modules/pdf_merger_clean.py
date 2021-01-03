import argparse
import PyPDF2
import re
from sys import exit
from os.path import join, isdir, splitext
from os import makedirs, getcwd


class ValidateInpdf(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        self.check_args_length(values)
        setattr(namespace, self.dest, values)

    def check_args_length(self, values):
        nmin = 2
        if not nmin <= len(values):
            msg = f"positional argument {self.dest} requires at least 2 arguments"
            raise argparse.ArgumentTypeError(msg)


inpdf_arg = {
    "metavar": "PDF",
    "type": argparse.FileType("rb"),
    "nargs": "+",
    "help": "pdf list",
    "action": ValidateInpdf,
}

output_arg = {
    "default": "merged.pdf",
    "help": "name of merged pdf",
}


def create_parser():
    parser = argparse.ArgumentParser(description="Merge two or more PDF files.")
    parser.add_argument("inpdf", **inpdf_arg)
    parser.add_argument("-o", "--out", **output_arg)

    return parser


def create_new_folder(out_folder_name):
    all_before_last_slash = re.compile(r"^(.*[\\\/])")
    out_folder_path = all_before_last_slash.findall(out_folder_name)[0]

    if isdir(out_folder_path):
        return out_folder_path

    try:
        makedirs(out_folder_path)
        return out_folder_path
    except OSError:
        return None


def merge_pdf_files(pdf_list, out_file_path):
    merger = PyPDF2.PdfFileMerger()

    counter = 0
    for single in pdf_list:
        try:
            with single as pdf:
                merger.append(PyPDF2.PdfFileReader(pdf))
                print(f"{pdf.name} was merged to {out_file_path}")
            counter += 1
        except:
            pass

    merger.write(out_file_path)
    return counter


def parse_output_name(out_name):
    after_last_dot = re.compile(r"([^\.]+$)")

    if "pdf" not in after_last_dot.findall(out_name)[0]:
        return f"{out_name}.pdf"

    return out_name


def main():
    parser = create_parser()
    args = parser.parse_args()

    parsed_out = parse_output_name(args.out)

    output_folder_path = create_new_folder(args.out)
    if not output_folder_path:
        exit()

    num_merged_pdf = merge_pdf_files(args.inpdf, parsed_out)
    if num_merged_pdf:
        print(f"Successfully merged {num_merged_pdf} pdfs")
    else:
        print("Specified pdfs couldn't be merged")


if __name__ == "__main__":
    main()