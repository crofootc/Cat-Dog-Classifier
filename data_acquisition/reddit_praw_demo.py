import praw
import urllib.request
import time
import os

PIC_EXTENSIONS = ['jpg', 'png']
VERBOSE = True


# Get credentials from DEFAULT instance in praw.ini
reddit = praw.Reddit()
print(reddit.user.me())


class SubredditPictureScraper_test:
    def __init__(self, sub, sort='new', lim=10):
        self.sub = sub
        self.sort = sort
        self.lim = lim
        print(
            f'SubredditPictureScraper instance created with values '
            f'sub = {sub}, sort = {sort}, lim = {lim}')

    def set_sort(self):
        if reddit.auth.limits['remaining'] < 5:
            print('Reached Auth Limit: Resetting')
            time.sleep(reddit.auth.limits['reset_timestamp'] - time.time())

        if self.sort == 'new':
            return self.sort, reddit.subreddit(self.sub).new(limit=self.lim)
        elif self.sort == 'top':
            return self.sort, reddit.subreddit(self.sub).top(limit=self.lim)
        elif self.sort == 'hot':
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)
        else:
            self.sort = 'hot'
            print('Sort method was not recognized, defaulting to hot.')
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)

    def get_image_urls(self):
        sort, subreddit = self.set_sort()
        urls = []
        i = 0
        for submission in subreddit:
            if reddit.auth.limits['remaining'] < 5:
                print('Reached Auth Limit: Resetting')
                time.sleep(reddit.auth.limits['reset_timestamp'] - time.time())

            if not submission.stickied:
                urls.append(submission.url)
            time.sleep(0.1)
            if i % 500 == 0:
                print(i)
            i += 1
        return urls


class UrlPictureScraper:
    def __init__(self, urls, folder="TEMP"):
        if type(urls) == type(''):
            self.urls = [urls]
        else:
            self.urls = urls

        self.folder = os.path.dirname(__file__) + "\\" + folder
        if not os.path.isdir(self.folder):
            print("MAKNG DIRECTORY: " + folder)
            os.mkdir(self.folder)

    def save_images(self):
        print("SAVING IMAGES")
        for url in urls:
            if url.rsplit('.')[-1] in PIC_EXTENSIONS:
                if VERBOSE:
                    print(url)
                if not os.path.exists(self.folder + "\\" + url.rsplit('/', 1)[-1]):
                    try:
                        urllib.request.urlretrieve(url,
                                                   self.folder + "\\" + url.rsplit('/', 1)[-1])
                    except:
                        print("BAD FILENAME")
            elif VERBOSE:
                print("BAD FILENAME")
                
                


dogs = SubredditPictureScraper_test('dogpictures', lim=24000, sort='top')
urls = dogs.get_image_urls()
print(len(urls))
pics = UrlPictureScraper(urls, 'dogs')
pics.save_images()

cats = SubredditPictureScraper_test('catpictures', lim=20000, sort='top')
urls = cats.get_image_urls()
print(len(urls))
pics = UrlPictureScraper(urls, 'cats')
pics.save_images()

cats2 = SubredditPictureScraper_test('cats', lim=5000, sort='top')
urls = cats2.get_image_urls()
print(len(urls))
pics = UrlPictureScraper(urls, 'cats')
pics.save_images()
