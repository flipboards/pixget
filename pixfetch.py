# fetch image urls with corresponding tag.


import pixget
import requests
import bs4

operate_url = pixget.root_url + '/search.php'
ImageInfo = {}


def search_one_page(tag, page_index):
    PageParams = dict(word=tag, p=page_index)
    try:
        r = requests.get(operate_url, params=PageParams, cookies=pixget.mycookies)
    except:
        print('Sorry, search page cannot be opened')
        return
    Page = r.text.encode('utf-8')
    soup = bs4.BeautifulSoup(Page, 'html.parser')
    for ImgItem in soup.find_all('li', class_='image-item'):  # find image boxes
        ImgIndex = int(ImgItem.contents[0].attrs.get('href').split('=')[-1])  # image index
        print(ImgIndex)
        ImgUrl = ImgItem.find('img').attrs.get('src')
        ImgTitle = ImgItem.contents[1].text
        ImgAuthor = int(ImgItem.contents[2].attrs.get('data-user_id'))
        ImgCollection = int(ImgItem.contents[3].find('a').text)
        ImageInfo[ImgIndex] = dict(ImgUrl=ImgUrl, ImgTitle=ImgTitle, ImgAuthor=ImgAuthor, ImgCollection=ImgCollection)


def write_data(filename):
    f = open(filename, 'w')
    f.write('PixId,Title,Collection,Author\n')
    for (ImgIndex, ImgData) in ImageInfo.items():
        f.write(str(ImgIndex) + ',' + ImgData['ImgTitle'] + ',' + str(ImgData['ImgCollection']) + ',' + str(
            ImgData['ImgAuthor']) + '\n')
    f.close()


if __name__ == '__main__':
    search_one_page('風景1000users', 1)
    write_data('./pics' + 'imgs.csv')
