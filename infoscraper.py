#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  this file is a scraper, download the image imformation of pictures.


import pixfetch
import sys
import getopt


def get_part_pages(tag, start, end, filename):
    """
    Get pages from start to end.
    :param tag: The search tag.
    :param start: Start page index.
    :param end: End page index.
    :param filename: Saved file.
    :return: 1 for error
    """
    ImageInfo = {}
    MeetError = False

    for i in range(start, end):
        lastInfoLength = len(ImageInfo)
        if pixfetch.search_one_page(tag, i, ImageInfo) == 1:
            MeetError = True
            break
        if len(ImageInfo) == lastInfoLength:
            print('The search result only has ' + str(i-1) + ' pages.')
            break
    print('Saving...')
    pixfetch.write_data_content(filename, ImageInfo)
    if MeetError:
        return 1


def main():
    step = 10
    info = ''
    infopath = ''
    limit = 1000
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:t:s:h')
    except getopt.GetoptError:
        print('Use -h to get help.')
        return 1

    for opt, arg in opts:
        if opt == '-t':
            info = arg
            infopath = arg + '.txt'
        elif opt == '-s':
            step = int(arg)
        elif opt == '-l':
            limit = int(arg)
        elif opt == '-h':
            print('Usage: python infoscraper.py -t [tag] (-s [step]) (-l [limit])')
            return

    if not info:
        print('Please specify a path!')
        return 1

    if pixfetch.write_data_head(infopath) == 1:
        return 1

    for j in range(1, limit + 1 - step, step):
        if get_part_pages(info, j, j+step, infopath) == 1:
            exit(0)


if __name__ == '__main__':
    main()
