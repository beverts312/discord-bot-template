import logging
import os

import requests

from .bot_info import BotCommand

DISCORD_BASE_URL = "https://discord.com/api/v10"
DISCORD_TOKEN_KEY = "DISCORD_TOKEN"
COMMAND_OPTION_TYPES = [
    {"name": "SUB_COMMAND", "value": 1},
    {"name": "SUB_COMMAND_GROUP", "value": 2},
    {"name": "STRING", "value": 3},
    {"name": "INTEGER", "value": 4},
    {"name": "BOOLEAN", "value": 5},
    {"name": "USER", "value": 6},
    {"name": "CHANNEL", "value": 7},
    {"name": "ROLE", "value": 8},
    {"name": "MENTIONABLE", "value": 9},
    {"name": "NUMBER", "value": 10},
    {"name": "ATTACHMENT", "value": 11},
]


class DiscordClient:
    def __init__(self, app_id, token=None):
        self.app_id = app_id
        if not token:
            try:
                token = os.environ[DISCORD_TOKEN_KEY]
            except:
                raise Exception("Must provide bot token")
        self.headers = {
            "Authorization": f"Bot {token}",
        }

    def _make_request(self, method, path, req_args={}):
        res = method(
            f"{DISCORD_BASE_URL}/{path}", headers=self.headers, **req_args
        )
        if res.status_code > 299:
            logging.error(f"Request Failure to: {path}")
            logging.error(res.text)
            raise Exception(res.text)
        return res.json()

    def crupdate_command(self, command: BotCommand):
        create_res = self._make_request(
            requests.post,
            f"applications/{self.app_id}/commands",
            {
                "json": {
                    "name": command.name,
                    "description": command.description,
                    "type": command.type,
                }
            },
        )
        return create_res

    def list_commands(self):
        logging.info(
            self._make_request(
                requests.get,
                f"applications/{self.app_id}/commands",
            )
        )
