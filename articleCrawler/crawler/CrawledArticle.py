import textwrap


class TagesschauTeaser:
    def __init__(self, title, top, teaser, link, dach):
        self.title = title
        self.top = top
        self.teaser = teaser
        self.link = link
        self.body = ""
        split = dach.split(" ")
        self.date=split[2]
        self.time=split[3]

    def get_full_body(self):
        return self.body

    def get_title_line(self):
        if not self.top=="":
            return self.top + " - " + self.title
        else:
            return self.title

    def print(self):
        print(self.get_title_line())
        print(self.date + " " + self.time)
        for block in self.body:
            for line in textwrap.wrap(block):
                print(line)
        print(self.link)
        print()
