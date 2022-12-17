import json

import boto3


def setup_secret(bot_name, discord_public_key):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.create_secret(
        Name=f"{bot_name}-secrets",
        SecretString=json.dumps({"discord_public_key": discord_public_key}),
        ForceOverwriteReplicaSecret=True,
    )
    return response["ARN"]


def create_sam_config(
    bot_name,
    secret_arn,
    domain,
    hosted_zone_id,
    sam_bucket="aws-sam-cli-managed-default-samclisourcebucket-1uxzopm8jvt3h",
    region="us-east-1",
):
    contents = f"""
version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "{bot_name}"
s3_bucket = "{sam_bucket}"
s3_prefix = "{bot_name}"
region = "{region}"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Stage=\\"dev\\" Domain=\\"{domain}\\" HostedZoneId=\\"{hosted_zone_id}\\" BotSecretArn=\\"{secret_arn}\\" BotName=\\"{bot_name}\\""
image_repositories = []
"""
    with open("samconfig.toml", "w") as f:
        f.write(contents)


name = input("Bot Name: ")
key = input("Discord Public Key: ")
secret_arn = setup_secret(name, key)
print(f"Created secret {secret_arn}")
domain = input("Domain: ")
hosted_zone_id = input("Hosted Zone ID: ")
create_sam_config(name, secret_arn, domain, hosted_zone_id)
print("Created samconfig.toml")
print("Run `sam build` and `sam deploy` to deploy the bot")
print(
    "After the bot is deployed, navigate to your app in the developer portal"
)
print(
    f"Find the 'INTERACTIONS ENDPOINT URL' field and set it to: https://{domain}/api/interactions"
)
print("When you click save discord will validate that your bot is working")
