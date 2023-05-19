# AutoGPT-Discord
## A plugin to enable you to control and watch your AutoGPT instance from Discord!

![ee](https://github.com/gravelBridge/AutoGPT-Discord/assets/107640947/90eaad77-eed3-4375-a60d-9145c7038103)

<img width="1470" alt="Screenshot 2023-05-04 at 9 21 15 PM" src="https://user-images.githubusercontent.com/107640947/236398607-5145f9f9-015b-4573-90ac-435dd118ea79.png">

## 📚 Requirements

1. **Python Package**: Install the discord Python package:

`pip install discord`

2. **Discord Bot Token**: Visit the link https://discord.com/developers/docs/getting-started
- Press the Create App button and log in with your Discord account.
- Name the app anything you want, I like to name it AutoGPT for readability.
- Navigate to the Bot tab on the left side of the screen, and scroll down to the Priviliged Gateway Intents section.
- Enable the Server Members Intent and the Message Content Intent.
- Then, press the OAuth2 -> URL Generator tab.
- Press bot in the scopes section. Then, in bot permissions, check send messages and read message history.
- Scroll down and copy the link. Paste the link into a new tab, and invite the bot to a server of your choosing! (You must have admin access to this server)
- Go back to the bot tab, and press Reset Token. Copy this token, and keep this safe, as you will use this to configure the plugin later on.

## ⚙️ Installation

Follow these steps to configure the AutoGPT Discord Plugin:

### 1. Clone this Repository
cd into a folder that you can find easily. For example: `cd desktop`. 
Then, paste this command: `git clone https://github.com/gravelBridge/AutoGPT-Discord.git`

### 2. Navigate to the folder
Navigate to the folder where you ran the cd command

### 3. Zip the discord_plugin folder
On MacOS, right click the discord_plugin folder and press `Compress`. On windows, right click the folder, and press `Send to > Compressed (zipped)`.

### 4. Move the zip file
Move the new discord_plugin.zip file to the AutoGPT plugins directory, there should already be a file there titled `__PUT_PLUGIN_ZIPS_HERE__`.

## 🔧 Configuration

1. **Update the .env file**: Add the following lines to your `.env` file:

```
################################################################################
### DISCORD PLUGIN SETTINGS
################################################################################

DISCORD_BOT_TOKEN=sadfJHo3h4h3heof
AUTHORIZED_USER_IDS=111111,222222,333333
BOT_PREFIX=!
CHANNEL_ID=123456789
ASK_FOR_INPUT=True
```
- DISCORD_BOT_TOKEN: This is the bot token that you received from Step Two.
- AUTHORIZED_USER_IDS: A list of comma separated Discord User IDS that will have access to control AutoGPT. If you don't know how to get this, search up "How to get Discord User Id"
- BOT_PREFIX: The prefix to use when using commands with the Discord Bot.
- CHANNEL_ID: The channel id in which the bot will be giving information, and requesting input. If you don't know how to get this, search up "How to get Discord Channel Id"
- ASK_FOR_INPUT: Whether to ask for user confirmation and/or feedback before running a command.

2. **Run the bot in continuous mode**: Run AutoGPT with the extra argument --continuous
- Without this, the plugin is useless as you still have to manually confirm commands in the actual AutoGPT instance.
- You can configure if you want AutoGPT to be truly continuous with the ASK_FOR_INPUT env variable. If this is False, then AutoGPT will be truly continuous: running commands without consulting you. If this is True, AutoGPT will ask you in Discord to approve, deny, or to provide feedback on the command.

3. **Allowlist Plugin**: In your `.env` file, search for `ALLOWLISTED_PLUGINS` and add this plugin:

```
################################################################################
ALLOWLISTED PLUGINS
################################################################################

#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTDiscord
```

## 🤖 Commands

Remember to use your bot prefix directly before running any commands!

- shutdown: Shuts down the entire AutoGPT instance.

### Shoutout to @CTHULHUCTHULHU for reworking most of the plugin, really amazing work <3

## 🚀 That's it! Congratulations!

**Make sure to leave a star on this repository! Thank you!**
