import json
import os

import boto3


def get_secrets():
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name="us-east-1"
    )
    return json.loads(
        client.get_secret_value(SecretId=os.environ["BOT_SECRETS_ARN"])[
            "SecretString"
        ]
    )
