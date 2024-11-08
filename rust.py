import obspython as obs
from threading import Thread
from pynput import keyboard
import threading
import time
import random
import os

# Ana değişkenler
running = True
hide_timer = None
DELAY = 0.5
current_scene_item = None
current_media_source = None
is_showing = False  # Medyanın gösterilip gösterilmediğini takip etmek için

# Video boyutları
VIDEO_WIDTH = 2560
VIDEO_HEIGHT = 1440

def script_description():
   return "Shows random images/videos with G key"

def script_load(settings):
   # Videos klasörünü kontrol et
   video_dir = os.path.join(os.path.dirname(__file__), "videos")
   if os.path.exists(video_dir):
       videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
       print(f"Bulunan videolar: {videos}")

def get_source_by_name(name):
   sources = obs.obs_enum_sources()
   if sources:
       for source in sources:
           if obs.obs_source_get_name(source) == name:
               return source
   return None

def set_item_bounds(scene_item):
   """Video boyutunu ve pozisyonunu ayarla"""
   # Boyut ayarları
   bounds = obs.vec2()
   bounds.x = VIDEO_WIDTH
   bounds.y = VIDEO_HEIGHT
   obs.obs_sceneitem_set_bounds(scene_item, bounds)
   obs.obs_sceneitem_set_bounds_type(scene_item, obs.OBS_BOUNDS_SCALE_INNER)
   
   # Videonun merkezde olması için pozisyon ayarları
   pos = obs.vec2()
   pos.x = 0  # Yatay pozisyon
   pos.y = 0  # Dikey pozisyon
   obs.obs_sceneitem_set_pos(scene_item, pos)
   
   # Hizalama ayarları (merkezde olması için)
   obs.obs_sceneitem_set_alignment(scene_item, 5)  # 5 = Merkez hizalama
   
   # Videonun boyutunu sabit tut
   scale = obs.vec2()
   scale.x = 1.0
   scale.y = 1.0
   obs.obs_sceneitem_set_scale(scene_item, scale)

def show_random_media():
   try:
       global current_scene_item, current_media_source, is_showing
       
       # Eğer zaten gösteriyorsa, yeni medya yükleme
       if is_showing:
           return
           
       video_dir = os.path.join(os.path.dirname(__file__), "videos")
       media_files = []
       if os.path.exists(video_dir):
           media_files.extend([(os.path.join(video_dir, f), 'video') 
                             for f in os.listdir(video_dir) 
                             if f.endswith('.mp4')])
       
       if not media_files:
           print("HATA: Video dosyası bulunamadı!")
           return
           
       # Rastgele video seç
       media_path, media_type = random.choice(media_files)
       print(f"Seçilen video: {os.path.basename(media_path)}")
       
       # Rust kaynağını gizle
       rust_source = get_source_by_name("rust")
       if rust_source:
           obs.obs_source_set_enabled(rust_source, False)
       
       # Mevcut sahneyi al
       current_scene = obs.obs_frontend_get_current_scene()
       scene = obs.obs_scene_from_source(current_scene)
       
       if scene:
           # Eski medyayı kaldır
           if current_scene_item:
               obs.obs_sceneitem_remove(current_scene_item)
               current_scene_item = None
           if current_media_source:
               obs.obs_source_remove(current_media_source)
               current_media_source = None
           
           # Video kaynağı oluştur
           settings = obs.obs_data_create()
           obs.obs_data_set_string(settings, "local_file", media_path)
           obs.obs_data_set_bool(settings, "looping", True)
           obs.obs_data_set_bool(settings, "restart_on_activate", True)
           current_media_source = obs.obs_source_create("ffmpeg_source", "random_media", settings, None)
           
           if current_media_source:
               # Sahneye ekle
               current_scene_item = obs.obs_scene_add(scene, current_media_source)
               # Boyut ve pozisyonu ayarla
               set_item_bounds(current_scene_item)
               obs.obs_source_release(current_media_source)
           
           obs.obs_data_release(settings)
           is_showing = True
       
       obs.obs_source_release(current_scene)
       
   except Exception as e:
       print(f"HATA (show_random_media): {str(e)}")

def hide_media():
   try:
       global current_scene_item, current_media_source, is_showing
       
       # Mevcut sahneyi al
       current_scene = obs.obs_frontend_get_current_scene()
       scene = obs.obs_scene_from_source(current_scene)
       
       if scene:
           # Medyayı kaldır
           if current_scene_item:
               obs.obs_sceneitem_remove(current_scene_item)
               current_scene_item = None
           
           if current_media_source:
               obs.obs_source_remove(current_media_source)
               current_media_source = None
           
           # Rust kaynağını göster
           rust_source = get_source_by_name("rust")
           if rust_source:
               obs.obs_source_set_enabled(rust_source, True)
               print("Rust kaynağı gösterildi")
       
       obs.obs_source_release(current_scene)
       is_showing = False
       
   except Exception as e:
       print(f"HATA (hide_media): {str(e)}")

def delayed_hide():
   global hide_timer
   if hide_timer:
       hide_timer.cancel()
   hide_timer = threading.Timer(DELAY, hide_media)
   hide_timer.start()

def on_press(key):
   try:
       if hasattr(key, 'char') and key.char and key.char.lower() == 'g':
           if not is_showing:  # Sadece gösterilmiyorsa yeni video göster
               print("G tuşuna basıldı")
               if hide_timer:
                   hide_timer.cancel()
               show_random_media()
   except Exception as e:
       print(f"HATA (on_press): {str(e)}")

def on_release(key):
   try:
       if hasattr(key, 'char') and key.char and key.char.lower() == 'g':
           print("G tuşu bırakıldı")
           delayed_hide()
   except Exception as e:
       print(f"HATA (on_release): {str(e)}")

def script_unload():
   global running
   running = False
   if hide_timer:
       hide_timer.cancel()
   listener.stop()
   key_thread.join()

# Tuş dinleyiciyi başlat
key_thread = Thread(target=lambda: keyboard.Listener(
   on_press=on_press,
   on_release=on_release).start(), 
   daemon=True)
key_thread.start()

print("Script başlatıldı ve çalışıyor...")