
# Set Webhook
You need to set up an webhook that will be called by the Telegram servers
```python
import telegram
import urllib.parse

TOKEN = "YOURTOKEN"
bot = telegram.Bot(TOKEN)
app_url = "YourHookUrl"
url = urllib.parse.urljoin(app_url, '/' + TOKEN)
bot.setWebhook(url)
print(url)
```