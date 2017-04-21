import re
import requests
import time
import sys
from random import randint
from urlparse import urlparse
 
headers = {"Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8"}
 
startingURLs = ["http://weheartit.com/inspirations/fashion", 
                "http://www.imdb.com/",
                "http://www.espn.com/",
                "http://abcnews.go.com",
                "http://www.eonline.com/",
                "http://fandom.wikia.com/",
                "http://www.breitbart.com/",
                "http://www.motherjones.com/", 
                "http://talkingcomicbooks.com/",
                "http://www.independent.co.uk/us",
                "http://www.wikihow.com/Main-Page",
                "https://www.google.com/search?q=beyonce"]
 
def getNextURL(session, url):
    responseText = requests.get(url, headers=headers, timeout=5).text
    allHrefs = re.findall(r'(href="(\w|:|\/|\.|\?|\=|\&|\;)+")',responseText)
    hrefText = str(allHrefs[randint(0,len(allHrefs))][0])
    if 'http' not in hrefText: 
        if '//' not in hrefText: 
            # 'href="/questions/tagged/angularjs"'
            parsed_uri = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            return session, domain + hrefText[7:len(hrefText)-1]
        else:
            # 'href="//philosophy.stackexchange.com"'
            return session, "http://" + hrefText[8:len(hrefText)-1]
    else:
        # 'href="http://www.espn.com/"'
        return session, hrefText[6:(len(hrefText)-1)]
 
def main(startIndex):
    urlIndex = int(startIndex)
    browsingSession = requests.Session()
    try:
        while (True):
            lastGoodUrl = startingURLs[urlIndex]
            url = lastGoodUrl
            urlIndex = randint(0, len(startingURLs)-1)
            for x in xrange(randint(0, 50)):
                try:
                    print(time.strftime("%c") + ": Going to: " + url)
                    browsingSession, url = getNextURL(browsingSession, url)
                    lastGoodUrl = url
                    waitTime = randint(2,60)
                    print("Waiting " + str(waitTime) + " seconds")
                    time.sleep(waitTime)
                except:
                    browsingSession, url = getNextURL(browsingSession, lastGoodUrl)
    except:
        print("-------------Starting Again----------------")
        main(randint(0, len(startingURLs)-1))   
 
if __name__ == '__main__':
    print("-------------Starting FogOfWeb----------------")
    main(sys.argv[1])