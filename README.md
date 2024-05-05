# Set up
clone this repo, change ```private.py``` so that ```TOKEN``` and ```BOT_NAME``` match your bot's token and name (you get them when you create your bot via BotFather).
you can also set commands' descriptions (and commands themselves to show in chat) via any method you prefer (for example, using BotFather command).

# Config
change season number (and channel name), timings or messages in ```config.py```.
if you'd like to set a larger string, I'd recommend creating separate file for it and reading it in ```config.py```.

# Usage
```/start``` send a start message (depending on if user's id is in the ```all-users.json```) and writes user's info into ```all-users.json```.

```/help``` sends a help message.

```/add``` adds a user's id into ```active-users.json```, so the user is notified when the season starts.

```/remove``` removes a user's id from ```active-users.json```

# Development
## What trigers the bot to notify users?
the function ```manage_unread_messages``` scarps ```CHANNEL_NAME``` channel's messages, which have an id smaller than the last seen id (which is written later in ```last-message-id.txt```) and tries to find "PepeLand ```SEASON_NUMBER```" in the text of the message. notice that the loop doesn't break when it finds it, but it continues so that ```last-message0id``` is up to date.
## Passing other info into notification
if you'd like to get more info from the bot when it notifies you, I'd suggest returning this info in ```manage_unread_messages``` and changing ```callback_minute``` function, so it manages it correctly.
## Timings
you may want to change ```JOB_INTERVAL``` to get the notification faster, but be aware that it can lead into blocking your proxi (or smth like this idk).
