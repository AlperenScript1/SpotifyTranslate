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
        client_id="yourID",  
        client_secret="yourSecret", 
        redirect_uri="http://127.0.0.1:8000/callback",
        scope="user-read-playback-state"
    )
)

def poller():
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
                        sleep(1)
                        driver.get("https://www.azlyrics.com/lyrics/" + clean(artist) + "/" +clean(lastTrack) + ".html" ) #! https://www.azlyrics.com/lyrics/cigarettesaftersex/silversable.html
                        sleep(2)
                        driver.execute_script("window.scrollBy(0, 1200)") #! 1200 pixel downPage
                        sleep(5) #! yüklendiği zaman kullanılacak
                        lyrics = driver.find_element(By.XPATH,"//body/div[@class='container main-page']/div[@class='row']/div[@class='col-xs-12 col-lg-8 text-center']/div[5]").text #! lyrics
                        lyrics_Label1.config(text = str(lyrics))  
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
            error_Label1.config(text=f"Hata: {e}")
        
        sleep(1) #! 10
            
#! UI
root = tk.Tk()
root.title("Spotify Takip") 
root.geometry("600x500")
root.configure(bg="black")

error_Label1 = tk.Label(root, text="Console", font=("Arial", 15), fg="red")
error_Label1.pack(pady=20)

track_Label1 = tk.Label(root, text="Bekleniyor...", font=("Arial", 15))
track_Label1.pack(pady=20)

lyrics_Label1 = tk.Label(root, text="Sözler alınıyor..", font=("Arial", 15))
lyrics_Label1.pack(pady=20)




#? threading olayı UI ve backend ayrı çalışması için.
threading.Thread(target=poller, daemon=True).start()
root.mainloop();

