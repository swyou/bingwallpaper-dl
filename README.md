bingwallpaper-dl
=======

REQUIREMENTS:
---------
- python3
- requests

DISCLAIMER:
--------
bingwallpaper-dl locates bing wallpaper image by parsing content of a third-party website:
http://sowang.com/bbs/forumdisplay.php?fid=67

bingwallpaper-dl is only a tool that demonstrates the way to parse html content and download media file from Internet.

DO NOT USE IT TO DOWNLOAD ANY UNAUTHORIZED CONTENT.

The author of bingwallpaper-dl will NOT be responsible for any illegal use of this software.

USAGE:
-------

`clone https://github.com/swyou/bingwallpaper-dl.git`

`cd bingwallpaper-dl`

`python setup.py`

simply type `bwpdl` to download wallpaper for today

or

`bwpdl -d /Users/username/targetdirectory/ --date 2019-09-02` to download wallpaper for appointed date

or

`bwpdl -d /Users/username/targetdirectory/ --from 2019-08-20` to download wallpapers from an appointed date to today
use `--to yyyy-MM-dd` to add an end constraint.

use `-d` to appoint a target directory, its default to user's home directory

for further information see:

`bwpdl -h`
