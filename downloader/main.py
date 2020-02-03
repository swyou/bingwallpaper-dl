from downloader import cliutil
from downloader import core


def main():
    arguments = cliutil.read_args()
    downloader = core.ImgDownloader(arguments)
    downloader.download()
    downloader.close()


def test():
    arguments = cliutil.read_args()
    arguments.date = '2019-01-01'
    downloader = core.ImgDownloader(arguments)
    downloader.download()
    downloader.close()


if __name__ == '__main__':
    main()
