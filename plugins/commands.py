from pyrogram import Client, Filters
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


@Client.on_message(Filters.user("self") & Filters.command("commands", prefixes=prefixes))
def commands_command(c, msg):
    msg.edit_text(f"Avaiable Commands:\n"
                  f"To Do\n"
                  f"\n"
                  f"Prefixes: {' '.join(prefixes)}")

print("[MultiUserbot] Loaded \"commands.py\" plugin")