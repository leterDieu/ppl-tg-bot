# Set up
clone this repo, add ```private.py``` in which create two variables ```TOKEN``` and ```BOT_NAME``` (as shown in private_example.py, which you can remove), add ```active-users.json``` (an empty list) and ```all-users.json``` (an empty dict).

# Config
change season number, timings or messages in ```config.py```.
if you'd like to set a bigger string, I'd recommend creating separate file for it and reading it in ```config.py```.

# Usage
```/start``` send a start message (depending on if user's id is in the ```all-users.json```) and writes user's info into ```all-users.json```.

```/help``` sends a help message.

```/add``` adds user's id into ```active-users.json```.

```/remove``` removes user's id from ```active-users.json```
