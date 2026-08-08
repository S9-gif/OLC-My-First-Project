import schedule
import time
from datetime import datetime
from rss_fetcher import run_all_feeds
from config import CHECK_INTERVAL_HOURS


def job():
    try:
        run_all_feeds()
    except Exception as e:
        print(f"❌ Job hatası: {e}")


if __name__ == "__main__":
    print(f"🚀 OLC Automation başlatıldı - {datetime.now()}")
    print(f"⏰ Her {CHECK_INTERVAL_HOURS} saatte bir çalışacak\n")

    # İlk çalıştırmayı hemen yap
    job()

    # Sonra periyodik olarak tekrarla
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # her dakika kontrol et
