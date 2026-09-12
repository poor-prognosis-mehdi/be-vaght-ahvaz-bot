# Be Vaght Ahvaz — Telegram Bot

The official Telegram bot for **Be Vaght Ahvaz** (به وقت اهواز), a news outlet covering current issues and problems affecting the people of Khuzestan province. This bot serves as an anonymous communication channel between citizens and the news team.

## Purpose

Citizens of Khuzestan can use this bot to report local issues, problems, and concerns (infrastructure, public services, environment, and other day-to-day matters) directly to the Be Vaght Ahvaz news team — completely anonymously, without revealing their name or Telegram ID.

## Features

- 🤖 **About the Bot** — explains the purpose of the bot and how to use it
- ✉️ **Anonymous Personal Message** — users can report issues or send messages; their identity (name, username, numeric ID) is never shown to the admin
- 🔑 **Reply System** — the admin can respond to each message using a unique question code, without ever seeing who sent it

## Requirements

- Python 3.9 or higher
- A bot token from [@BotFather](https://t.me/BotFather)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. Install the required library:
   ```bash
   pip install pyTelegramBotAPI
   ```

3. Set your bot token and admin ID in `bot.py`:
   ```python
   TOKEN = "your_bot_token"
   ADMIN_ID = your_telegram_numeric_id
   ```

   > ⚠️ **Security warning:** Never commit your real bot token to a public GitHub repository. It's recommended to load the token from an environment variable instead.

## Anonymous Message Reply System

When a citizen sends a message via the "Anonymous Personal Message" button:

- The message is forwarded to the admin along with a **question code** (no name, username, or ID is shown)
- The admin replies by sending the following command in the chat with the bot:
  ```
  /reply question_code your_answer
  ```
- The reply is automatically sent back to that user, without revealing their identity to the admin

> ℹ️ Question codes are stored in memory (RAM) only and will be lost if the bot restarts.

## Project Structure

```
.
├── bot.py          # Main bot code
└── README.md       # This file
```

## First-Time Setup: Running the Bot with Screen

To run the bot persistently on a server for the first time, follow these steps:

1. Create a new virtual screen session:
   ```bash
   screen -S telegram_bot
   ```

2. Activate your Python virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Run the bot:
   ```bash
   python3 bot.py
   ```

4. If everything is set up correctly, you should see the following output:
   ```
   Bot is running...
   ```

5. Detach from the screen session (leaving the bot running in the background) by pressing:
   ```
   Ctrl + A, then D
   ```

## Stopping the Bot to Apply Code Changes

If the bot is running inside a `screen` session (e.g. named `telegram_bot`) on your server, follow these steps before pulling and applying new code:

1. Reattach to the running screen session:
   ```bash
   screen -r telegram_bot
   ```

2. Stop the bot by pressing:
   ```
   Ctrl + C
   ```

3. Now pull the latest changes (see the section below) and run the bot again:
   ```bash
   python bot.py
   ```

4. To detach from the screen session and leave the bot running in the background, press:
   ```
   Ctrl + A, then D
   ```

> ℹ️ If you don't have a screen session named `telegram_bot` yet, create one with `screen -S telegram_bot` before starting the bot for the first time.

## Updating the Bot After Code Changes

If you make changes to `bot.py` (locally or via GitHub) and want to pull the latest version to your server:

1. Open a terminal (or PowerShell on Windows) in your project folder.

2. Pull the latest changes from GitHub:
   ```bash
   git pull
   ```

3. If you edited the code on the server itself and pushed it to GitHub from there, make sure to commit and push first, **before** pulling elsewhere:
   ```bash
   git add .
   git commit -m "Describe your change here"
   git push
   ```

4. After pulling, restart the bot so the new code takes effect (see "Stopping the Bot to Apply Code Changes" above, then start it again).

> ℹ️ If the bot is running as a background service (e.g. via `systemd`, `pm2`, or `screen`), remember to restart that service after `git pull`, otherwise it will keep running the old code.

## Running Continuously on a Server (VPS)

To keep the bot running 24/7, use a process manager such as `systemd`, `screen`, `tmux`, or `pm2` so it stays active after the terminal closes or the server restarts.

## Disclaimer

This bot is intended solely as a communication channel for citizens of Khuzestan province to report local issues to the Be Vaght Ahvaz news team. All submissions are anonymous and the news team is responsible for reviewing and following up on reported matters.
