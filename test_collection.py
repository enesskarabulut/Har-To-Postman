#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection Test Script
Collection dosyasını test etmek için
"""

import os
from postman_collection_editor import PostmanCollectionEditor

def test_collection():
    """Collection dosyasını test et"""
    
    collection_file = "collection (2).json"
    
    print("🧪 Postman Collection Test Başlıyor...")
    print("=" * 50)
    
    # Dosya kontrolü
    if not os.path.exists(collection_file):
        print(f"❌ Collection dosyası bulunamadı: {collection_file}")
        print("   Lütfen collection dosyasının bu klasörde olduğundan emin olun.")
        return False
    
    try:
        # Collection yükle
        editor = PostmanCollectionEditor(collection_file)
        
        if not editor.load_collection():
            print("❌ Collection yüklenemedi!")
            return False
        
        print("✅ Collection başarıyla yüklendi!")
        
        # Temel bilgileri göster
        print("\n📊 Collection Test Raporu:")
        editor.get_collection_info()
        
        # Endpoint sayısını say
        endpoints = editor.list_all_endpoints()
        print(f"✅ Toplam {len(endpoints)} endpoint bulundu")
        
        # İlk 5 endpoint'i göster
        if endpoints:
            print("\n📋 İlk 5 Endpoint:")
            for i, endpoint in enumerate(endpoints[:5], 1):
                print(f"   {i}. [{endpoint['method']:6s}] {endpoint['name']}")
        
        print("\n🎉 Test başarıyla tamamlandı!")
        print("\n💡 Şimdi şunları yapabilirsiniz:")
        print("   • python postman_collection_editor.py  (İnteraktif menü)")
        print("   • python postman_cli.py --help         (Command line yardım)")
        print("   • python örnek_kullanım.py             (Örnek kullanımlar)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {e}")
        return False

if __name__ == "__main__":
    success = test_collection()
    if not success:
        print("\n🔧 Sorun Giderme:")
        print("   1. Collection dosyasının doğru dizinde olduğundan emin olun")
        print("   2. Dosyanın geçerli JSON formatında olduğunu kontrol edin")
        print("   3. Dosya izinlerini kontrol edin")
        exit(1) 