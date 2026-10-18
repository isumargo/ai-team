import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse

class Command(BaseCommand):
    help = 'Registers the Telegram webhook'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The public URL of the app (e.g. https://distro.raminesia.com)')

    def handle(self, *args, **options):
        base_url = options['url'].rstrip('/')
        token = settings.TELEGRAM_BOT_TOKEN
        webhook_path = reverse('telegram_webhook', kwargs={'token': token})
        webhook_url = f"{base_url}{webhook_path}"
        
        self.stdout.write(f"Setting webhook to: {webhook_url}...")
        
        url = f"https://api.telegram.org/bot{token}/setWebhook"
        response = requests.post(url, data={'url': webhook_url})
        
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS(f"Successfully set webhook: {response.json()}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to set webhook: {response.text}"))
