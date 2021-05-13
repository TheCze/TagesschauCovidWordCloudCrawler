import csv
from article import Article
import queue

word_filter = ['der', 'die', 'in', 'und', 'den', 'von', 'zu', 'Die', 'mit', 'das', 'für', 'auf', 'im', 'sich',
               'nicht', 'des', 'dem', 'eine', 'es', 'ist', 'werden', 'auch', 'dass', 'an', 'ein', 'als', 'sagte',
               'aus', 'sind', 'nach', 'bei', 'Das', 'einer', 'hat', 'wie', 'um', 'am', 'sei', 'mehr',
               'Der', 'vor', 'noch', 'In', 'haben', 'einem', 'bis', 'einen', 'sie', 'aber', 'wieder', 'oder', 'zum',
               'wird', 'über', 'nur', 'so', 'hatte', 'er', 'seien', 'Es', 'zur', 'wir', 'gegen', 'unter', 'worden',
               'können', 'sollen', 'Auch', 'habe', 'sein', 'müssen', 'soll', 'bereits', 'ab', 'seit', 'wurden',
               'war', 'keine', 'werde', 'alle', 'etwa', 'Wir', 'wegen', 'man', 'durch', 'wenn', 'rund', 'zwei', 'Sie',
               'gibt', 'nun', 'viele', 'weiter', 'damit', 'Nach', 'dann', 'will', 'ihre', 'kann', 'wurde',
               'vom', 'Im', 'waren', 'neue', 'jetzt', 'weitere', 'eines', 'dürfen', 'sehr', 'diese', 'teilte', 'Er',
               'schon', 'vergangenen', 'hatten', 'würden', 'anderen', 'sagt', 'ersten', 'könnten', 'Für', 'derzeit',
               'hätten', 'sowie', 'Tagen', 'muss', 'könne', 'Ein', 'dieser', 'zufolge', 'bleiben', 'deutlich', 'Eine',
               'müsse', 'immer', 'gilt', 'möglich', 'geht', 'laut', 'Bei', 'diesem', 'drei', 'andere', 'allem', 'ohne',
               'sollten', 'heute', 'Mit', 'geben', 'seine', 'Und', 'Aber']


def get_words(text):
    to_replace = [",", ".", "?", ";", ":", "'", '"', "(", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for char in to_replace:
        text = text.replace(char, "")
    words = text.split(" ")
    for w in words:
        if len(w) <= 1:
            words.remove(w)
        w = w.strip()
    return words


def load_articles(filename):
    loaded_articles = []
    with open(filename, 'r', newline='', encoding='utf-8') as csv_file:
        article_reader = csv.reader(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in article_reader:
            if row[4] == "":
                continue
            art = Article(row[0], row[1], row[4])
            loaded_articles.append(art)
    print("Loaded " + str(len(loaded_articles)) + " articles")
    return loaded_articles


def filter_words(to_filter):
    print("Filtering words from size : " + str(len(to_filter)))
    for f in word_filter:
        if f in to_filter:
            del to_filter[f]
    return to_filter


def count_single_words(to_count):
    print("Counting single words")
    word_counter = {}
    for c in to_count:
        if c in word_counter:
            word_counter[c] = word_counter[c] + 1
        else:
            word_counter[c] = 1
    print("Found a total of " + str(len(word_counter)) + " words")
    return word_counter


def delete_low_occurs(to_search, min_occurs):
    print("Deleting Low occurrences, Word count before: " + str(len(to_search)))
    to_del = []
    for wc in to_search:
        if to_search[wc] < min_occurs:
            to_del.append(wc)
    for delete in to_del:
        del to_search[delete]
    print("Deleted " + str(len(to_del)) + " words appearing less then " + str(min_occurs) + " times")
    return to_search


def sort_words(words):
    sorted_list = {}
    print("Sorting " + str(len(words)) + " words")
    while len(words) > 0:
        max_amount = 0
        max_word = ""
        for w in words:
            if words[w] > max_amount:
                max_amount = words[w]
                max_word = w
        del words[max_word]
        sorted_list[max_word] = max_amount
    print("Finished sorting!")
    return sorted_list


def show_top(to_chart, max_charts):
    n = 0
    print()
    print("TOP " + str(max_charts))
    charts = []
    for top in to_chart:
        print(str(n + 1) + ": " + top + " (" + str(to_chart[top]) + ")")
        charts.append((top, to_chart[top]))
        n += 1
        if n >= max_charts:
            break
    return charts


def p_queue_sort(unsorted_list):
    q = queue.PriorityQueue()
    for key, num in unsorted_list.items():
        q.put((-num, key))
    sorted = {}
    while not q.empty():
        w_tuple = q.get()
        sorted[w_tuple[1]] = -w_tuple[0]
    return sorted


# PROGRAM START
articles = load_articles()
word_list = []
for article in articles:
    word_list += get_words(article.get_full_text())
counted_words = count_single_words(word_list)
filtered_words = filter_words(counted_words)
sorted_words = p_queue_sort(filtered_words)
charted = show_top(sorted_words, 1000)
print(len(charted))
print("Saving")
with open("word_stats.csv", "w", encoding="utf-8") as file:
    for t in charted:
        file.write(str(t[0]) + ":" + str(t[1]) + "\n")
print("Done")
