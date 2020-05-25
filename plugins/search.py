import configparser
import urllib.parse

import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters, Emoji

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


class Bing:
    def __init__(self, useragent=b'\xf0\x9f\xa5\x94'.decode("utf-8")):
        self.__author__ = "GodSaveTheDoge"
        self.selector = ".b_algo h2 a"
        self.url = "https://www.bing.com/search?q={}&form=QBLH"
        self.headers = {
            "IAmAPotato": "Yes".encode("utf-8"),
            "User-Agent": useragent.encode("utf-8")
        }

    def search(self, keyword):
        tags = BeautifulSoup(requests.get(
            self.url.format(urllib.parse.quote(keyword)),
            headers=self.headers,
            ).text, "lxml").select(self.selector)
        results = []
        for t in tags:
            results.append((
                t.get_attribute_list("href")[0],
                t.text
            ))
        return results


Bing = Bing()


@Client.on_message(Filters.command("search", prefixes=prefixes))
def search_command(c, msg):
    msg.edit_text("Searching...")
    if len(msg.command) < 2:
        msg.edit_text("Please use <code>/search Your Keywords</code>")
        return 0
    results = Bing.search(" ".join(msg.command[1:]))
    if results:
        message = "{} Search {}\n\n".format(Emoji.GLOBE_WITH_MERIDIANS, Emoji.GLOBE_WITH_MERIDIANS)
        for r in results:
            message += f"{Emoji.HEAVY_MINUS_SIGN} <a href=\"{r[0]}\">{r[1]}</a>\n"
        msg.edit_text(message, disable_web_page_preview=True)
    else:
        msg.edit_text("Nothing Found")


print("[MultiUserbot] Loaded \"search.py\" plugin")
