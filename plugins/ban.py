import configparser
import time

from pyrogram import Client, Filters, Emoji

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())

banned = Filters.user()
to_delete = {}
last_msg = {}


@Client.on_message(Filters.private & banned & ~Filters.user("self"), group=-1)
def delete_banned(c, msg):
    if msg.chat.id not in to_delete:
        to_delete[msg.chat.id] = []
    if msg.chat.id not in last_msg:
        last_msg[msg.chat.id] = int(time.time())
        msg.delete()
        return 0
    if last_msg[msg.chat.id] + 1 >= int(time.time()):
        c.read_history(msg.chat.id)
        to_delete[msg.chat.id].append(msg.message_id)
    else:
        last_msg[msg.chat.id] = int(time.time())
        to_delete[msg.chat.id].append(msg.message_id)
        c.delete_messages(msg.chat.id, to_delete[msg.chat.id])  # revoke = True by default
        to_delete[msg.chat.id] = []


@Client.on_message(Filters.private & Filters.user("self") & Filters.command("ban", prefixes=prefixes))
def ban_command_private(c, msg):
    banned.add(msg.chat.id)
    msg.edit_text("{} Banned {}".format(Emoji.NO_ENTRY, msg.chat.id))


@Client.on_message(Filters.private & Filters.user("self") & Filters.command("unban", prefixes=prefixes))
def unban_command_private(c, msg):
    banned.remove(msg.chat.id)
    msg.edit_text("{} Unbanned {}".format(Emoji.HEAVY_CHECK_MARK, msg.chat.id))


@Client.on_message(Filters.group & Filters.user("self") & Filters.command("ban", prefixes=prefixes))
def ban_command_group(c, msg):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user.id
    elif len(msg.command) >= 2:
        target = msg.command[1]
    else:
        msg.edit_text("Please use <code>/ban User</code> or reply to a message.")
        return 0
    if c.get_chat_member(msg.chat.id, "self").status == "creator" or c.get_chat_member(msg.chat.id,
                                                                                       "self").can_restrict_members:
        try:
            c.kick_chat_member(msg.chat.id, target)
        except Exception as e:
            msg.edit_text(str(e))
        else:
            msg.edit_text("{} Banned {}".format(Emoji.NO_ENTRY, target))
    else:
        msg.edit_text("Not enough permissions.")


@Client.on_message(Filters.group & Filters.user("self") & Filters.command("unban", prefixes=prefixes))
def unban_command_group(c, msg):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user.id
    elif len(msg.command) >= 2:
        target = msg.command[1]
    else:
        msg.edit_text("Please use <code>/unban User</code> or reply to a message.")
        return 0
    if c.get_chat_member(msg.chat.id, "self").status == "creator" or c.get_chat_member(msg.chat.id,
                                                                                       "self").can_restrict_members:
        try:
            c.unban_chat_member(msg.chat.id, target)
        except Exception as e:
            msg.edit_text(str(e))
        else:
            msg.edit_text("{} Unbanned {}".format(Emoji.HEAVY_CHECK_MARK, target))
    else:
        msg.edit_text("Not enough permissions")


print("[MultiUserbot] Loaded \"ban.py\" plugin")
