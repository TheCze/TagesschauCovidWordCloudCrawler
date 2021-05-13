import crawler
import time
import csv
articles = []

def fetch_articles():
    print("Starting fetching")
    fetcher = crawler.ArticleFetcher()
    for element in fetcher.fetch_teasers():
        time.sleep(1.0)
        fetcher.fetch_text(element)
        print("Loaded: " + element.date + ": " + element.get_title_line())
        articles.append(element)
    print("Finished loading " + str(len(articles)) + " Articles")
    unloaded = ""

    for a in articles:
        if len(a.body) == 0:
            unloaded += a.get_title_line() + "; "

    if len(unloaded) > 0:
        print("Could not load body for Articles: " + unloaded)


def save_articles():
    with open('articles.csv', 'w', newline='', encoding='utf-8') as csv_file:
        article_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for article in articles:
            article_writer.writerow([article.get_title_line(), article.date, article.time, article.link, article.body])
    print("Finished Creating .csv")


def load_articles(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as csv_file:
        article_reader = csv.reader(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in article_reader:
            print(row[1])
            break
    print("Finished Loading .csv")