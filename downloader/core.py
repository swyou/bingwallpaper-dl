import asyncio

from aiohttp import client
from downloader import parsers
from aiohttp import TCPConnector

_URL_ROOT = "http://sowang.com/bbs/"
_LIST_PAGE = "forumdisplay.php?fid=67"


class DownloadDispatcher:

    def __init__(self, config):
        self.config = config
        self.pageAdviser = parsers.PageAdviser(config)
        self._loop = asyncio.get_event_loop()
        self.pages = []
        self.pic_page_urls = []
        self.conn = TCPConnector(ssl=False, limit=10, use_dns_cache=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._loop.run_until_complete(self.conn.close())
        self._loop.close()

    def dispatch(self):
        self.pages = self.pageAdviser.get_pages()
        print("%d images are expected to be downloaded." % self.pageAdviser.get_pic_number())
        print("parsing list page, %d list pages found" % len(self.pages))
        work_limit = min(len(self.pages), self.config.maxr)
        self._start_tasks(work_limit, self._handle_list_page())
        self._check_pic_number()
        work_limit = min(len(self.pic_page_urls), self.config.maxr)
        print("started to download images")
        self._start_tasks(work_limit, self._handle_pic_page())

    def _start_tasks(self, work_limit, cor_gen):
        tasks = []
        for i in range(work_limit):
            tasks.append(cor_gen)
        self._loop.run_until_complete(asyncio.wait(tasks))

    def _check_pic_number(self):
        print("parsing list page finished. %d pic urls found" % len(self.pic_page_urls))
        missed_number = self.pageAdviser.get_pic_number() - len(self.pic_page_urls)
        if missed_number > 0:
            print("there is(are) %d image(s) can't be found." % missed_number)

    async def _handle_list_page(self):
        while len(self.pages) > 0:
            page = self.pages.pop()
            content = await self._get_request_text("%s%s&page=%d" % (_URL_ROOT, _LIST_PAGE, page))
            parser = parsers.ListPageParser()
            parsed_urls = parser.parse_img_urls(content)
            parser.close()
            for date_str, url in parsed_urls:
                if self.pageAdviser.is_required_img(date_str):
                    self.pic_page_urls.append((date_str, url))
            await asyncio.sleep(0.1)

    async def _handle_pic_page(self):
        while len(self.pic_page_urls) > 0:
            img_name, url = self.pic_page_urls.pop()
            content = await self._get_request_text(_URL_ROOT + url)
            parser = parsers.ImgViewPageParser()
            src = parser.get_img_src(content)
            parser.close()
            if src:
                await self._download_img(src, img_name)
            await asyncio.sleep(0.1)

    async def _download_img(self, src, img_name):
        file_path = "%s%s.png" % (self.config.directory, img_name)
        content = None
        async with client.request("GET", src, connector=self.conn) as response:
            content = await response.read()
        if content:
            with open(file_path, 'wb') as fd:
                fd.write(content)
        print(" :=> downloaded wallpaper of date: %s" % img_name)

    async def _get_request_text(self, url):
        async with client.request("GET", url, connector=self.conn) as response:
            text = await response.text()
            return text
