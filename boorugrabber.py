#!/usr/bin/python3
import requests
import os
import argparse
import asyncio
import aiohttp
import aiofiles

class Grabber:

    booru_urls = {"danbooru": "https://danbooru.donmai.us/posts.json?tags=", "gelbooru": "https://gelbooru.com/index.php?page=dapi&s=post&json=1&q=index&tags="}

    def __init__(self, booru, tags, limit, path="", random=False):
        self.booru = self.booru_urls[booru]
        
        self.tags = "+".join(tags)
        self.path = path
        self.random = random
        
        self.limit = limit


    def __get_pages(self):
        
        req_str = self.booru + self.tags + '&random=' + str(self.random) + '&limit=' + str(self.limit)
        req = requests.get(req_str)

        return req.json()

    def get_image_urls(self):
        req = self.__get_pages()
        
        response_dict = {}
        for i in req:
            if 'file_url' in i:
                response_dict[i['id']] = i['file_url']
            else:
                print("Image "+str(i['id'])+" could not be downloaded.")
        return response_dict

    async def download(self, pid, url):
        #print ("Downloading "+str(len(image_dict)) + " images")
        #for pid, url in image_dict.items():
        print("Downloading "+str(pid))
        filetype = url.split('.')[-1]
        filename = self.path + str(pid) + "." + filetype
        async with aiohttp.ClientSession() as req:
            response = await req.get(url)
            out_file = await aiofiles.open(filename, mode='wb')
            await out_file.write(await response.read())
            await out_file.close()
        
        return True
        #print ("Downloads complete")

    async def download_all(self):
        image_dict = self.get_image_urls()
        await asyncio.gather(*[self.download(pid,url) for pid, url in image_dict.items()])

if __name__ == "__main__":
    booru_len = { "danbooru":2, "gelbooru":99 }
    parser = argparse.ArgumentParser(prog="boorugrabber", description = "Download images from a booru site")
    parser.add_argument('-b','--booru', nargs=1, help="name of booru")
    parser.add_argument('-t','--tags', nargs='+', help="List of tags")
    parser.add_argument('-l','--limit', default=20, type=int, help="Number of results wanted (default=20)")
    parser.add_argument('-p','--path', default="", help="File path for output")

    args = parser.parse_args()
    if args.limit == None:
        print("Using default value for limit (20)")
    if args.path == None:
        print("Using default value for path (cwd)")
    
    grabber = Grabber(args.booru[0], args.tags, args.limit)
    asyncio.run(grabber.download_all())
