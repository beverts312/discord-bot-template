import json
import logging
import os

import boto3

from discord_lite import bot_handler

logging.getLogger().setLevel(logging.INFO)


@bot_handler
def discord_bot(command_body):
    return {"content": "Hello Moto"}


def long_response_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        logging.info(body)


def send_long_response_msg(body):
    boto3.client("sqs", region_name="us-east-1").send_message(
        QueueUrl=os.getenv("LONG_RESPONSE_QUEUE"), MessageBody=body
    )
