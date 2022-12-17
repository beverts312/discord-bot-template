from dataclasses import asdict, dataclass, field
from typing import List

import yaml

from .dir_helpers import get_repo_dir

REPO_DIR = get_repo_dir()
BOT_INFO_FILE = f"{REPO_DIR}/bot_info.yml"
SAMCONFIG_FILE = f"{REPO_DIR}/samconfig.toml"


@dataclass
class BotArg:
    name: str
    description: str
    type: int


@dataclass
class BotCommand:
    name: str
    description: str
    type: int
    id: str = ""
    arguements: List[BotArg] = field(default_factory=lambda: [])


@dataclass
class BotInfo:
    name: str
    app_id: str
    interaction_url: str
    secrets_arn: str
    hosted_zone_id: str
    commands: List[BotCommand] = field(default_factory=lambda: [])

    def crupdate_info_file(self):
        with open(BOT_INFO_FILE, "w") as f:
            f.write(yaml.safe_dump(asdict(self), sort_keys=False))

    def crupdate_sam_config(
        self,
        sam_bucket="aws-sam-cli-managed-default-samclisourcebucket-1uxzopm8jvt3h",
        region="us-east-1",
    ):
        contents = f"""
version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "{self.name}"
s3_bucket = "{sam_bucket}"
s3_prefix = "{self.name}"
region = "{region}"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Stage=\\"dev\\" Domain=\\"{self.interaction_url.replace('https://', '').replace('/api/interactions', '')}\\" HostedZoneId=\\"{self.hosted_zone_id}\\" BotSecretArn=\\"{self.secrets_arn}\\" BotName=\\"{self.name}\\""
image_repositories = []
    """
        with open(SAMCONFIG_FILE, "w") as f:
            f.write(contents)

    @staticmethod
    def load_from_file():
        try:
            with open(BOT_INFO_FILE) as f:
                data = f.read()
        except:
            raise Exception(f"Could not read file {BOT_INFO_FILE}")

        parsed_data = yaml.safe_load(data)
        parsed_data["commands"] = list(
            map(lambda x: BotCommand(**x), parsed_data.get("commands", []))
        )
        return BotInfo(**parsed_data)
