# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 16:15:50 2020

@author: Cody Crofoot
"""

import urllib.request
import os
import math
import json
import requests
import time
from datetime import datetime, timedelta

class SubredditPictureScraper:
        def __init__(self, sub, days=10):
            self.sub = sub
            self.days = days
            self.urls = []
            self.PIC_EXTENSIONS = ['jpg', 'png']

            print(
                f'SubredditPictureScraper instance created with values: sub = {sub} and days = {days}')
        
        def update_image_urls(self):
                    
            def make_request(uri, max_retries = 5):
                def fire_away(uri):
                    response = requests.get(uri)
                    assert response.status_code == 200
                    return json.loads(response.content)

                current_tries = 1
                while current_tries < max_retries:
                    try:
                        time.sleep(1)
                        response = fire_away(uri)
                        return response
                    except:
                        time.sleep(1)
                        current_tries += 1
                return fire_away(uri)
            
            def pull_posts_for(subreddit, start_at, end_at):
    
                def map_posts(posts):
                    return list(map(lambda post: {
                        'url': post['url'],
                        'created_utc': post['created_utc'],
                        'prefix': 't4_'
                    }, posts))

                SIZE = 500
                URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?subreddit={}&after={}&before={}&size={}'

                post_collections = map_posts( \
                    make_request( \
                        URI_TEMPLATE.format( \
                            subreddit, start_at, end_at, SIZE))['data'])
                n = len(post_collections)
                while n == SIZE:
                    last = post_collections[-1]
                    new_start_at = last['created_utc'] - (10)

                    more_posts = map_posts( \
                        make_request( \
                            URI_TEMPLATE.format( \
                                subreddit, new_start_at, end_at, SIZE))['data'])

                    n = len(more_posts)
                    post_collections.extend(more_posts)
                return post_collections
            
            print(f"Pulling all urls for last {self.days} days")
            
            subreddit = self.sub
            end_at = math.ceil(datetime.utcnow().timestamp())
            start_at = math.floor((datetime.utcnow() - timedelta(days=self.days)).timestamp())
            posts = pull_posts_for(subreddit, start_at, end_at)
            
            for post in posts:
                if post['url'].rsplit('.')[-1] in self.PIC_EXTENSIONS and post['url'] not in self.urls:
                    self.urls.append(post['url'])

            print(f"urls contains {len(self.urls)} different urls")
            
        def get_urls(self):
            return self.urls
        
        def save_images(self, foldername="TEMP", verbose=False, image_limit=10):
            print(f"Saving max of {image_limit} images from urls")
            folder = os.path.dirname(__file__) + "\\" + foldername
            count = 0            
            
            if not os.path.isdir(folder):
                print("MAKNG DIRECTORY: " + folder)
                os.mkdir(folder)
                
            print("SAVING IMAGES")
            for url in self.urls:
                if count == image_limit:
                    break                
                
                if url.rsplit('.')[-1] in self.PIC_EXTENSIONS:
                    if verbose:
                        print(url)
                    if not os.path.exists(folder + "\\" + url.rsplit('/', 1)[-1]):
                        try:
                            urllib.request.urlretrieve(url,
                                                       folder + "\\" + url.rsplit('/', 1)[-1])
                        except:
                            print("BAD FILENAME")
                elif verbose:
                    print("BAD FILENAME")
                    
                count += 1
            
            print(f"Processed {count} images")

        def save_url(self, name="url.txt"):
            with open(name, 'w') as f:
                for url in self.urls:
                    f.write("%s\n" % url)

            
#if __name__ == "__main__": 
#    print("Not intended to be a standalone module")


"""
SOURCES: https://medium.com/@pasdan/how-to-scrap-reddit-using-pushshift-io-via-python-a3ebcc9b83f4
https://pushshift.io/api-parameters/
"""
            
            
