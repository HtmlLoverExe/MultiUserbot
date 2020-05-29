import configparser
import time

from pyrogram import Client, Filters

config = configparser.ConfigParser()
config.read("config.ini")
prefixes = list(config["prefixes"].keys())
