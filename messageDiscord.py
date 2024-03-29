import requests
import os
from discord import Webhook, RequestsWebhookAdapter

def push(message: str):
    url = os.environ.get("DC_WEBHOOK")
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    webhook.send(message)