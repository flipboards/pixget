# this file contains basic information about downloading pictures.


import requests
import sys
import bs4
import re

root_url = 'http://www.pixiv.net'
operate_url = root_url + '/member_illust.php'

# url = http://i3.pixiv.net/img-original/img/2016/06/18/23/53/59/_p0.jpg

# cookies
mycookies = dict(PHPSESSID='18002369_151fa062b11bd07f9e802879a8144dbb',
                 __utmz='235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=18002369=1',
                 __ga='GA1.2.897318290.1470488357', manga_viewer_expanded='1',
                 module_orders_mypage='%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D',
                 p_ab_id='7')


# only used in debug
def save_webpage(Page):
    open('result.html', 'wb').write(Page)


# download an image in multiple images
def get_image_url2(pixid, index, imgInfoPool):
    PageParams = dict(mode='manga_big', illust_id=pixid, page=index)
    try:
        r = requests.get(operate_url, params=PageParams, cookies=mycookies)
    except:
        print('I cannot open the page. Maybe the id is invalid?')
        return 1
    soup = bs4.BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
    img = soup.find('img')
    imgName = soup.find('title').string
    print('Name: ' + imgName)
    imgInfoPool.append(dict(id=pixid + '_p' + str(index), name=imgName, url=img.attrs.get('src'), pageurl=r.url))
    return 0


# return the image url
def get_image_url(pixid, imgInfoPool):
    # open the page
    PageParams = {'mode': 'medium', 'illust_id': pixid}
    try:
        r = requests.get(operate_url, params=PageParams, cookies=mycookies)
    except:
        print('I cannot open the page. Maybe the id is invalid?')
        return 1
    # print(r.url)

    soup = bs4.BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
    img = soup.find('img', class_='original-image')
    if not img:     # multiple images
        # open the page
        PageParams = {'mode': 'manga', 'illust_id': pixid}
        try:
            r = requests.get(operate_url, params=PageParams, cookies=mycookies)
        except:
            print('I cannot open the page. Maybe the id is invalid?')
            return 1

        soup = bs4.BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
        imgNumber = len(soup.find_all('div', class_='item-container'))

        if imgNumber == 0:
            print('Cannot find pictures in the page. Please try again?')
            print('Url is ' + r.url)
            return
        imgIndex = input('Illustration ' + str(pixid) + ' has ' + str(imgNumber) + ' pictures. Download all (a) or index: (number)')

        if imgIndex == 'a': # a stands for all
            for i in range(0, imgNumber):
                print('Getting image ', i)
                if get_image_url2(pixid, i, imgInfoPool):
                    return 1
            return 0
        else:
            if get_image_url2(pixid, int(imgIndex), imgInfoPool):
                return 0

    else:       # one image
        imgName = img.attrs.get('alt')
        print('name: ' + imgName)
        imgInfoPool.append(dict(id=pixid, name=imgName, url=img.attrs.get('data-src'), pageurl=r.url))  # put into pool
        return 0


# download a url
def download_image(save_dir, imgInfoPool):
    for imgInfo in imgInfoPool:
        print('url: ', imgInfo['url'])
        try:
            r = requests.get(imgInfo['url'], headers={'Referer': imgInfo['pageurl']})
        except:
            print('I cannot download the page...')
        f = open(save_dir + str(imgInfo['id']) + '.' + imgInfo['url'].split('.')[-1], 'wb')
        f.write(r.content)
        f.close()


# main
if __name__ == '__main__':
    pixid = sys.argv[1]
    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = '.'
    imgInfoPool = []
    if get_image_url(pixid, imgInfoPool):
        exit(1)
    download_image(path, imgInfoPool)
