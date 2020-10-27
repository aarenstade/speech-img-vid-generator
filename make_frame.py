from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from PIL import Image
from datetime import date
import uuid
import os

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

# get images from bing based on query


def get_images(query):
    url = "https://www.bing.com/images/search?q="+query
    request = Request(url, headers=header)
    soup = BeautifulSoup(urlopen(request), 'html.parser')

    ActualImages = []
    for a in soup.find_all('div', {'class': 'img_cont hoff'}):
        src = a.find('img').get('src')
        b64 = str(src).startswith('data')
        if(b64 == False):
            if(src != None):
                ActualImages.append(str(src))
    return ActualImages


def create_imgs_dir(path):
    if not (os.path.exists(path)):
        os.makedirs(path)
        return True
    else:
        return False

# download list of image urls


def download_images(images, path):
    for image in images:
        request = requests.get(image, stream=True)
        filename = "/" + str(uuid.uuid4()) + ".jpg"
        if not request.ok:
            print(request)
        with open(path + filename, 'wb') as imgFile:
            for block in request.iter_content(1024):
                if not block:
                    break
                imgFile.write(block)


def remove_src_dir(path):
    if(os.path.exists(path)):
        os.rmdir(path)

# create video frame and paste images


def create_collage(path, query):
    final_h = 720
    final_w = 1280
    image_paths = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    images = []
    imgs_w = 0
    for img in image_paths:
        full_path = path + '/' + img
        img = Image.open(full_path)
        images.append(img)
        imgs_w = imgs_w + img.width
    padding = 0
    if(imgs_w < final_w):
        padding = round((final_w - imgs_w) / 2)
    cur_x = padding
    final_img = Image.new('RGB', (final_w, final_h))
    for i in images:
        y_pos = round((final_h - i.height) / 2)
        final_img.paste(i, box=(cur_x, y_pos))
        cur_x = cur_x + i.width
    return final_img


def CreateFrame(query):
    query = query.split(' ')
    query = '+'.join(query)
    images = get_images(query)
    if(len(images) > 0):
        dt = date.today().strftime("%b-%d-%Y")
        path = './src/' + query + '-' + dt
        hasImages = create_imgs_dir(path)
        if(hasImages):
            download_images(images, path)
        img = create_collage(path, query)
        return img
    else:
        print('no images found')
        return None
