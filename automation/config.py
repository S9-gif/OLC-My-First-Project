import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "https://olc-backend.onrender.com/api/v1")
CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", 6))

# RSS Feed'ler - kategori bazlı
RSS_FEEDS = [
    {
        "url": "https://www.cnnturk.com/feed/rss/spor/news",
        "kategori": "spor",
        "kaynak_adi": "CNN Türk Spor"
    },
    {
        "url": "https://webrazzi.com/feed/",
        "kategori": "teknoloji",
        "kaynak_adi": "Webrazzi"
    },
    {
        "url": "https://www.bloomberght.com/rss",
        "kategori": "borsa",
        "kaynak_adi": "Bloomberg HT"
    },
]
