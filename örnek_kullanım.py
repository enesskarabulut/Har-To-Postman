#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection Düzenleyici - Kullanım Örnekleri
"""

from postman_collection_editor import PostmanCollectionEditor

def örnek_kullanım():
    """Temel kullanım örnekleri"""
    
    # Collection dosyasını yükle
    editor = PostmanCollectionEditor("collection (2).json")
    
    if not editor.load_collection():
        print("Collection yüklenemedi!")
        return
    
    print("🚀 Postman Collection işlemleri başlıyor...")
    
    # 1. Collection hakkında bilgi al
    print("\n1️⃣ Collection Bilgileri:")
    editor.get_collection_info()
    
    # 2. Yedek oluştur
    print("\n2️⃣ Yedek oluşturuluyor...")
    editor.create_backup()
    
    # 3. Tüm endpoint'leri listele
    print("\n3️⃣ Endpoint'ler listeleniyor...")
    endpoints = editor.list_all_endpoints()
    
    # 4. Authorization header ekle
    print("\n4️⃣ Authorization header ekleniyor...")
    editor.add_header_to_all_requests("Authorization", "Bearer YOUR_TOKEN_HERE")
    
    # 5. Content-Type header ekle
    print("\n5️⃣ Content-Type header ekleniyor...")
    editor.add_header_to_all_requests("Content-Type", "application/json")
    
    # 6. Tüm scriptleri kaldır
    print("\n6️⃣ Scriptler kaldırılıyor...")
    editor.remove_all_scripts()
    
    # 7. Düzenlenmiş collection'ı kaydet
    print("\n7️⃣ Düzenlenmiş collection kaydediliyor...")
    editor.save_collection("collection_düzenlenmiş.json")
    
    print("\n🎉 İşlemler tamamlandı!")
    print("   - Orijinal dosya: collection (2).json")
    print("   - Düzenlenmiş dosya: collection_düzenlenmiş.json")
    print("   - Yedek dosya: collection (2).json.backup_[timestamp]")

def sadece_header_ekle():
    """Sadece header ekleme örneği"""
    editor = PostmanCollectionEditor("collection (2).json")
    
    if editor.load_collection():
        editor.create_backup()
        
        # API Key header ekle
        editor.add_header_to_all_requests("X-API-Key", "your-api-key-here")
        
        # User-Agent header ekle
        editor.add_header_to_all_requests("User-Agent", "MyApp/1.0")
        
        editor.save_collection()
        print("✅ Header'lar eklendi ve kaydedildi!")

def sadece_script_temizle():
    """Sadece script temizleme örneği"""
    editor = PostmanCollectionEditor("collection (2).json")
    
    if editor.load_collection():
        editor.create_backup()
        editor.remove_all_scripts()
        editor.save_collection()
        print("✅ Tüm scriptler temizlendi!")

if __name__ == "__main__":
    print("Hangi örneği çalıştırmak istiyorsunuz?")
    print("1. Tam özellikli örnek")
    print("2. Sadece header ekleme")
    print("3. Sadece script temizleme")
    
    seçim = input("Seçiminiz (1-3): ").strip()
    
    if seçim == "1":
        örnek_kullanım()
    elif seçim == "2":
        sadece_header_ekle()
    elif seçim == "3":
        sadece_script_temizle()
    else:
        print("Geçersiz seçim!") 