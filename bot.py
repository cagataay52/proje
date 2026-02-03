import feedparser
import json
import ssl

# SSL Sertifika hatalarını yok saymak için (Bazen engel çıkarır)
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# 1. Adres: ShiftDelete.Net (Teknoloji Haberleri)
rss_url = "https://shiftdelete.net/feed"

print(f"Baglanti kuruluyor: {rss_url}")

# Kendimizi "Chrome Tarayıcısı" gibi tanıtıyoruz (Engellenmemek için)
feed = feedparser.parse(rss_url, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

yeni_haberler = []

# Veri geldi mi kontrol et
if len(feed.entries) > 0:
    print(f"Bağlantı Başarılı! Toplam {len(feed.entries)} haber bulundu.")

    # İlk 6 haberi al
    for entry in feed.entries[:6]:
        
        # Resim bulma (ShiftDelete genelde 'media_content' kullanır)
        gorsel = "https://picsum.photos/400/300?random=1" # Yedek resim
        
        try:
            if 'media_thumbnail' in entry:
                gorsel = entry.media_thumbnail[0]['url']
            elif 'media_content' in entry:
                gorsel = entry.media_content[0]['url']
            elif 'links' in entry:
                for link in entry.links:
                    if 'image' in link.type:
                        gorsel = link.href
                        break
        except:
            pass # Resim bulamazsa hata verme, yedeği kullan

        # Özeti temizle
        ozet_metni = entry.summary if 'summary' in entry else entry.title
        # HTML etiketlerini (p, br gibi) basitçe temizle
        ozet_metni = ozet_metni.replace("<p>", "").replace("</p>", "").replace("[&hellip;]", "...")[:120] + "..."

        haber = {
            "baslik": entry.title,
            "ozet": ozet_metni,
            "kategori": "TEKNOLOJİ",
            "resim": gorsel,
            "link": entry.link,
            "tarih": "Yeni"
        }
        
        yeni_haberler.append(haber)
        print(f"Alındı: {entry.title}")

    # JSON Dosyasını Yaz
    with open('haberler.json', 'w', encoding='utf-8') as f:
        json.dump(yeni_haberler, f, ensure_ascii=False, indent=4)
    
    print("-" * 30)
    print("MÜKEMMEL! haberler.json dosyası ShiftDelete haberleriyle doldu.")

else:
    print("HATA: Yine veri gelmedi. Lütfen internet bağlantınızı kontrol edin.")
    if hasattr(feed, 'status'):
        print(f"Hata Kodu: {feed.status}")