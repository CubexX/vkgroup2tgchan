VKpulbic2TGbot
====
Reposting articles from VKontakte public group to Telegram bot.

Installation
-------
```bash
sudo pip3 install -r requirements.txt
```
Usage
-------
Edit constants in app.py:
```python
TOKEN = ''  # TG bot token
VK_TOKEN = ''  # VK access token
PUBLIC_ID = 0  # vk.com/wall<PUBLIC_ID>_...
INTERVAL = 60  # Seconds
IGNORE_TAGS = []  # ['#IGNORE', '#HASHTAGS']
```
And run bot:
```bash
python app.py
```
Then you need to start dialog with your bot and follow instructions.

License
-------
[MIT License](http://www.opensource.org/licenses/MIT)
