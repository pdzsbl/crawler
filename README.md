#Crawler
-------
> Crawler is a small web crawler for pixiv, based on python3.5.2

## Features
- Find pictures under specific keyword searching(the default keyword is lovelive) of which the number of stars is larger than a specific number(the default number is 200)
- Support turning to next page and find other pictures.The defalt page range is 20 to 40

## Usage
This crawler depends on re, urllib and selenium. You can just use pip or easy install or even just install package by pycharm to install these libs.

If you have installed all above libs, you can use this crawler just by entering


`python crawler.py`


After u start, u need to enter ur pixiv account and pw by urself. And u wiil get all the picture url and their star number in a txt.