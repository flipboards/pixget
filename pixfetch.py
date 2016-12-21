#!/usr/bin/python3
# fetch image urls with corresponding tag.


import pixget
import requests
import bs4
import sys
import codecs


# pixiv search page url
operate_url = pixget.root_url + '/search.php'


def search_one_page(tag, page_index, ImageInfo):
    """
    Download the index page of the search result for the tag.
    :param tag: The search option.
    :param page_index: Page index of the search result.
    :param ImageInfo: The array to put image infomation
    :return: 0 for complete, 1 for error.
    """

    try:
        r = requests.get(operate_url, params=dict(word=tag, p=page_index), cookies=pixget.mycookies)
    except ConnectionError:
        print('Sorry, search page cannot be opened')
        return 1
    else:
        print('get page ' + r.url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

    for ImgItem in soup.find_all('li', class_='image-item'):  # find image boxes

        ImgIndex = int(ImgItem.contents[0].attrs.get('href').split('=')[-1])  # image index
        print('get image ' + str(ImgIndex))

        Img = ImgItem.contents[0].find('img')
        ImgUrl = Img.attrs.get('src')
        # check if multiple images
        if 'manga' in ImgItem.contents[0].attrs.get('class'):
            IsMultiple = True
        else:
            IsMultiple = False

        # download other information
        if len(ImgItem.contents) >= 4:
            ImgTags = Img['data-tags']
            ImgTitle = ImgItem.contents[1].text
            ImgAuthor = int(ImgItem.contents[2].attrs.get('data-user_id'))
            ImgCollection = int(ImgItem.contents[3].find('a').text)
            ImageInfo[ImgIndex] = dict(ImgUrl=ImgUrl, ImgTitle=ImgTitle, ImgAuthor=ImgAuthor, ImgTags=ImgTags,
                                   ImgCollection=ImgCollection, IsMultiple=IsMultiple)
    return 0


def write_data_head(filename):
    """
    Write head of data, in the case that there is too much data.
    :param filename: Output filename. Format is utf-8
    :return: 1 for error.
    """
    try:
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write('PixId,Title,IsMultiple,Collection,Author,Tags\n')
    except IOError:
        print('Cannot write file ' + str(filename))
        return 1


def write_data_content(filename, ImageInfo):
    """
    Write data content as columns
    :param filename: Same as write_data_head
    :param ImageInfo: The array contains image information
    """
    with codecs.open(filename, 'a', 'utf-8') as f:
        for (ImgIndex, ImgData) in ImageInfo.items():
            f.write(str(ImgIndex) + '\t' + ImgData['ImgTitle'] + '\t' + str(ImgData['IsMultiple']) + '\t' + str(
                ImgData['ImgCollection']) + '\t' + str(ImgData['ImgAuthor']) + '\t' + ImgData['ImgTags'] + '\n')


def main():
    ImageInfo = {}
    if len(sys.argv) < 3:
        print('Usage: pixfetch [tag] [page number]')
    for i in range(1, int(sys.argv[2]) + 1):
        if search_one_page(sys.argv[1].decode('gbk').encode('utf-8'), i, ImageInfo) == 1:
            break
    if write_data_head(sys.argv[1] + '.txt'):
        return 1
    write_data_content(sys.argv[1] + '.txt', ImageInfo)


if __name__ == '__main__':
    main()
