import configparser
from datetime import datetime

from pyrogram import Client, Filters, Emoji

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())

info_message = {"id": f"{Emoji.ID_BUTTON} <b>Id</b>: <code>[%id%]</code>",
                "first_name": f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} <b>Name</b>: <code>[%first_name%]</code>",
                "last_name": f"{Emoji.BUST_IN_SILHOUETTE} <b>Last Name</b>: <code>[%last_name%]</code>",
                "username": f"{Emoji.LINK} <b>Username</b>: <code>[%username%]</code>",
                "dc_id": f"{Emoji.DESKTOP_COMPUTER} <b>Dc</b>: <code>[%dc_id%]</code>",
                "status": f"{Emoji.MOBILE_PHONE_WITH_ARROW} <b>Status</b>: <code>[%status%]</code>",
                "last_online_date": f"{Emoji.TWELVE_O_CLOCK} <b>Last Online Date</b>: "
                                    f"<code>[%last_online_date%]</code>",
                "next_offline_date": f"{Emoji.SEVEN_THIRTY} <b>Next Offline Date</b>: "
                                     f"<code>[%next_offline_date%]</code>",
                "is_bot": f"{Emoji.ROBOT_FACE} <b>Is Bot</b>: <code>[%is_bot%]</code>",
                "is_contact": f"{Emoji.TELEPHONE} <b>Is Contact</b>: <code>[%is_contact%]</code>",
                "is_mutual_contact": f"{Emoji.MOBILE_PHONE} <b>Is Mutual Contact</b>: "
                                     f"<code>[%is_mutual_contact%]</code>",
                "is_scam": f"{Emoji.CROSS_MARK} <b>Is scam</b>: <code>[%is_scam%]</code>",
                "language_code": f"[%emoji%] <b>Language</b>: <code>[%language_code%]</code>",
                "bio": f"{Emoji.TRIDENT_EMBLEM} <b>Bio</b>: <code>[%bio%]</code>"}


@Client.on_message(Filters.user("self") & Filters.command("info", prefixes=prefixes) & Filters.reply)
def info_command_reply(c, msg):
    target = msg.reply_to_message.from_user
    message = "{} Info {}\n\n".format(Emoji.INFORMATION, Emoji.INFORMATION)
    for key in info_message:
        try:
            message += info_message[key].replace(
                f"[%{key}%]", str(
                    (
                        target[key] if key != "next_offline_date" and key != "last_online_date" else (
                            datetime.fromtimestamp(int(target[key])).strftime("%H:%M:%S %d/%m/%y")
                        )
                    ) if target[key] and key!="language_code" else (
                        target["raise AttributeError()"])
                )
                ) + "\n"
        except AttributeError:
            pass
    lang_code = target.language_code
    if lang_code:
        flag = ""
        for c in lang_code:
            flag += Emoji["REGIONAL_INDICATOR_SYMBOL_LETTER_{}".format(c.upper())]
        message += info_message["language_code"].replace("[%emoji%]", flag).replace("[%language_code%]", lang_code)
    bio = c.get_chat(target.id).description
    if bio:
        message += info_message["bio"].replace("[%bio%]", c.get_chat(target.id).description)
    message += f"\n\n<a href=\"tg://user?id={target.id}\">Profile Link</a>"
    msg.edit_text(message)


print("[MultiUserbot] Loaded \"info.py\" plugin")
