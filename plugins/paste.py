import configparser

import requests
from pyrogram import Client, Filters, Emoji

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


class DelDog:
    def __init__(self):
        self.__author__ = "GodSaveTheDoge"
        self.url = "https://del.dog/documents?frontend=true"
        self.headers = {
            "User-Agent": "Opera/8.71 (Windows CE; en-US) Presto/2.9.167 Version/11.00",
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "close",
            "Host": "del.dog"
        }

    def paste(self, text, slug=""):
        return "https://del.dog/{}".format(requests.post(
            self.url,
            headers=self.headers,
            data=('{"content":"' + text + '", "slug":"' + slug + '"}').encode("utf-8")
        ).json()["key"])


DelDog = DelDog()


@Client.on_message(Filters.user("self") & Filters.command("paste", prefixes=prefixes) & Filters.reply)
def paste_command(c, msg):
    msg.edit_text("Pasting...")
    if not msg.reply_to_message.text:
        if msg.reply_to_message.caption:
            text = msg.reply_to_message.caption
        else:
            msg.edit_text("Please reply to a message with some text")
            return 0
    else:
        text = msg.reply_to_message.text
    msg.edit_text(f"{Emoji.GLOBE_WITH_MERIDIANS} Paste {Emoji.GLOBE_WITH_MERIDIANS}\n"
                  f"\n"
                  f"{Emoji.LINK} Url: {DelDog.paste(text)}\n"
                  f"{Emoji.INPUT_LATIN_UPPERCASE} Text: {text[0:100]}...\n"
                  f"\n",
                  disable_web_page_preview=True
                  )


print("[MultiUserbot] Loaded \"paste.py\" plugin")
