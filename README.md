# 🎧 SpotifyLyricsTranslate

Bu proje, Spotify’da çalan şarkıları gerçek zamanlı olarak takip eden ve şarkı sözlerini İngilizce’den Türkçe’ye çeviren bir otomasyon sistemidir.  

🌐 Spotify API ile anlık parça bilgileri alınır ve Selenium ile tarayıcı üzerinden lyrics sayfasına erişim sağlanır. Ardından sözler **argos-translate** kütüphanesi ile tamamen lokal olarak çevrilir. 🌐  

## 🖥️ Kullanılan Teknolojiler
- Python
- Spotipy (Spotify API)
- Selenium
- Tkinter
- argos-translate (offline çeviri)

## ⚙️ İşleyiş
- Kullanıcı arayüzü çalan şarkıyı ve çevirisini gösterir.
- Backend, şarkı sözlerini çekmek, sayfayı kontrol etmek ve çeviriyi sağlamak için ayrı bir thread üzerinde çalışır.
- Şarkı değişimlerini sürekli kontrol eder ve lyrics çeker.
- Çekilen sözler otomatik olarak İngilizce’den Türkçe’ye çevrilir ve arayüzde görüntülenir.

## 📄 Durum
Proje hâlihazırda geliştirme aşamasında olup, farklı lyrics kaynakları, çeviri entegrasyonu ve stabilite iyileştirmeleri üzerinde çalışılmaktadır.

**Özet:** Spotify entegrasyonu + web otomasyonu + İngilizce’den Türkçe’ye offline çeviri üzerine canlı gelişen teknik bir demo. 🚀
