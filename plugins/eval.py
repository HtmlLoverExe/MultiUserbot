import configparser
import sys
import traceback

from pyrogram import Client, Filters

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())


@Client.on_message(Filters.user("self") & Filters.command("eval", prefixes=prefixes))
def eval_command(c, msg):
    if len(msg.command) < 2:
        msg.edit_text("Please use: <code>/eval msg.reply(some python code)</code>\nNote: Client = c, Message = msg")
        return 0
    null = None
    code = " ".join(msg.command[1:])
    try:
        result = eval(code)
    except Exception as e:
        result = "".join(traceback.format_exception(e, e,sys.exc_info()[2]))
    try:
        msg.edit_text("<b>Code:</b>\n<code>{}</code>\n\n<b>Result:</b>\n<code>{}</code>".format(str(code)[:1000], str(result)[:2000]))
    except Exception as e:
        msg.edit_text(str(e))


print("[MultiUserbot] Loaded \"eval.py\" plugin")
