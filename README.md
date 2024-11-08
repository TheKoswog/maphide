# Rust OBS Eklentisi Kurulum Kılavuzu
![image](https://github.com/user-attachments/assets/70f13b91-1027-4389-ab95-63de6bbac0f1)


![image](https://github.com/user-attachments/assets/41c6d50a-2668-42e8-9fe0-3ac0bcc4aba7)
![image](https://github.com/user-attachments/assets/9ce34952-8621-455c-8be2-0286fe96bffc)



Bu OBS eklentisi, oyun sırasında "G" tuşuna basılı tutulduğunda rastgele video göstermeyi sağlar.

## Gereksinimler

- OBS Studio (En son sürüm)
- Python 3.6 veya üzeri
- pip (Python paket yöneticisi)

## Kurulum Adımları

### 1. Python Kurulumu

1. [Python'un resmi sitesinden](https://www.python.org/downloads/) Python 3.6 veya üzeri bir sürümü indirin ve kurun
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretlediğinizden emin olun

### 2. Gerekli Python Kütüphanelerinin Kurulumu

Komut istemini (CMD) yönetici olarak açın ve aşağıdaki komutu çalıştırın:

```bash
pip install pynput
```

### 3. OBS Scripts Klasörüne Kurulum

1. OBS Studio'yu açın
2. Üst menüden "Araçlar" > "Scripts" seçeneğine tıklayın
3. Scripts penceresinde "Python Settings" sekmesine geçin
4. Python yolunun doğru ayarlandığından emin olun

### 4. Eklenti Dosyalarının Yerleştirilmesi

1. `rust.py` dosyasını OBS'nin scripts klasörüne kopyalayın
   - Windows: `%APPDATA%\obs-studio\scripts\`
   - Linux: `~/.config/obs-studio/scripts/`
   - macOS: `~/Library/Application Support/obs-studio/scripts/`

2. Scripts klasörü içinde `videos` adında bir klasör oluşturun
3. `videos` klasörüne göstermek istediğiniz MP4 formatındaki videoları yerleştirin

### 5. OBS Sahne Ayarları

1. OBS'de "rust" adında bir kaynak oluşturun (Oyun yakalama veya ekran yakalama)
2. Script'i OBS'ye eklemek için:
   - Araçlar > Scripts menüsüne gidin
   - "+" butonuna tıklayın
   - `rust.py` dosyasını seçin

## Kullanım

- Oyun sırasında "G" tuşuna basılı tuttuğunuzda rastgele bir video gösterilecektir
- Tuşu bıraktığınızda video kaybolup normal oyun görüntüsüne dönecektir

## Önemli Notlar

- Video dosyalarınız MP4 formatında olmalıdır
- Varsayılan video boyutları 2560x1440 pikseldir
- Farklı boyutlar için `VIDEO_WIDTH` ve `VIDEO_HEIGHT` değişkenlerini `rust.py` dosyasında düzenleyebilirsiniz

## Sorun Giderme

1. **Script çalışmıyorsa:**
   - Python'un doğru kurulduğundan emin olun
   - OBS'de Python yolunun doğru ayarlandığını kontrol edin
   - `pynput` kütüphanesinin kurulu olduğunu kontrol edin

2. **Videolar gösterilmiyorsa:**
   - `videos` klasörünün doğru konumda olduğunu kontrol edin
   - Video dosyalarının MP4 formatında olduğunu doğrulayın
   - OBS konsolunda hata mesajları olup olmadığını kontrol edin

## Güvenlik Notu

Bu script, klavye girişlerini dinlediği için bazı anti-virüs yazılımları tarafından yanlış algılanabilir. Güvenilir kaynaklardan indirdiğinizden emin olun.
