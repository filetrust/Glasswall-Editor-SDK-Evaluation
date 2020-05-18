import argparse
import sys


def argParser(parser):
    # Parser command line arguments

    parser.parse_args()
    args = parser.parse_args()
    validate_sisl_flag = False
    fragmentation_directory = ""
    defragmentation_directory = ""
    sisl_splitter_mode = False
    input_zip_directory = ""
    sisl_split_size = 0

    if str(args.InputZipDirectory) != 'None':
        input_zip_directory = str(args.InputZipDirectory)

    if str(args.ValidateSislInfo) != 'None':
        validate_sisl_flag = int(args.ValidateSislInfo)

    if str(args.FragmentationDirectory) != 'None':
        fragmentation_directory = str(args.FragmentationDirectory)

    if str(args.DefragmentationDirectory) != 'None':
        defragmentation_directory = str(args.DefragmentationDirectory)

    if str(args.SislSplitterMode) != 'None':
        sisl_splitter_mode = int(args.SislSplitterMode)

    if str(args.SislSplitSize) != 'None':
        sisl_split_size = int(args.SislSplitSize)

    return input_zip_directory, validate_sisl_flag, fragmentation_directory, defragmentation_directory, sisl_splitter_mode, sisl_split_size


def getCommandLineArgs():
    # Command Line Help Options

    parser = argparse.ArgumentParser()

    parser.add_argument("-i,",
                        dest="InputZipDirectory",
                        help="[Required] Input Zip File directory.",
                        type=str)

    parser.add_argument("-v,",
                        dest="ValidateSislInfo",
                        help="[Optional] extra validation and correction (if issues) for the SislInformation file.",
                        type=int)

    parser.add_argument("-m,",
                        dest="FragmentationDirectory",
                        help="[Optional] The directory you would like your output to go after fragmentation",
                        type=str)

    parser.add_argument("-o,",
                        dest="DefragmentationDirectory",
                        help="[Optional] The directory you would like your output to go after defragmentation."
                             "Please note that this must be the same as the minimise directory.",
                        type=str)

    parser.add_argument("-z,",
                        dest="SislSplitterMode",
                        help="[Required] You must choose a mode to minimise [0] or maximise [1].",
                        type=int)
    parser.add_argument("-s,",
                        dest="SislSplitSize",
                        help="[Optional] Specify the size of the Sisl's you want to split in bytes e.g. 1000000.",
                        type=int)

    return argParser(parser)
