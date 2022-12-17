import logging
import sys

from bot_utils import (
    COMMAND_OPTION_TYPES,
    BotArg,
    BotCommand,
    BotInfo,
    DiscordClient,
    select_item,
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

try:
    bot_info = BotInfo.load_from_file()
    discord_client = DiscordClient(bot_info.app_id)
except Exception as e:
    logging.error(e)
    exit(1)

name = input("Command Name: ")
description = input("Command Description: ")
command = BotCommand(name=name, description=description, type=1, arguements=[])

has_args_input = input("Does your command take arguements? (y/N) ")
has_args = has_args_input.lower() == "y"
while has_args:
    arg_name = input("Arguement Name: ")
    arg_description = input("Arguement Description: ")
    arg_type = select_item(
        COMMAND_OPTION_TYPES, "Arguement Type: ", "name", "value"
    )
    command.arguements.append(
        BotArg(name=arg_name, description=arg_description, type=arg_type)
    )
    has_more_args_input = input("Do you have more arguements to add? (y/N) ")
    has_args = has_more_args_input.lower() == "y"

res = discord_client.crupdate_command(command)
logging.info(f"Registed command with id {res['id']}")
command.id = res["id"]
bot_info.commands.append(command)
bot_info.crupdate_info_file()
logging.info("Updated bot_info.yml")
