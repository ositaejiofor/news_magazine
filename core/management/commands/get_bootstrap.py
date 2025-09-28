import os
import urllib.request
from django.core.management.base import BaseCommand
from django.conf import settings

BOOTSTRAP_VERSION = "5.3.3"
BOOTSTRAP_CSS_URL = f"https://cdn.jsdelivr.net/npm/bootstrap@{BOOTSTRAP_VERSION}/dist/css/bootstrap.min.css"
BOOTSTRAP_JS_URL = f"https://cdn.jsdelivr.net/npm/bootstrap@{BOOTSTRAP_VERSION}/dist/js/bootstrap.bundle.min.js"

class Command(BaseCommand):
    help = "Download Bootstrap CSS and JS into static/ folder"

    def handle(self, *args, **kwargs):
        static_dir = settings.BASE_DIR / "static" / "bootstrap"
        os.makedirs(static_dir, exist_ok=True)

        files = {
            "bootstrap.min.css": BOOTSTRAP_CSS_URL,
            "bootstrap.bundle.min.js": BOOTSTRAP_JS_URL,
        }

        for filename, url in files.items():
            path = static_dir / filename
            self.stdout.write(f"Downloading {url} → {path}")
            urllib.request.urlretrieve(url, path)

        self.stdout.write(self.style.SUCCESS("Bootstrap downloaded successfully!"))
