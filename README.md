# 🎧 SpotifyLyricsTranslate

Bu proje, Spotify’da çalan şarkıları gerçek zamanlı olarak takip eden ve şarkı sözlerini İngilizce’den Türkçe’ye çeviren bir otomasyon sistemidir.  

🌐 Spotify API ile anlık parça bilgileri alınır ve Selenium ile tarayıcı üzerinden lyrics sayfasına erişim sağlanır. Ardından sözler **argos-translate** kütüphanesi ile tamamen lokal olarak çevrilir. 🌐  

## ⚠️ UYARI ⚠️ 
-Uygulamanın şuanki sürümünde (v1.0) UI kısmı Spotify API bağlantısı yapıldıktan sonra açıldığından dolayı uygulamanın açılması uzun sürebilir 

## 🖥️ Kullanılan Teknolojiler
- Python
- Spotipy (Spotify API)
- Selenium
- azlyrics.com (lyrics sources)
- Tkinter
- argos-translate (offline çeviri)

## ⚙️ İşleyiş
- Kullanıcı arayüzü çalan şarkıyı ve çevirisini gösterir.
- Backend, şarkı sözlerini çekmek, sayfayı kontrol etmek ve çeviriyi sağlamak için ayrı bir thread üzerinde çalışır.
- Şarkı değişimlerini sürekli kontrol eder ve lyrics çeker.
- Çekilen sözler otomatik olarak İngilizce’den Türkçe’ye çevrilir ve arayüzde görüntülenir.

## 📄 Durum
Proje yayınlanmıştır stabilite iyileştirmeleri üzerinde çalışılmaktadır ve ilerleyen zamanlarda diğer dilleri desteklemesi planlanıyordur.
