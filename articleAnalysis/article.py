class Article:
    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content

    def get_full_text(self):
        return self.title + " " + self.content
