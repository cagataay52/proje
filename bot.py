import feedparser
import json
import os
from datetime import datetime

# Haber çekilecek kaynak (CNN Türk Teknoloji RSS)
rss_url = "https://www.cnnturk.com/feed/rss/teknoloji/news"

print("Haberler kaynaktan çekiliyor...")

# RSS kaynağını oku
feed = feedparser.parse(rss_url)

yeni_haberler = []

# İlk 6 haberi al
for entry in feed.entries[:6]:
    # Resim bulma işlemi (RSS'den görseli ayıkla)
    gorsel = "https://picsum.photos/400/300?random=1" # Varsayılan resim
    
    # Eğer haberin içinde medya görseli varsa onu al
    if 'media_content' in entry:
        gorsel = entry.media_content[0]['url']
    elif 'links' in entry:
        for link in entry.links:
            if 'image' in link.type:
                gorsel = link.href
                break

    # Haberi bizim formatımıza uyarla
    haber = {
        "baslik": entry.title,
        "ozet": entry.summary[:120] + "...", # Özeti kısalt
        "kategori": "TEKNOLOJİ",
        "resim": gorsel,
        "link": entry.link,
        "tarih": "Yeni"
    }
    
    yeni_haberler.append(haber)
    print(f"Alındı: {entry.title}")

# Verileri JSON dosyasına kaydet
with open('haberler.json', 'w', encoding='utf-8') as f:
    json.dump(yeni_haberler, f, ensure_ascii=False, indent=4)

print("-" * 30)
print("BAŞARILI! haberler.json dosyası güncellendi.")