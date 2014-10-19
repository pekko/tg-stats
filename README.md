tg-stats
========
Some fun stats based on Telegram discussions.

Requirements
------------
- Python3 (run/tested only with Python >= 3.3)
- Telegram CLI. I use a modified version (see my forked repo pekko/tg), which includes complete timestamps and rate-limiting in fetching the full log

Installation
------------
Create symlink `tg` to point to Telegram CLI directory.

Usage
-----
- `get_log.sh` gets the discussions. First parameter is the chat identifier, e.g. `./get_log.sh ChatRoom`
- `analyze.py` generates the stats and prints to stdout
- `markov.py` simulates the dicussion using Markov chains
- `flask-markov.py` launches a http server for simulation
