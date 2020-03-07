from downloader import cliutil
from downloader import core


def main():
    arguments = cliutil.read_args()
    with core.DownloadDispatcher(arguments) as downloader:
        downloader.dispatch()


def test():
    arguments = cliutil.read_args()
    arguments.start_date = '2020-02-29'
    with core.DownloadDispatcher(arguments) as downloader:
        downloader.dispatch()


if __name__ == '__main__':
    # main()
    test()
