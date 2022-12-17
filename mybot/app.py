import json
import logging

from discord_lite import BotUtils, bot_handler

logging.getLogger().setLevel(logging.INFO)


@bot_handler
def discord_bot(command_body):
    data = command_body.get("data", {})
    logging.info(data)
    command_name = data.get("name")
    if command_name == "hello":
        return {"content": "Hello Moto"}
    elif command_name == "helloasync":
        BotUtils.send_command_to_queue(command_body)
        return {"content": "Hello..."}
    else:
        logging.warn(f"unhandled command: {command_name}")
        return {"content": "Unknown Command"}


def long_response_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        BotUtils.edit_interaction(body, {"content": "Hello...async"})
