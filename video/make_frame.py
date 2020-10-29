from selenium.webdriver import Chrome, ChromeOptions
import requests
from PIL import Image
from datetime import date
import base64
import uuid
import os
import time
import math
import utils.log as log

CHROME_DRIVER_PATH = '/Users/aarenstade/Documents/chromedriver'


def downloadB64Img(img, filename):
    data = str(img)[22:]
    decoded = base64.b64decode(data)
    with open(filename, 'wb') as img:
        img.write(decoded)
        img.close()


def get_images(query):
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = Chrome(
        executable_path=CHROME_DRIVER_PATH, options=options)
    url = "https://www.bing.com/images/search?q="+query
    driver.get(url)
    ActualImages = []
    images = driver.find_elements_by_class_name('mimg')
    for i in images:
        src = i.get_attribute('src')
        if(src != None):
            ActualImages.append(src)
    driver.quit()
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
        if(image != None):
            filename = path + "/" + str(uuid.uuid4()) + ".jpg"
            if(image.startswith('data')):
                downloadB64Img(image, filename)
            else:
                request = requests.get(image, stream=True)
                if not request.ok:
                    print(request)
                with open(filename, 'wb') as imgFile:
                    for block in request.iter_content(1024):
                        if not block:
                            break
                        imgFile.write(block)
                imgFile.close()


def remove_src_dir(path):
    if(os.path.exists(path)):
        os.rmdir(path)

# create video frame and paste images


def create_collage(path, query):
    final_w = 1280
    final_h = 720
    image_paths = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    imgs_w = 0
    imgs_h = 0
    # get average size of images
    for i in image_paths:
        img = Image.open(path + '/' + i)
        imgs_w = imgs_w + img.width
        imgs_h = imgs_h + img.height
        img.close()
    # define block size
    block_w = round((imgs_w / len(image_paths)))
    block_h = round((imgs_h / len(image_paths)))
    # determine number of rows of blocks
    nper_row = int(math.floor(final_w / block_w))
    nrows = int(math.ceil(len(image_paths) / nper_row))
    row_w = block_w * nper_row
    row_h = block_h
    # for first img
    # determine padding from top and left
    y_pad_start = round((final_h - (row_h * nrows)) / 2)
    x_pad_start = round((final_w - row_w) / 2)
    x_cur = x_pad_start
    y_cur = y_pad_start
    col_num = 1
    img_num = 0
    # paste images, scaled into blocks
    final_img = Image.new('RGB', (final_w, final_h))
    for i in image_paths:
        img_num = img_num + 1
        img = Image.open(path + '/' + i)
        image = img.resize((block_w, block_h))
        final_img.paste(image, box=(x_cur, y_cur))
        # move to next column
        col_num = col_num + 1
        x_cur = x_cur + block_w
        # if we've exited the image
        if(col_num > nper_row):
            col_num = 1
            y_cur = y_cur + row_h  # move down a row
            # modify x_cur for when next row < than nper_row
            imgs_left = len(image_paths) - img_num
            if(imgs_left < nper_row):
                x_cur = round((final_w - (block_w * imgs_left)) / 2)
            else:
                x_cur = x_pad_start  # go to x start
    return final_img


def CreateFrame(query, path):
    start = time.time()
    query = query.split(' ')
    query = '+'.join(query)
    images = get_images(query)
    if(len(images) > 0):
        dt = date.today().strftime("%b-%d-%Y")
        path = path + '/src/' + query + '-' + dt
        newDir = create_imgs_dir(path)
        if(newDir):
            download_images(images, path)
        img = create_collage(path, query)
        # img.save(str(query) + '.jpg')
        end = time.time()
        log.Log_Frame(query, (end - start))
        return img
    else:
        print('no images found')
        # return None
