from html.parser import HTMLParser
import requests
import datetime
import re

_STATUS_SEARCHING = 0
_STATUS_LINE_FOUND = 1
_STATUS_TITTLE_FOUND = 2
_STATUS_URL_FOUND = 3
_STATUS_IMG_FOUND = 4

_URL_ROOT = "http://sowang.com/bbs/"
_LIST_PAGE = "forumdisplay.php?fid=67"

DATE_STR_PATTERN = re.compile(r"^\d{8}$", flags=0)


class PageAdviser(object):

    def __init__(self, config):
        self.dates: [datetime.date] = []
        self.date_strs: [str] = []
        self.pages: [int] = []
        timedelta = datetime.timedelta(days=1)
        if config.date:
            self.dates = [self._parse_date(config.date)]
            self.date_strs = [self.dates[0].strftime("%Y%m%d")]
        else:
            start_date = self._parse_date(config.start_date)
            end_date = self._parse_date(config.end_date)
            if end_date > datetime.date.today():
                end_date = datetime.date.today()
            while start_date <= end_date:
                self.dates.append(start_date)
                self.date_strs.append(start_date.strftime("%Y%m%d"))
                start_date = start_date + timedelta

    def _find_estimated_pages(self):
        start_page = self._find_estimated_page_by_date(self.dates[len(self.dates) - 1])
        end_page = self._find_estimated_page_by_date(self.dates[0])
        for i in range(start_page, end_page):
            self.pages.append(i)
        self.pages.append(end_page)

    @staticmethod
    def _find_estimated_page_by_date(date: datetime.date) -> int:
        today = datetime.date.today()
        if date >= today:
            return 1
        cursor = today - datetime.timedelta(days=26)
        if date > cursor:
            return 1
        page = 2
        while True:
            cursor = cursor - datetime.timedelta(days=30)
            if date > cursor:
                return page
            page = page + 1

    @staticmethod
    def _parse_date(str: str) -> datetime.date:
        if not str:
            return datetime.date.today()
        splits = str.split("-")
        if len(splits) is not 3:
            return datetime.date.today()
        try:
            year = int(splits[0])
            month = int(splits[1])
            day = int(splits[2])
            return datetime.date(year=year, month=month, day=day)
        except ValueError:
            return datetime.date.today()

    def get_pages(self) -> [int]:
        if len(self.pages) == 0:
            self._find_estimated_pages()
        return self.pages

    def is_required_img(self, date_str: str) -> bool:
        if not date_str:
            return False
        return self.date_strs.count(date_str) > 0


class ImgDownloader(HTMLParser):

    def __init__(self, config):
        HTMLParser.__init__(self)
        self.status = _STATUS_SEARCHING
        self.config = config
        self.page_adviser = PageAdviser(config)
        self.last_url = None

    def download(self):
        pages = self.page_adviser.get_pages()
        for page in pages:
            response = requests.request("GET", "%s%s&page=%d" % (_URL_ROOT, _LIST_PAGE, page))
            self.feed(response.text)
            self.reset()

    def _check_if_is_line(self, tag, attrs):
        if tag == 'tbody':
            for each in attrs:
                if "id" == each[0] and each[1].startswith("normalthread"):
                    self.status = _STATUS_LINE_FOUND
                    return

    def _check_if_is_tittle(self, tag):
        if tag == "th":
            self.status = _STATUS_TITTLE_FOUND

    def _check_if_is_url(self, tag, attrs):
        if tag == "a":
            for each in attrs:
                if "class" == each[0] and each[1] == "s xst":
                    self.status = _STATUS_URL_FOUND
                    break
            if self.status == _STATUS_URL_FOUND:
                for each in attrs:
                    if "href" == each[0]:
                        self.last_url = each[1]

    def handle_detail_view_url(self, url, img_name: str):
        response = requests.request("GET", _URL_ROOT + url)
        # response.raise_for_status()
        parser = ImgViewPageParser()
        parser.feed(response.text)
        if parser.src:
            response = requests.request("GET", parser.src)
            file_path = "%s%s.png" % (self.config.directory, img_name)
            with open(file_path, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=512 * 1024):
                    fd.write(chunk)
            print("downloaded wallpaper of date: %s" % img_name)
        parser.close()

    @staticmethod
    def _format_file_name(date_str: str):
        if not date_str:
            return None
        if DATE_STR_PATTERN.match(date_str):
            # a = re.match(r"^\d{8}$", date_str, flags=0)
            return date_str
        else:
            date_str = date_str.replace("（", "").replace("）", "")
            try:
                parsed_date = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
                return parsed_date.strftime("%Y%m%d")
            except ValueError:
                print("unknown date format: %s, you can commit a issue on this." % date_str)
                return None

    def handle_starttag(self, tag, attrs):
        if self.status == _STATUS_SEARCHING:
            self._check_if_is_line(tag, attrs)
        elif self.status == _STATUS_LINE_FOUND:
            self._check_if_is_tittle(tag)
        elif self.status == _STATUS_TITTLE_FOUND:
            self._check_if_is_url(tag, attrs)

    def handle_data(self, data):
        if self.status == _STATUS_URL_FOUND and self.last_url:
            splits = data.split()
            if len(splits) > 0:
                date_str = splits[len(splits) - 1]
                date_str = self._format_file_name(date_str)
                if self.page_adviser.is_required_img(date_str):
                    self.handle_detail_view_url(self.last_url, date_str)

    def handle_endtag(self, tag):
        if self.status == _STATUS_URL_FOUND and tag == "a":
            self.status = _STATUS_SEARCHING


class ImgViewPageParser(HTMLParser):

    status = _STATUS_SEARCHING
    src = None

    def handle_starttag(self, tag, attrs):
        if self.status == _STATUS_SEARCHING:
            if tag == "img":
                for each in attrs:
                    if "id" == each[0] and each[1].startswith("aimg_"):
                        self.status = _STATUS_IMG_FOUND
                        break
            if self.status == _STATUS_IMG_FOUND:
                for each in attrs:
                    if "src" == each[0]:
                        self.src = each[1]
