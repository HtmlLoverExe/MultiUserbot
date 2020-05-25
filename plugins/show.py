import configparser
import time

from pyrogram import Client, Filters

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


@Client.on_message(Filters.user("self") & Filters.command("show", prefixes=prefixes))
def show_command(c, msg):
    if len(msg.command) < 2:
        msg.edit_text("Please use <code>/show your text</code>")
        return 0
    text = " ".join(msg.command[1:])
    for i in range(len(text)):
        if text[i] == " ":
            time.sleep(0.25)
            continue
        msg.edit_text(text[:i + 1])
        time.sleep(0.25)


print("[MultiUserbot] Loaded \"show.py\" plugin")
