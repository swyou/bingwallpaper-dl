import argparse
import os


def read_args():
    parser = argparse.ArgumentParser(description="Download bing wallpaper by simple commands")
    parser.add_argument("-d", dest="directory", help="download directory, default to current directory", type=str)
    parser.add_argument("-v", "--version", help="show version", action="version", version="0.1.0")
    parser.add_argument("--from", dest="start_date", help="start date", type=str)
    parser.add_argument("--to", dest="end_date", help="end date, default to today.", type=str)
    parser.add_argument("--date", help="download wallpaper of a specific day", type=str)
    # parser.add_argument("--worker", help="number of download workers, default is one.", type=int)
    return validate_args(parser.parse_args())


def validate_args(arguments):
    if not arguments.directory:
        arguments.directory = os.path.expanduser("~") + "/bingwallpapers/"
    elif not arguments.directory.endswith("/"):
        arguments.directory += "/"
    if not os.path.exists(arguments.directory):
        os.makedirs(arguments.directory)
    return arguments
