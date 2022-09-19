# No DPS 4 U
A bot made to help decide who gets what role in Overwatch.
Forget the tension created from the poker faces in the discord
call, waiting for eachother to fold for DPS.

## License:
MIT License

Copyright (c) 2022 Stoned Code

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Setup Instructions:
1. Clone the repository
```
git clone https://github.com/Stoned-Code/no_dps_4_u.git
```
2. Change directory to the repository
```
cd no_dps_4_u
```
3. Create a virtual environment:
```
python -m venv venv
```
4. Activate Virtual Environment:

- If you're using Windows
```
source venv/Scripts/activate
```

- If you're using Linux
``` 
source venv/bin/activate
```
5. Install Libraries
```
pip install -r requirements.txt
```
6. Create and open a file named "config.py" (Use whatever text editor you're comfortable using)
```
code config.py
```
7. Within the "config.py" file, create four variables
```python
PREFIX = 'owb.' # `string`: Prefix for the bot's commands.
TOKEN = 'your_bot_token' # `string`: The discord bot's token.
BOT_CHANNEL_IDS = [ID1, ID2, ID...] # `list(int)`: The whitelisted bot command channel for the bot.
REROLL_REACTION = '🎲' # `string`: The reaction used for 
```
8. Insure that the bot has the following permissions.
* "Send Message"
* "Read Message History"
* "Use External Emojis"
* "Add Reaction"

![Bot Permissions](https://github.com/Stoned-Code/no_dps_4_u/blob/main/Images/Permissions.png)
9. Run the bot
```
python main.py
```
