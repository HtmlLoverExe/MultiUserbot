import configparser

import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters, Emoji

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


def extracturls(msg):
    if not msg.entities:
        if msg.caption_entites:
            entites = msg.caption_entities
            text = msg.caption
        else:
            return []
    else:
        entites = msg.entities
        text = msg.text
    results = []
    for e in entites:
        if e.type == "text_link":
            results.append(e.url)
        elif e.type == "url":
            results.append(text[e.offset:e.offset + e.length])
    return results


def tinyurl(url, alias=""):
    e = BeautifulSoup(
        requests.get("https://tinyurl.com/create.php",
                     params={
                         "url": url,
                         "alias": alias
                     }).text,
        "lxml"
    ).select("div.indent:nth-child(4) > b:nth-child(1)")
    if len(e) >= 1:
        return e[0].text
    else:
        print(f"Retrying url {url[:25]}")
        return tinyurl(url, alias)
#Filters.user("self") &

@Client.on_message(Filters.reply & Filters.command("short", prefixes=prefixes))
def short_command(c, msg):
    msg.edit_text("Shortening...")
    c.send_chat_action(msg.chat.id, "typing")
    urls = extracturls(msg.reply_to_message)
    message = f"{Emoji.LINK} Shortener {Emoji.LINK}\n\n{Emoji.GLOBE_WITH_MERIDIANS} Results:\n"
    for u in urls:
        if u.startswith("http"):
            message += f"{Emoji.HEAVY_MINUS_SIGN} {u[:25]}\n" \
                       f"{Emoji.WHITE_HEAVY_CHECK_MARK} {tinyurl(u)}\n"
    msg.edit_text(message,
                  disable_web_page_preview=True)


print("[MultiUserbot] Loaded \"short.py\" plugin")
