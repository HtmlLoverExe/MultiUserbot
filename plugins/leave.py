import configparser

from pyrogram import Client, Filters

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


@Client.on_message(Filters.user("self") & Filters.command("leave", prefixes=prefixes))
def leave_command(c, msg):
    msg.delete()
    msg.chat.leave()


print("[MultiUserbot] Loaded \"leave.py\" plugin")
