# 🚀 Vercel'e Deployment Rehberi

Bu rehber Postman Collection Düzenleyici uygulamasını Vercel'e nasıl deploy edeceğinizi anlatır.

## 📋 Gereksinimler

- ✅ GitHub hesabı
- ✅ Vercel hesabı (GitHub ile bağlantılı)
- ✅ Bu proje dosyaları

## 📁 Deployment Dosyaları

Deployment için gerekli dosyalar otomatik oluşturuldu:

- `requirements.txt` - Python bağımlılıkları
- `vercel.json` - Vercel konfigürasyonu  
- `streamlit_app.py` - Ana giriş noktası
- `.vercelignore` - Hariç tutulacak dosyalar

## 🔧 Deployment Adımları

### 1. GitHub Repository Oluştur

```bash
# Proje klasöründe
git init
git add .
git commit -m "Initial commit with Vercel deployment files"

# GitHub'da yeni repo oluşturun ve push edin
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git branch -M main
git push -u origin main
```

### 2. Vercel'e Deploy Et

#### Option A: Vercel Dashboard ile
1. [vercel.com](https://vercel.com)'a gidin
2. GitHub ile giriş yapın
3. "New Project" tıklayın
4. GitHub repo'nuzu seçin
5. "Deploy" butonuna tıklayın

#### Option B: Vercel CLI ile
```bash
# Vercel CLI yükle
npm i -g vercel

# Deploy et
vercel

# Production deploy
vercel --prod
```

### 3. Environment Variables (Opsiyonel)

Vercel Dashboard'da Environment Variables ekleyebilirsiniz:
- `STREAMLIT_SERVER_PORT` → `8501`
- `STREAMLIT_SERVER_ADDRESS` → `0.0.0.0`

## 🎯 Deployment URL'si

Deploy tamamlandıktan sonra Vercel size bir URL verecek:
```
https://your-app-name.vercel.app
```

## ⚡ Özelliklerin Durumu

### ✅ Çalışan Özellikler:
- HAR to Postman converter
- Collection düzenleme (header, URL, metin değiştirme)
- Script temizleme
- Environment variables
- Endpoint listeleme ve silme
- Web arayüzü tam fonksiyonel

### ⚠️ Sınırlamalar:
- **Dosya yükleme**: Vercel'de geçici dosyalar 512MB ile sınırlı
- **İşlem süresi**: Maksimum 30 saniye timeout
- **Memory**: Serverless function'lar için memory sınırı

## 🔄 Otomatik Deployment

GitHub'a her push yaptığınızda Vercel otomatik deploy eder:

```bash
git add .
git commit -m "Feature: Yeni özellik eklendi"
git push
```

## 🐛 Troubleshooting

### Build Hatası
```bash
# Local'de test edin
streamlit run postman_web_app.py
```

### Import Hatası
- `requirements.txt`'i kontrol edin
- Gerekli kütüphaneleri ekleyin

### Timeout Hatası
- Büyük HAR dosyaları için local kullanım önerilir
- `vercel.json`'da `maxDuration` değerini artırın

## 📊 Performance Tips

1. **Hafif dosyalar**: Büyük HAR dosyaları local'de işleyin
2. **Cache**: Session state ile cache kullanımı
3. **Lazy loading**: Büyük collection'lar için sayfalama

## 🔒 Güvenlik

- API key'leri environment variables'da saklayın
- Sensitive data'yı repository'ye eklemeyin
- Production'da HTTPS kullanın

## 📞 Destek

Deploy sırasında sorun yaşarsanız:
1. Vercel logs'larını kontrol edin
2. GitHub Actions'ları kontrol edin
3. Local'de test edin

---

🎉 **Tebrikler!** Uygulamanız artık Vercel'de live!

Access URL: `https://your-app-name.vercel.app` 