import tkinter as tk
import threading
import time
from spotipy.oauth2 import SpotifyOAuth
import spotipy
#! Selenium
from selenium import webdriver  
import chromedriver_autoinstaller 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep, time
import random
import re

chromedriver_autoinstaller;
options = Options()

#! Kullanılmıyor
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


def poller():
    lyrics_text1.config(state="disabled") #! noWrite
    while True:
        try:
            current = spotify.current_playback()
            if current and current["is_playing"]:
                firstTrack = current["item"]["name"]
                lastTrack = firstTrack
                artist = current["item"]["artists"][0]["name"]
                track_Label1.config(text=f"{artist} - {lastTrack}")
                print(artist +" "+ lastTrack) 
                if artist and lastTrack != None:
                        print("===========================================================")
                        lyrics_Label1.config(text="Şarkı sözleri alınıyor..");
                        driver.get("https://www.azlyrics.com/lyrics/" + clean(artist) + "/" +clean(lastTrack) + ".html" ) #! https://www.azlyrics.com/lyrics/cigarettesaftersex/silversable.html
                        driver.execute_script("window.scrollBy(0, 1200)") #! 1200 pixel downPage
                        sleep(5) #TODO: element yüklendiği zaman kullanılacak
                        lyrics = driver.find_element(By.XPATH,"//body/div[@class='container main-page']/div[@class='row']/div[@class='col-xs-12 col-lg-8 text-center']/div[5]").text #! lyrics
                        lyrics_Label1.config(bg="green")
                        lyrics_Label1.config(text="Şarkı sözleri alındı :)");
                        lyrics_text1.config(state="normal") #! Write
                        lyrics_text1.insert("1.0", lyrics)  #! Lyrics to text 
                        lyrics_text1.config(state="disabled") #! noWrite
                        print(lyrics);
                        if(lyrics != None):
                            print("Şarkı sözleri alındı !");
                        else:
                            print("Şarkı sözleri alınamadı..");
                else:
                    print("Spotify bağlantısı kurulamadı..");
            else:
                track_Label1.config(text="Çalmıyor")
        except Exception as e:
               lyrics_Label1.config(bg="red")
               lyrics_Label1.config(text="Şarkı sözleri alınamadı :(");  #!error_Label1.config(text=f"Hata: {e}")
               #TODO: if sorgusu gelicek 
        sleep(10) #! 10
            
#! UI
root = tk.Tk()
root.title("SpotifyTranslate") 
root.geometry("650x550")
root.configure(bg="black")

error_Label1 = tk.Label(root, text="Terminal Exception {E}", font=("Arial", 15), fg="red")
error_Label1.pack(pady=20)

track_Label1 = tk.Label(root, text="Bekleniyor... {Track}", font=("Arial", 15))
track_Label1.pack(pady=20)

lyrics_Label1 = tk.Label(root, text="none {Lyrics}", font=("Arial", 15))
lyrics_Label1.pack(pady=20)

#? text
lyrics_text1 = tk.Text(root, wrap="word", bg="black", fg="white")
lyrics_text1.pack(side="left", fill="both", expand=True)

#? scrollbar
lyrics_scrollbar1 = tk.Scrollbar(root, command=lyrics_text1.yview)
lyrics_scrollbar1.pack(side="right", fill="y")
#? lyrics_text1 → scrollbar bağlantısı
lyrics_text1.config(yscrollcommand=lyrics_scrollbar1.set) #! state="disabled" (Değişken değerini atamıyorum) 

#? "threading" olayı UI ve backend ayrı çalışması için.
threading.Thread(target=poller, daemon=True).start()
root.mainloop();
