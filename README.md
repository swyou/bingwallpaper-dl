bingwallpaper-dl
=======

Simple tool to download bing wallpapers, originally it's designed to download wallpapers from the year 2010,
however, due to restrictions applied by the APIs we use,
the earliest day we can find a wallpaper is limited to approximately 178 days ago.

bingwallpaper-dl locates bing wallpaper image by parsing content of a third-party website:
http://sowang.com/bbs/forumdisplay.php?fid=67

UPDATE ON 6TH MAR 2020:
---------

switched to an aio way.
aiohttp is used to handle http request,
requests is now removed from dependencies,

REQUIREMENTS:
---------
- Python3
- ~~requests~~
- aiohttp

DISCLAIMER:
--------

bingwallpaper-dl is only a tool that demonstrates the way to parse html content and download media file from Internet.

DO NOT USE IT TO DOWNLOAD ANY UNAUTHORIZED CONTENT.

The author of bingwallpaper-dl will NOT be responsible for any illegal use of this software.

USAGE:
-------

`git clone https://github.com/swyou/bingwallpaper-dl.git`

`cd bingwallpaper-dl`

`python setup.py install`

simply type `bwpdl` to download wallpaper for today

or

`bwpdl -d /Users/username/targetdirectory/ --date 2019-09-02` to download wallpaper for an appointed date

or

`bwpdl -d /Users/username/targetdirectory/ --from 2019-08-20` to download wallpapers from an appointed date till today
use `--to yyyy-MM-dd` to add an end constraint.

use `-d` to appoint a target directory, which is default to user's home directory

for further information see:

`bwpdl -h`
