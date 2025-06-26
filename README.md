# 🚀 Postman Collection Düzenleyici

Web tabanlı Postman collection düzenleme aracı. HAR dosyalarını Postman collection'larına çevirme ve mevcut collection'ları düzenleme özellikleri sunar.

## ✨ Özellikler

### 📁 **Collection İşlemleri**
- ✅ Postman collection JSON dosyalarını yükleme
- ✅ Collection bilgilerini görüntüleme
- ✅ Yedek oluşturma ve geri yükleme

### 🔧 **Header İşlemleri**
- ➕ Tüm requestlere header ekleme
- 🗑️ Belirli header'ı tüm requestlerden kaldırma
- ✏️ Tek tek header düzenleme

### 📄 **Body Düzenleme**
- 📝 Raw body düzenleme (JSON, XML, Text)
- 🎨 JSON/XML beautify (formatlama)
- ⚡ Code minify (sıkıştırma)
- 📊 Form data düzenleme

### 📜 **Script Yönetimi**
- 🗑️ Tüm pre-request ve test scriptlerini kaldırma
- ✏️ Script düzenleme ve ekleme

### 📝 **Genel Düzenleme**
- 🔄 Metin değiştirme (URL, header, body)
- ⚙️ Environment variable ekleme
- 🔍 Endpoint detayları görüntüleme ve düzenleme

### 🔄 **HAR Converter**
- 📥 HAR dosyalarını Postman collection'a çevirme
- 🌐 Domain bazlı gruplama
- 📊 Otomatik istatistik hesaplama

## 🚀 Hızlı Başlangıç

### 📋 Gereksinimler
- Python 3.8+
- pip

### 🔧 Kurulum

```bash
# Repository'yi klonlayın
git clone <repository-url>
cd hartopostman

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
streamlit run postman_web_app.py
```

### 💻 Komut Satırı Kullanımı

```bash
# CLI arayüzü
python postman_collection_editor.py

# Tkinter GUI
python postman_gui_tkinter.py
```

## 📱 Web Arayüzü

1. **📁 Collection Yükle**: Sol sidebar'dan JSON dosyasını yükleyin
2. **🔧 İşlem Seç**: Üst sekmelerden yapmak istediğiniz işlemi seçin
3. **✏️ Düzenle**: Endpoint detaylarında değişiklik yapın
4. **💾 Kaydet**: İşlemlerinizi tamamlayıp indirin

## 🔧 Desteklenen Formatlar

### 📥 Girdi
- `.json` - Postman Collection v2.1+
- `.har` - HTTP Archive files

### 📤 Çıktı
- `.json` - Güncellenmiş Postman Collection

## 📖 Kullanım Örnekleri

### HAR'dan Collection Oluşturma
```python
from postman_collection_editor import PostmanCollectionEditor

# HAR dosyasını çevir
success = PostmanCollectionEditor.create_collection_from_har(
    "network_requests.har",
    "api_collection.json",
    "My API Collection"
)
```

### Toplu Header Ekleme
```python
editor = PostmanCollectionEditor("collection.json")
editor.load_collection()

# Tüm requestlere Authorization header ekle
editor.add_header_to_all_requests("Authorization", "Bearer TOKEN")
editor.save_collection()
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Destek

Sorunlar için GitHub Issues kullanın. 