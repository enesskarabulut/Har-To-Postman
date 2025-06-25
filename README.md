# 🚀 Postman Collection Düzenleyici

Postman collection JSON dosyalarınızda toplu düzenlemeler yapmanızı sağlayan kapsamlı Python araç seti.

## 📋 Özellikler

- ✅ **Header Yönetimi**: Tüm requestlere header ekleme/çıkarma
- ✅ **Script Temizleme**: Pre-request ve test scriptlerini toplu kaldırma
- ✅ **URL Güncelleme**: Base URL'leri toplu değiştirme
- ✅ **Metin Değiştirme**: URL, body ve header değerlerinde metin değiştirme
- ✅ **Environment Variables**: Collection seviyesinde değişken ekleme
- ✅ **Endpoint Silme**: İsim, method veya URL pattern'ına göre endpoint silme
- ✅ **HAR Converter**: HAR dosyalarını Postman collection'ına çevirme
- ✅ **Yedekleme**: Otomatik yedek oluşturma
- ✅ **Endpoint Listeleme**: Tüm API endpoint'lerini görüntüleme
- ✅ **İnteraktif Menü**: Kullanımı kolay arayüz
- ✅ **Command Line**: Otomasyon için CLI desteği

## 📁 Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `postman_collection_editor.py` | Ana kütüphane ve interaktif menü |
| `postman_cli.py` | Command line interface |
| `har_to_postman.py` | HAR dosyalarını Postman collection'a çevirme |
| `har_converter_örnek.py` | HAR converter kullanım örnekleri |
| `örnek_kullanım.py` | Kullanım örnekleri |

## 🎯 Kullanım

### 1. İnteraktif Menü ile Kullanım

```bash
python postman_collection_editor.py
```

Menüden istediğiniz işlemi seçebilirsiniz:

```
İşlem seçiniz:
1. Collection bilgilerini göster
2. Tüm endpoint'leri listele
3. Tüm requestlere header ekle
4. Tüm requestlerden header kaldır
5. Tüm scriptleri kaldır
6. Base URL güncelle
7. Environment variable ekle
8. Metin değiştir (URL/Body/Header)
9. Yedek oluştur
10. Collection'ı kaydet
0. Çıkış
```

### 2. Command Line ile Kullanım

#### Collection bilgilerini görüntüle
```bash
python postman_cli.py "collection (2).json" --info
```

#### Tüm endpoint'leri listele
```bash
python postman_cli.py "collection (2).json" --list-endpoints
```

#### Authorization header ekle
```bash
python postman_cli.py "collection (2).json" --add-header "Authorization" "Bearer YOUR_TOKEN" --backup
```

#### Content-Type header ekle
```bash
python postman_cli.py "collection (2).json" --add-header "Content-Type" "application/json"
```

#### Tüm scriptleri kaldır
```bash
python postman_cli.py "collection (2).json" --remove-scripts --backup
```

#### Base URL güncelle
```bash
python postman_cli.py "collection (2).json" --update-url "https://old-api.com" "https://new-api.com"
```

#### Metin değiştir
```bash
python postman_cli.py "collection (2).json" --replace-text "localhost:3000" "api.example.com"
```

#### Environment variable ekle
```bash
python postman_cli.py "collection (2).json" --add-variable "API_BASE_URL" "https://api.example.com"
```

#### Birden fazla işlemi birlikte yap
```bash
python postman_cli.py "collection (2).json" \
  --add-header "Authorization" "Bearer TOKEN" \
  --add-header "Content-Type" "application/json" \
  --remove-scripts \
  --backup \
  --output "updated_collection.json"
```

### 3. HAR to Postman Converter

#### HAR dosyasını Postman collection'a çevir
```bash
# Basit kullanım
python har_to_postman.py example.har

# Özel çıktı dosyası ile
python har_to_postman.py example.har my_collection.json

# Özel collection adı ile
python har_to_postman.py example.har my_collection.json "My API Collection"
```

