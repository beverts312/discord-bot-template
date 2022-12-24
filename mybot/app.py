import logging

from discord_sls import Interaction, bot_handler, deferred_response_handler


@bot_handler
def discord_bot(command_body, send_command_to_queue):
    data = command_body.get("data", {})
    logging.info(data)
    command_name = data.get("name")
    if command_name == "hello":
        return {"content": "Hello Moto"}
    elif command_name == "helloasync":
        send_command_to_queue(command_body)
        return {"content": "Hello..."}
    else:
        logging.warn(f"unhandled command: {command_name}")
        return {"content": "Unknown Command"}


@deferred_response_handler
def long_response_handler(interaction: Interaction):
    interaction.follow_up({"content": "async"})
