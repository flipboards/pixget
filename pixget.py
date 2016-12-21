<<<<<<< HEAD
#!/usr/bin/python3
# this file contains basic information about downloading pictures.
# it can save the corresponding picture when gets pixid.

import requests
import sys
import bs4
import os

# pixiv root url
root_url = 'http://www.pixiv.net'

# page contains image
operate_url = root_url + '/member_illust.php'

# cookies
mycookies = dict(PHPSESSID='18002369_151fa062b11bd07f9e802879a8144dbb',
                 __utmz='235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=18002369=1',
                 __ga='GA1.2.897318290.1470488357', manga_viewer_expanded='1',
                 module_orders_mypage='%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D',
                 p_ab_id='7')


# only used in debug
def save_webpage(Page):
    open('result.html', 'wb').write(Page)


def get_image_url2(pixid, index, imgInfoPool):
    """download an image in multiple images
    Args:
    :param pixid: The pixiv id of the picture groups, int.
    :param index: The page index to download.
    :param imgInfoPool: Array to put the image url and other data.

    Returns:
    :return: 1 for invalid id, 2 for timeout.
    """

    PageParams = dict(mode='manga_big', illust_id=pixid, page=index)
    try:
        r = requests.get(operate_url, params=PageParams, cookies=mycookies)
    except requests.exceptions.ConnectionError:
        print('I cannot open the page. Maybe the id is invalid?')
        return 1
    else:
        soup = bs4.BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
        img = soup.find('img')
        imgName = soup.find('title').string
        imgInfoPool.append(dict(id=pixid + '_p' + str(index), name=imgName, url=img.attrs.get('src'), pageurl=r.url))
        return


def get_image_url(pixid, imgInfoPool, multiAutocheck=0, timeout=10):
    """
    Put the image url into imgInfoPool.
    Currently this function will not print anything to keep speed.

    Arguments:
    :param pixid: Pixiv id of image.
    :param imgInfoPool: The array contains image information.
    :param multiAutocheck: 0: later determined (will cause user input); 1: download all; 2: download none.

    Returns:
    :return: 1 for invalid id, 2 for timeout.
    """

    # open the page
    try:
        r = requests.get(operate_url, params=dict(mode='medium', illust_id=pixid), cookies=mycookies)
    except ConnectionError:
        print('I cannot open the page. Maybe the id is invalid?')
        return 1

    soup = bs4.BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
    img = soup.find('img', class_='original-image')
    if not img:  # multiple images, or error
        if multiAutocheck == 2:  # silence
            return None

        try:
            r = requests.get(operate_url, params=dict(mode='manga', illust_id=pixid), cookies=mycookies)
        except ConnectionError:  # it's error
            print('I cannot open the page. Maybe the id is invalid?')
            return 1
        else:   # it's multiple images
            soup = bs4.BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
            imgNumber = len(soup.find_all('div', class_='item-container'))
            if imgNumber == 0:
                print('Cannot find pictures in the page. Please try again?')
                print('Url is ' + r.url)
                return 1

        if multiAutocheck == 1:
            imgIndex = 'a'
        elif multiAutocheck == 0:
            imgIndex = input('Illustration ' + str(pixid) + ' has ' + str(
                    imgNumber) + ' pictures. Download all (a) or index: (number)')

        if imgIndex == 'a':
            for i in range(0, imgNumber):
                result2 = get_image_url2(pixid, i, imgInfoPool)
                if result2:
                    return result2
        else:
            result2 = get_image_url2(pixid, int(imgIndex), imgInfoPool)
            if result2:
                return result2

    else:  # one image
        imgName = img.attrs.get('alt')
        imgInfoPool.append(dict(id=pixid, name=imgName, url=img.attrs.get('data-src'), pageurl=r.url))
        return


def download_image(save_dir, imgInfoPool, timeout=10, replaceExist=False):
    """Download all images from imgInfoPool.

    :param save_dir: The directory to save.
    :param imgInfoPool: The image information array, contains url and pageurl.
    """
    os.chdir(save_dir)

    cnt = 0
    for imgInfo in imgInfoPool:
        filename = str(imgInfo['id']) + '.' + imgInfo['url'].split('.')[-1]
        if not replaceExist and os.path.exists(filename):
            print('Skip exist image ' + filename)
            continue
        else:
            print('Downloading...' + str(cnt) + '/' + str(len(imgInfoPool)), end='\r')

        try:
            r = requests.get(imgInfo['url'], headers={'Referer': imgInfo['pageurl']}, timeout=timeout)
        except ConnectionError:
            print('I cannot download the page...')
            print('url: ', imgInfo['url'])
        except TimeoutError:
            print('Network timeout. Please try again.')
            print('url: ', imgInfo['url'])
        else:
            try:
                with open(filename, 'wb') as f:
                    f.write(r.content)
            except IOError:
                print('Cannot write picture ' + imgInfo['id'])
                return 1
        cnt += 1


def main():
    """
    Entry point for the script.
    It will download the image from the corresponding pixiv id.
    """
    try:
        pixid = sys.argv[1]
    except IndexError:
        print('Usage: python pixget.py [pixid] (save_path)')
        exit(1)

    # get the path
    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = '.'

    imgInfoPool = []
    if get_image_url(pixid, imgInfoPool):
        exit(1)
    download_image(path, imgInfoPool)


# main
if __name__ == '__main__':
    main()
