import argparse
import html.parser

def read_args():
    parser = argparse.ArgumentParser(description="Download bing wallpaper by simple commands")
    parser.add_argument("-d", help="download directory, default to current directory", type=str)
    parser.add_argument("-v", "--version", help="show version", action="version", version="0.0.1")
    parser.add_argument("--from", help="start date", type=str)
    parser.add_argument("--to", help="end date, default to today.", type=str)
    parser.add_argument("--date", help="download wallpaper of a specific day", type=str)
    # parser.add_argument("--worker", help="number of download workers, default is one.", type=int)
    return validate_args(parser.parse_args())


def validate_args(args_map):
    directory = args_map['d']
    if not directory:
        args_map['d'] = ""
    elif not directory.endswith("/"):
        args_map['d'] = directory + "/"
    if not args_map['from'] and not args_map['date']:
        pass
    return args_map
