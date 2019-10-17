#!/usr/bin/python3
import requests
import os
import argparse
import shutil

danbooru = "http://danbooru.donmai.us"
stringlist = []
urlsToEnter = []
flags = {'arg':False,'verbose':False}

out_folder="Pictures/"

class Grabber:

    booru_urls = {"danbooru": "https://danbooru.donmai.us/", "gelbooru": "https://gelbooru.com"}

    def __init__(self, booru, tags, limit, path=""):
        self.booru = self.booru_urls[booru]
        
        self.tags = "+".join(tags)
        self.path = path
        
        self.limit = limit


    def __get_pages(self):
        
        req_str = self.booru + 'posts.json?tags='+ self.tags + '&limit=' + str(self.limit)
        req = requests.get(req_str)

        return req.json()

    def get_image_urls(self):
        req = self.__get_pages()
        
        response_dict = {}
        for i in req:
            response_dict[i['id']] = i['file_url']
        return response_dict

    def download(self):
        image_dict = self.get_image_urls()
        print ("Downloading "+str(len(image_dict)) + " images")
        for pid, url in image_dict.items():
            filetype = url.split('.')[-1]
            filename = self.path + str(pid) + "." + filetype
            response = requests.get(url)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

        print ("Downloads complete")

        

if __name__ == "__main__":
    booru_len = { "danbooru":2, "gelbooru":99 }
    parser = argparse.ArgumentParser(prog="boorugrabber", description = "Download images from a booru site")
    parser.add_argument('-b','--booru', help="name of booru")
    parser.add_argument('-l','--limit', default=20, type=int, help="Number of results wanted (default=20)")
    parser.add_argument('-t','--tags', nargs='+', help="List of tags")

    args = parser.parse_args()
    if args.booru not in booru_len.keys():
        print("Argument booru not found, exiting")
        exit()
    
    if args.limit == None:
        print("Using default value for limit (20)")
    

    grabber = Grabber(args.booru, args.tags, args.limit)
    grabber.download()
