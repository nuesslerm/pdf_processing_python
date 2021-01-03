import argparse
import PyPDF2
from os.path import join, isdir
from os import makedirs, getcwd
from sys import exit


class ValidateInpdf(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        self.check_args_length(values)
        setattr(namespace, self.dest, values)

    def check_args_length(self, values):
        nmin = 2
        print(values)
        if not nmin <= len(values):
            msg = f"positional argument {self.dest} requires at least 2 arguments"
            raise argparse.ArgumentTypeError(msg)


inpdf_arg = {
    "metavar": "PDF",
    # auto-checks if files exist, but opens a dangling file,
    # which needs to be closed manually via "with ... as file:" syntax
    # i.e. only check whether files exist if you plan to use them in the script
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
    out_folder_path = join(getcwd(), out_folder_name)

    if isdir(out_folder_path):
        return out_folder_path

    try:
        makedirs(out_folder_path)
        return out_folder_path
    except OSError:
        return None


def merge_pdf_files(pdf_list, output_folder_path):
    merger = PyPDF2.PdfFileMerger()
    # for inpdf in args.inpdf:
    #     with open(inpdf.name, "rb") as pdf:
    #         print(pdf.name)
    counter = 0
    for single in pdf_list:
        try:
            with single as pdf:
                merger.append(PyPDF2.PdfFileReader(pdf))
                print(f"{pdf.name} was merged to {output_folder_path}")
            counter += 1
        except:
            pass

    merger.write(output_folder_path)
    return counter


def main():
    parser = create_parser()
    # args = vars(parser.parse_args())
    args = parser.parse_args()

    output_folder_path = create_new_folder(args.o)

    if not output_folder_path:
        exit()

    num_merged_pdf = merge_pdf_files(args.inpdf, output_folder_path)

    if num_merged_pdf:
        print(f"Successfully merged {num_merged_pdf} pdfs")
    else:
        print("Specified pdfs couldn't be merged")


if __name__ == "__main__":
    main()