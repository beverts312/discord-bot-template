import json
import logging
from functools import wraps

from nacl.signing import VerifyKey

from get_secrets import get_secrets


def respond(status_code, body):
    return {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Expose-Headers": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "statusCode": status_code,
        "body": json.dumps(body),
    }


class BotUtils:
    @staticmethod
    def ping_pong(body):
        if body["type"] == 1:
            return True
        return False

    @staticmethod
    def verify_signature(event):
        raw_body = event["body"]
        auth_sig = event["headers"]["x-signature-ed25519"]
        auth_ts = event["headers"]["x-signature-timestamp"]

        message = auth_ts.encode() + raw_body.encode()
        verify_key = VerifyKey(
            bytes.fromhex(get_secrets()["discord_public_key"])
        )
        verify_key.verify(message, bytes.fromhex(auth_sig))


def bot_handler(func):
    @wraps(func)
    def wrapper(event, context):
        if event.get("source") == "aws.events":
            logging.info("cron event")
            return

        try:
            logging.info("verifying signature")
            BotUtils.verify_signature(event)
        except Exception as e:
            logging.error(e)
            return respond(401, {"message": "Unauthorized"})

        body = json.loads(event["body"])
        logging.info(body)
        if BotUtils.ping_pong(body):
            logging.info("ping pong")
            return respond(200, {"type": 1})

        try:
            res_data = func(body)
        except Exception as e:
            logging.error(e)
            res_data = {"content": "The bot experienced an error"}

        return respond(
            200,
            {
                "type": 4,
                "data": res_data,
            },
        )

    return wrapper
