from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from spotipy.oauth2 import SpotifyOAuth
import chromedriver_autoinstaller 
import argostranslate.translate #? Local ceviri yapacağımız kütüphane.
from unidecode import unidecode #? Karakterleri TR'den en çevirmeye yarayan kütüphane. 
from selenium import webdriver  
from time import sleep, time
import tkinter as tk
import threading
import spotipy
import random
import time
import re
#! Selenium

chromedriver_autoinstaller;
options = Options()

#? URL özelleştirme 
def clean(text): 
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "", text)  # boşluk ve özel karakterleri tire yap
    return text.strip("-")  # baş/sondaki tireleri sil
options.add_argument("--window-size=1920,800") #? Sayfa görünür olmasa bile çözünürlüğü ayarlar.

#! Selenium
#! Sonradan eklendi SSL için 
options.add_argument("--disable-blink-features=AutomationControlled --allow-insecure-localhost --ignore-certificate-errors")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--headless") 
driver = webdriver.Chrome(options=options); 
url = "https://azlyrics.com" #! Sözlerin sağlandığı platform azlyrics
driver.get(url)

#? Spotify API  "client_id" & "client_secret"
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth( #! Tokenler kontrol edilecek [SSL error code] (handshake failed; returned -1, SSL error code 1, net_error -101)
        client_id="5d9b8645384941bb872cdc7cd4cc40a4", #TODO: YourID
        client_secret="017f56dba2444610b24af44b430c54a3", #TODO: YourSecret
        redirect_uri="http://127.0.0.1:8000/callback",
        scope="user-read-playback-state"
    )
)

        #! "azlyrics" ŞARKI İSİMLERİNİ FARKLI ŞEKİLLERDE KAYDETTİĞİ İÇİN
        #! ARATMA KISMINDAN ŞARKI + SANATCI OLACAK ŞEKİLDE ARATILACAK 


def checkApi():
    lyrics_text1.config(state="disabled") #! noWrite
    lastTrack = None
    while True: #? Çalan şarkı aynı olduğu zaman tekrardan söz alımı yapılmıyor.
        try:
            current = spotify.current_playback()
            if current and current.get("is_playing"):
                firstTrack = current["item"]["name"]
                artist = current["item"]["artists"][0]["name"]
                track_Label1.config(text=f"{artist} - {firstTrack}")
                print(artist + " " + firstTrack)

                
                if artist and firstTrack != None: #! Kullanıcı şarkıyı başlatmamış olabilir.              #artist is not None and firstTrack is not None 
                    if lastTrack == firstTrack: #? İsim Aynı ise atlanıyor
                        print("Aynı şarkı tekrar bulundu; arama atlandı.")
                    else:
                        lyrics_text1.config(state="normal")
                        lyrics_text1.delete("1.0", "end") #? Eski sözleri siliyor.
                        lyrics_text1.config(state="disable")
                        lastTrack = firstTrack
                        print("==========================--=================================")
                        lyrics_Label1.pack(pady=8)
                        lyrics_Label1.configure(bg="black", fg="white")
                        lyrics_text1.configure(bg="black", fg="white")
                        lyrics_Label1.config(text="Şarkı sözleri alınıyor..")
                        #? azlyrics search
                        searchEntry = driver.find_element(By.CLASS_NAME, "form-control")
                        print("Selenium: search Class bulundu")
                        print(str(artist) + " " + str(lastTrack))
                        try:
                            searchEntry.clear() #? Önceden aratılanı temizliyor.
                        except Exception:
                            pass
                        searchEntry.send_keys(str(artist) + " " + str(lastTrack))
                        sleep(2)
                        searchButton = driver.find_element(By.CSS_SELECTOR, "form[class='navbar-form navbar-right search'] button[type='submit']")
                        sleep(2)
                        foundTrack = driver.find_element(By.CLASS_NAME, "eac-item") 
                        print("foundTrack");
                        foundTrack.click()
                        lyrics = driver.find_element(By.XPATH, "//body/div[@class='container main-page']/div[@class='row']/div[@class='col-xs-12 col-lg-8 text-center']/div[5]").text

                        print("En: " + str(lyrics)) #? en
                        lyricsMakeTranslate = lyrics
                        lyricsTranslate = argostranslate.translate.translate(lyricsMakeTranslate, "en", "tr")
                        print("Tr: " + str(lyricsTranslate)) #? tr 
                        
                        lyrics_text1.config(state="normal")
                        lyrics_text1.delete("1.0", "end") #? Eski sözleri siliyor.
                        lyrics_text1.insert("1.0", lyricsTranslate) #? Yeni(TR Çevirilmiş) sözleri ekliyor.
                        lyrics_text1.config(state="disabled")
                        sleep(2)
                        lyrics_Label1.pack_forget()
                else:
                    print("Spotify bağlantısı kurulamadı..")
            else:
                track_Label1.config(text="Çalmıyor")
                lyrics_Label1.pack(pady=20)
                sleep(1)
                lyrics_Label1.config(text="En son dinlenilen: " + str(artist) + " - " +  str(lastTrack));
        except Exception as e:
               lyrics_Label1.config(bg="red")
               lyrics_Label1.config(text="Şarkı sözleri alınamadı :( Spotify bağlantınızı kontrol ediniz.")
               print("checkApi hata:", e)

        sleep(5) #! 10
            
#! UI
root = tk.Tk()
root.title("SpotifyTranslate")
root.geometry("650x600")
root.configure(bg="black")

top_frame = tk.Frame(root, bg="black")
top_frame.pack(side="top", fill="x")

error_Label1 = tk.Label(top_frame, text="Terminal Exception {E}", font=("Arial", 15), fg="red", bg="black")
error_Label1.pack(pady=(10, 5))

track_Label1 = tk.Label(top_frame, text="Bekleniyor... {Track}", font=("Arial", 15), wraplength=510, bg="black", fg="white")
track_Label1.pack(pady=5)

lyrics_Label1 = tk.Label(top_frame, text="none {Lyrics}", font=("Arial", 15), bg="black", fg="white")
lyrics_Label1.pack(pady=(5, 10))

# Content frame for text area and scrollbar
content_frame = tk.Frame(root)
content_frame.pack(side="top", fill="both", expand=True)

lyrics_text1 = tk.Text(content_frame, wrap="word", bg="black", fg="white")
lyrics_text1.pack(side="left", fill="both", expand=True)

lyrics_scrollbar1 = tk.Scrollbar(content_frame, command=lyrics_text1.yview)
lyrics_scrollbar1.pack(side="right", fill="y")
lyrics_text1.config(yscrollcommand=lyrics_scrollbar1.set)

threading.Thread(target=checkApi, daemon=True).start()
root.mainloop()
