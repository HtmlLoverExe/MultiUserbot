import sys

if sys.version_info.minor < 7:
    print("You should use python 3.7 or higher.\n")

from pyrogram import Client

bot = Client(
    "MultiUserbot",
    config_file="config.ini")


bot.start()
