import configparser

import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


class Wikipedia:
    def __init__(self):
        self.__author__ = "GodSaveTheDoge"
        self.selector = "#mw-content-text li , p" # ".mw-parser-output > p"
        self.url = "https://{}.wikipedia.org/wiki/{}"
        self.apiurl = "https://en.wikipedia.org/w/api.php?action=query&titles={}&format=json"

    def exists(self, page):
        if "-1" in requests.get(self.apiurl.format(page)).json(
        )["query"]["pages"]:
            return False
        return True

    def getpage(self, page, limit=5, lang="en"):
        tags = BeautifulSoup(requests.get(self.url.format(lang, page)).text, "lxml").select(self.selector)
        res = ""
        for i in range(limit):
            res += tags[i].text + "\n\n"
        return res


wiki = Wikipedia()


@Client.on_message(Filters.user("self") & Filters.command("wikipedia", prefixes=prefixes))
def wikipedia_command(c, msg):
    if len(msg.command) < 2:
        msg.edit_text("Please use <code>/wikipedia Doge</code>")
        return 0
    elif len(msg.command) > 2:
        page = "_".join(msg.command[1:])
    else:
        page = msg.command[1]

    if wiki.exists(page):
        text = wiki.getpage(page)
        if text:
            msg.edit_text(text)
        else:
            msg.edit_text("Could not get the page <code>{}</code>".format(page))
    else:
        msg.edit_text("The page <code>{}</code> does not exist.".format(page))


print("[MultiUserbot] Loaded \"wikipedia.py\" plugin")
