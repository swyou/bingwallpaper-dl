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
        self.pic_urls = []
        self._finished_pic_count = 0
        self.conn = TCPConnector(ssl=False, limit=100, use_dns_cache=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._loop.run_until_complete(self.conn.close())
        self._loop.close()

    def dispatch(self):
        self.pages = self.pageAdviser.get_pages()
        work_limit = min(self.pageAdviser.get_pic_number(), self.config.maxr)
        tasks = []
        for i in range(work_limit):
            tasks.append(self._handle())
        self._loop.run_until_complete(asyncio.wait(tasks))

    def finished(self):
        return self._finished_pic_count == self.pageAdviser.get_pic_number()

    async def _handle(self):
        while not self.finished():
            if len(self.pages) > 0:
                page = self.pages.pop()
                await self._handle_list_page(page)
            if len(self.pic_page_urls) > 0:
                pic_page_url = self.pic_page_urls.pop()
                await self._handle_pic_page(pic_page_url[1], pic_page_url[0])
            if len(self.pic_urls) > 0:
                pic_url = self.pic_urls.pop()
                await self._download_img(pic_url[1], pic_url[0])
            await asyncio.sleep(0.1)

    async def _handle_list_page(self, page):
        content = await self._get_request_text("%s%s&page=%d" % (_URL_ROOT, _LIST_PAGE, page))
        parser = parsers.ListPageParser()
        parsed_urls = parser.parse_img_urls(content)
        parser.close()
        for date_str, url in parsed_urls:
            if self.pageAdviser.is_required_img(date_str):
                self.pic_page_urls.append((date_str, url))

    async def _handle_pic_page(self, url, img_name):
        content = await self._get_request_text(_URL_ROOT + url)
        parser = parsers.ImgViewPageParser()
        src = parser.get_img_src(content)
        parser.close()
        if src:
            self.pic_urls.append((img_name, src))

    async def _download_img(self, src, img_name):
        file_path = "%s%s.png" % (self.config.directory, img_name)
        content = None
        async with client.request("GET", src, connector=self.conn) as response:
            content = await response.read()
        if content:
            with open(file_path, 'wb') as fd:
                fd.write(content)
        print("downloaded wallpaper of date: %s" % img_name)
        self._finished_pic_count = self._finished_pic_count + 1

    async def _get_request_text(self, url):
        async with client.request("GET", url, connector=self.conn) as response:
            text = await response.text()
            return text
