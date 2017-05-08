
# Set Webhook

```python
import telegram
import urllib.parse

TOKEN = "YOURTOKEN"
bot = telegram.Bot(TOKEN)
app_url = "YourHookUrl"
url = urllib.parse.urljoin(app_url, '/' + TOKEN)
bot.setWebhook(url)
print(url)
python
```