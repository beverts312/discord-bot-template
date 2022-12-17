import json

import boto3

from bot_utils import BotInfo


def setup_secret(bot_name, discord_public_key):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.create_secret(
        Name=f"{bot_name}-secrets",
        SecretString=json.dumps({"discord_public_key": discord_public_key}),
        ForceOverwriteReplicaSecret=True,
    )
    return response["ARN"]


try:
    bot_info = BotInfo.load_from_file()
    print(f"Bot with app id {bot_info.app_id} is already initialized here")
    exit(0)
except:
    print("No existing info found")

name = input("Bot Name: ")
app_id = input("Discord App Id: ")
key = input("Discord Public Key: ")
secrets_arn = setup_secret(name, key)
print(f"Created secret {secrets_arn}")
domain = input("Domain: ")
hosted_zone_id = input("Hosted Zone ID: ")
bot_info = BotInfo(
    app_id=app_id,
    name=name,
    interaction_url=f"https://{domain}/api/interactions",
    secrets_arn=secrets_arn,
    hosted_zone_id=hosted_zone_id,
    commands=[],
)
bot_info.crupdate_info_file()
print("Created bot_info.yml")
bot_info.crupdate_sam_config()
print("Created samconfig.toml")
print("Run `sam build` and `sam deploy` to deploy the bot")
print(
    "After the bot is deployed, navigate to your app in the developer portal"
)
print(
    f"Find the 'INTERACTIONS ENDPOINT URL' field and set it to: {bot_info.interaction_url}"
)
print("When you click save discord will validate that your bot is working")
