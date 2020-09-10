import re,os,urllib.request,sys,time
import concurrent.futures
import requests as rq
from tqdm import tqdm
import configparser
from configparser import ConfigParser
import json


#all config related stuff
file = 'config.ini'
config = ConfigParser()
config.read(file)
USERAGENT = config['config']['useragent']
USER = config['config']['username']
API = config['config']['apikey']
tag_name = input('Tag?: ')
tag = config['tags'][f'{tag_name}']
tag =tag.split(',')
tags = '+'.join(tag)

pages = int(input('how many pages: '))
folder = tag_name
save_path= f'\\{folder}\\'

exts = re.compile("\/*.(jpg|gif|png|mp4|webm)$")
try:
    with open('md5.txt','r') as d:
        md5_file = d.read()
        md5_file = md5_file.split("\n")
        md5_file = list(filter(None, md5_file))
except:
    md5_file = []
urls = []

md5_list=[]
headers = {
    'User-Agent' : USERAGENT,
    'login' : USER,
    'api-key':API,
}
files=[]
if not os.path.exists(folder):
    os.mkdir(folder)


def get_urls():
    for page in range(pages):
        page = page+1
        load = rq.get(f'https://e621.net/posts.json/?page={page}&tags={tags}&limit=10000', headers=headers).json()
        e621 = load['posts']
        for  post in tqdm(e621):
            if 'file' in post:
                if post not in files:
                    files.append(post['file'])
                    time.sleep(.02)




def download_yiff(files):
        md5 = files['md5']
        urls = files['url']
        md5_list.append(md5)
        if md5 not in md5_file:
            extss = exts
            fext = extss.findall(urls)[0]
            isMatch = len(exts.findall((urls))) > 0
            if isMatch:
                download_image = rq.get((urls),stream = True).content
                rootpath = os.path.dirname(sys.argv[0])
                file_name = f"{rootpath}{save_path}{md5}.{fext}"
                with open(file_name, 'wb+') as f:
                    f.write(download_image)

# This is used to stop the downloading of the same images over and over again.
def md5_txt(md5s):
     with open('md5.txt','a') as w:
        for md5 in md5_list:
            if md5 not in md5_file:
                w.write(md5+'\n')

def main():
    get_urls()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_yiff, files)
    md5_txt(md5_list)

if __name__ == '__main__':
    main()
