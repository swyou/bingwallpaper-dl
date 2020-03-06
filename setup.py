import codecs
from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bingwallpaper-dl",
    version="0.1.0",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="bingwallpaper-dl is only a tool that demonstrates the way to parse html content and download media file from Internet.",
    author='S.W.You',
    packages=['downloader'],
    package_data={
        'bingwallpaper-dl': ['README.rst', 'LICENSE']
    },
    install_requires=['aiohttp'],
    entry_points="""
    [console_scripts]
    bwpdl = downloader.main:main
    """,
    long_description=long_description,
)
