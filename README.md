# Discord Bot Template

## Getting Started

### Prerequisites
* Python 3/pip/virtualenv
* AWS CLI+SAM CLI
* AWS Account
* Discord Developer Account 

### Setup
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Go to the Bot tab and create a new bot.
3. Clone this repo
4. Setup local env: `virtualenv venv && source venv/bin/activate && pip install -r dev-requirements.txt`
5. Run the setup script and follow the instructions it gives you `python scripts/setup_project.py`, this will:
    * Create an AWS secret for your bot
    * Setup your initial `samconfig.toml`
    * Give you instructions for deploying your bot
    * Give you instructions for registering your endpoint with Discord

## Development
Common tasks are managed with [invoke](https://www.pyinvoke.org/), run `inv -l` to see what is available.