#### HAR dosyası nasıl elde edilir?
1. Chrome/Firefox'ta F12'ye basın (Developer Tools)
2. Network sekmesine gidin
3. Sayfayı yenileyin veya API istekleri yapın
4. Network sekmesinde sağ tık → 'Save all as HAR with content'
5. HAR dosyasını kaydedin

#### İnteraktif HAR converter
```bash
python har_converter_örnek.py
```

### 4. Python Script ile Kullanım

```python
from postman_collection_editor import PostmanCollectionEditor

# Collection yükle
editor = PostmanCollectionEditor("collection (2).json")
editor.load_collection()

# Yedek oluştur
editor.create_backup()

# Authorization header ekle
editor.add_header_to_all_requests("Authorization", "Bearer YOUR_TOKEN")

# Tüm scriptleri kaldır
editor.remove_all_scripts()

# Kaydet
editor.save_collection("updated_collection.json")
```

#### HAR Converter ile
```python
from har_to_postman import create_collection_from_har

# HAR'ı Postman collection'a çevir
success = create_collection_from_har(
    har_file_path="network_traffic.har",
    output_path="api_collection.json",
    collection_name="Website API Collection"
)

if success:
    print("✅ HAR başarıyla çevrildi!")
```

## 🛠️ Kurulum

Python 3.6+ gereklidir. Ek kütüphane kurulumu gerekmez, sadece standart Python kütüphaneleri kullanılır.

```bash
# Dosyaları indirin
git clone https://github.com/your-repo/postman-collection-editor.git
cd postman-collection-editor

# Çalıştırın
python postman_collection_editor.py
```

## 📊 Örnek Senaryolar

### Senaryo 1: API Token Güncelleme
```bash
# Eski token'ları değiştir
python postman_cli.py "collection.json" \
  --replace-text "old-token-123" "new-token-456" \
  --backup
```

### Senaryo 2: Development'tan Production'a Geçiş
```bash
# URL'leri güncelle ve authorization ekle
python postman_cli.py "collection.json" \
  --update-url "http://localhost:3000" "https://api.production.com" \
  --add-header "Authorization" "Bearer PROD_TOKEN" \
  --remove-scripts \
  --output "production_collection.json" \
  --backup
```

### Senaryo 3: Collection Temizleme
```bash
# Scriptleri kaldır ve gereksiz header'ları temizle
python postman_cli.py "collection.json" \
  --remove-scripts \
  --remove-header "X-Debug" \
  --remove-header "X-Test-Mode" \
  --backup
```

### Senaryo 4: HAR'dan Collection Oluşturma
```bash
# Web sitesinden HAR export edin ve Postman collection'a çevirin
python har_to_postman.py "website_traffic.har" "api_collection.json" "Website API Collection"

# Sonra collection'ı düzenleyin
python postman_cli.py "api_collection.json" \
  --add-header "Authorization" "Bearer YOUR_TOKEN" \
  --remove-scripts \
  --backup
```

## ⚠️ Güvenlik Notları

- **Yedekleme**: Önemli değişiklikler yapmadan önce mutlaka `--backup` kullanın
- **Token'lar**: API token'larını güvenli şekilde saklayın
- **Versiyon Kontrolü**: Collection dosyalarınızı git ile takip edin

## 🔧 Gelişmiş Özellikler

### Yedek Dosyaları
Yedek dosyalar otomatik olarak `dosya_adı.json.backup_YYYYMMDD_HHMMSS` formatında oluşturulur.

### Hata Yönetimi
Tüm işlemler try-catch bloklarıyla korunmuştur ve detaylı hata mesajları verilir.

### Büyük Dosya Desteği
2MB+ dosyalar için optimize edilmiştir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🆘 Destek

Sorun yaşıyorsanız:
1. [Issues](https://github.com/your-repo/issues) sayfasından yeni bir issue açın
2. Hata mesajının tam metnini paylaşın
3. Kullandığınız komut satırını ekleyin

---

**💡 İpucu**: Collection'ınızda çok sayıda request varsa, önce `--info` ve `--list-endpoints` ile genel bakış alın! 