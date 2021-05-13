import requests
from .CrawledArticle import TagesschauTeaser
from bs4 import BeautifulSoup
from urllib import parse
import time

class ArticleFetcher:

    def fetch_teasers(self):
        number = 357
        baseurl = "https://www.tagesschau.de/thema/coronavirus/index~_p-1.html?page_number="
        while number > 0:
            time.sleep(0)
            try:
                r = requests.get(baseurl + str(number))
                doc = BeautifulSoup(r.text, "html.parser")
                print("Loading page " + str(number))
            except requests.ConnectionError as exception:
                print("URL not found: " + baseurl + str(number) + str(exception))
                return
            for teaser in doc.select(".teaser"):
                dachzeile = teaser.select_one(".dachzeile")
                head = teaser.select_one(".headline")
                top = ""
                content = teaser.select_one(".teasertext")
                href_tags = teaser.find_all(href=True)
                link=href_tags[0].attrs["href"]
                link = parse.urljoin("http://www.tagesschau.de" , link)
                if head and content and link:
                    head = head.text.strip()
                    content = content.text.strip()
                    link = link.strip()
                    dachzeile = dachzeile.text.strip()
                    article = TagesschauTeaser(head, top, content, link, dachzeile)
                    yield article

            number -= 1

    def fetch_text(self, teaser):
        if teaser.link[0] == "/":
            return
        try:
            r = requests.get(teaser.link)
            doc = BeautifulSoup(r.text, "html.parser")
        except requests.ConnectionError as exception:
            print("URL not found: " + teaser.link + str(exception))
            return

        for element in doc.select(".textabsatz"):
            text = element.text.strip()
            teaser.body+=text+" "

