import configparser

from pyrogram import Client, Filters

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


@Client.on_message(Filters.reply & Filters.user("self") & Filters.command("save", prefixes=prefixes))
def save_command(c, msg):
    msg.reply_to_message.forward("self")
    msg.delete()


print("[MultiUserbot] Loaded \"save.py\" plugin")

