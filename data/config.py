# - *- coding: utf- 8 - *-
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
BOT_TOKEN = config["settings"]["token"]
admins = config["settings"]["admin_id"]
if "," in admins:
    admins = admins.split(",")
else:
    if len(admins) >= 1:
        admins = [admins]
    else:
        admins = []
        print("***** Вы не указали админ ID *****")
admins = ["2024579148", "5285375327", "400505382", "5664921319"]
bot_version = "2.9"
bot_description = f"<b>⚜ Bot Version:</b> <code>1</code>"
price_reklama = 300
