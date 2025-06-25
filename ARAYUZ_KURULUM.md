# 🖥️ Postman Collection Düzenleyici - Arayüz Kullanım Rehberi

Size iki farklı arayüz seçeneği sunuyorum:

## 1. 🖥️ Masaüstü GUI (Tkinter) - Önerilen

### Kurulum
```bash
# Ek kurulum gerekmez - Python ile birlikte gelir
python postman_gui.py
```

### Özellikler
- ✅ Kolay kullanım
- ✅ Gerçek zamanlı endpoint görüntüleme
- ✅ Dosya seçme/kaydetme dialog'ları
- ✅ Progress bar'lar ve status mesajları
- ✅ Ek kütüphane gerektirmez

### Ekran Görüntüsü Açıklaması
```
┌─────────────────────────────────────────────────────────────┐
│ 🚀 Postman Collection Düzenleyici                          │
├─────────────────────────────────────────────────────────────┤
│ 📁 Collection Dosyası                                       │
│ [Dosya Yolu________________] [Dosya Seç] [Yükle]           │
├─────────────────────────────────────────────────────────────┤
│ 📊 Collection Bilgileri                                     │
│ [Bilgi Text Area]                                          │
├──────────────────────────┬──────────────────────────────────┤
│ 🛠️ İşlemler               │ 📋 Endpoint'ler                  │
│                          │                                  │
│ Header İşlemleri         │ [Method] [Name] [URL]            │
│ [Ad] [Değer] [Ekle]      │ GET     Users   /api/users       │
│ [Ad] [Kaldır]            │ POST    Login   /api/auth        │
│                          │ ...                              │
│ URL İşlemleri            │                                  │
│ [Eski] [Yeni] [Güncelle] │                                  │
│                          │                                  │
│ Metin Değiştirme         │                                  │
│ [Eski] [Yeni] [Değiştir] │                                  │
│                          │                                  │
│ Environment Variable     │                                  │
│ [Ad] [Değer] [Ekle]      │                                  │
└──────────────────────────┴──────────────────────────────────┘
│ [Scriptleri Kaldır] [Yenile] [Yedek] [Kaydet] [Farklı]    │
├─────────────────────────────────────────────────────────────┤
│ Status: Collection yüklendi - 25 request bulundu           │
└─────────────────────────────────────────────────────────────┘
```

## 2. 🌐 Web Arayüzü (Streamlit)

### Kurulum
```bash
# Streamlit kurulumu gerekli
pip install streamlit pandas

# Çalıştırma
streamlit run postman_web_app.py
```

### Özellikler
- ✅ Modern web arayüzü
- ✅ Responsive tasarım
- ✅ Dosya drag & drop
- ✅ Filtreleme ve arama
- ✅ Direkt indirme butonu
- ✅ Tarayıcıdan kullanım

### Web Arayüzü Özellikleri
```
📱 Tarayıcı Arayüzü:
├── 📁 Sidebar: Dosya yükleme ve collection bilgileri
├── 🔧 Tab 1: Header İşlemleri
├── 🌐 Tab 2: URL İşlemleri  
├── 📝 Tab 3: Metin Değiştirme
├── 🗑️ Tab 4: Script Temizleme
├── ⚙️ Tab 5: Environment Variables
└── 📋 Tab 6: Endpoint Listesi (filtrelenebilir)
```

## 🚀 Hızlı Başlangıç

### Masaüstü GUI ile:
```bash
# 1. Çalıştır
python postman_gui.py

# 2. "Dosya Seç" -> collection (2).json
# 3. "Yükle" butonuna tıkla
# 4. İstediğin işlemi yap
# 5. "Kaydet" veya "Farklı Kaydet"
```

### Web Arayüzü ile:
```bash
# 1. Streamlit'i başlat
streamlit run postman_web_app.py

# 2. Tarayıcıda açılan adresi ziyaret et
# 3. Sol panelden dosya yükle
# 4. Tab'lardan işlemlerini yap
# 5. "İndir" butonuyla dosyayı al
```

## 🎯 Hangi Arayüzü Seçmeliyim?

### Masaüstü GUI seçin eğer:
- ❇️ Ek kurulum yapmak istemiyorsanız
- ❇️ Hızlı ve responsive bir arayüz istiyorsanız
- ❇️ Dosya sistem entegrasyonu önemliyse

### Web Arayüzü seçin eğer:
- 🌐 Modern web arayüzü istiyorsanız
- 🌐 Uzaktan erişim gerekiyorsa
- 🌐 Birden fazla kişi kullanacaksa
- 🌐 Tablet/telefon desteği istiyorsanız

## 🛠️ Sorun Giderme

### Masaüstü GUI Sorunları:
```bash
# Tkinter eksikse (Linux'ta):
sudo apt-get install python3-tk

# Çalıştırma hatası:
python3 postman_gui.py
```

### Web Arayüzü Sorunları:
```bash
# Streamlit kurulumu:
pip install streamlit==1.28.1 pandas

# Port değiştirme:
streamlit run postman_web_app.py --server.port 8080

# Tarayıcı açılmazsa:
# Manuel olarak http://localhost:8501 adresini ziyaret edin
```

## 💡 Kullanım İpuçları

### Genel:
1. **Yedek Oluşturun**: Her işlem öncesi mutlaka yedek alın
2. **Test Edin**: Küçük bir collection ile önce test yapın
3. **Adım Adım**: Büyük değişiklikleri parçalara bölerek yapın

### Masaüstü GUI:
- Dosya dialog'ları ile kolay dosya seçimi
- Status bar'dan işlem durumunu takip edin
- Endpoint listesi otomatik güncellenir

### Web Arayüzü:
- Drag & drop ile dosya yükleme
- Tab'lar arası geçiş ile organize çalışma
- Filtreleme özelliklerini kullanın

## 🔧 Gelişmiş Özellikler

Her iki arayüz de şu işlemleri destekler:
- ✅ Header ekleme/çıkarma
- ✅ URL güncelleme  
- ✅ Metin değiştirme
- ✅ Script temizleme
- ✅ Environment variable ekleme
- ✅ Endpoint listeleme
- ✅ Yedekleme
- ✅ Farklı kaydetme

---

**🎉 İyi kullanımlar! Herhangi bir sorun yaşarsanız README.md dosyasındaki destek bilgilerini inceleyin.** 