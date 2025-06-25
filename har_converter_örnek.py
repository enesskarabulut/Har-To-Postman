#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HAR to Postman Converter - Örnek Kullanım
Bu dosya HAR converter'ın nasıl kullanılacağını gösterir.
"""

from har_to_postman import har_to_postman_collection, create_collection_from_har
import json

def example_usage():
    """HAR converter'ın örnek kullanımları"""
    print("🚀 HAR to Postman Converter - Örnek Kullanımlar")
    print("=" * 60)
    
    # Örnek 1: Basit kullanım
    print("\n📋 Örnek 1: Basit HAR Çevirme")
    print("-" * 30)
    
    har_file = "example.har"  # HAR dosyasının yolu
    
    # HAR dosyası var mı kontrol et
    import os
    if not os.path.exists(har_file):
        print(f"⚠️  HAR dosyası bulunamadı: {har_file}")
        print("💡 Önce tarayıcınızdan bir HAR dosyası export edin:")
        print("   1. Chrome/Firefox'ta F12'ye basın")
        print("   2. Network sekmesine gidin")
        print("   3. Sayfayı yenileyin veya API istekleri yapın")
        print("   4. Network sekmesinde sağ tık → 'Save all as HAR with content'")
        print("   5. Dosyayı 'example.har' olarak kaydedin")
        return
    
    # Collection oluştur ve kaydet
    success = create_collection_from_har(
        har_file_path=har_file,
        output_path="my_api_collection.json",
        collection_name="My Website API Collection"
    )
    
    if success:
        print("✅ Collection başarıyla oluşturuldu!")
    else:
        print("❌ Collection oluşturulamadı!")
    
    print("\n📋 Örnek 2: Collection Objesi Almak")
    print("-" * 30)
    
    # Collection objesini al (kaydetmeden)
    collection = har_to_postman_collection(har_file, "Test Collection")
    
    if collection:
        print(f"✅ Collection oluşturuldu: {collection['info']['name']}")
        print(f"📊 Toplam folder sayısı: {len(collection['item'])}")
        
        # Domain'leri listele
        for folder in collection['item']:
            request_count = len(folder.get('item', []))
            print(f"   🌐 {folder['name']}: {request_count} istek")
    else:
        print("❌ Collection oluşturulamadı!")
    
    print("\n📋 Örnek 3: Collection'ı Manuel Kaydetme")
    print("-" * 30)
    
    if collection:
        # JSON string'e çevir
        collection_json = json.dumps(collection, indent=2, ensure_ascii=False)
        
        # Dosyaya kaydet
        with open("manual_collection.json", "w", encoding="utf-8") as f:
            f.write(collection_json)
        
        print("✅ Collection manuel olarak kaydedildi: manual_collection.json")

def analyze_har_file(har_file_path: str):
    """HAR dosyasını analiz eder"""
    print(f"\n🔍 HAR Dosyası Analizi: {har_file_path}")
    print("-" * 50)
    
    try:
        with open(har_file_path, 'r', encoding='utf-8') as f:
            har_data = json.load(f)
        
        if 'log' not in har_data or 'entries' not in har_data['log']:
            print("❌ Geçersiz HAR dosyası formatı")
            return
        
        entries = har_data['log']['entries']
        
        # İstatistikler
        print(f"📊 Toplam HTTP İsteği: {len(entries)}")
        
        # Method'ları say
        methods = {}
        domains = {}
        content_types = {}
        
        for entry in entries:
            if 'request' not in entry:
                continue
            
            request = entry['request']
            
            # Method istatistiği
            method = request.get('method', 'UNKNOWN')
            methods[method] = methods.get(method, 0) + 1
            
            # Domain istatistiği
            url = request.get('url', '')
            if url:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                domains[domain] = domains.get(domain, 0) + 1
            
            # Content-Type istatistiği
            headers = request.get('headers', [])
            for header in headers:
                if header.get('name', '').lower() == 'content-type':
                    ct = header.get('value', '').split(';')[0]
                    content_types[ct] = content_types.get(ct, 0) + 1
        
        # Sonuçları göster
        print("\n🌐 HTTP Method Dağılımı:")
        for method, count in sorted(methods.items()):
            print(f"   {method}: {count}")
        
        print("\n🏠 Domain Dağılımı:")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {domain}: {count}")
        
        if content_types:
            print("\n📄 Content-Type Dağılımı:")
            for ct, count in sorted(content_types.items(), key=lambda x: x[1], reverse=True):
                if ct:  # Boş olmayan content-type'ları göster
                    print(f"   {ct}: {count}")
        
    except Exception as e:
        print(f"❌ HAR dosyası analiz edilirken hata: {e}")

def interactive_converter():
    """İnteraktif HAR converter"""
    print("\n🎯 İnteraktif HAR Converter")
    print("-" * 30)
    
    har_file = input("HAR dosyasının yolu: ").strip()
    if not har_file:
        print("❌ HAR dosya yolu boş olamaz!")
        return
    
    import os
    if not os.path.exists(har_file):
        print(f"❌ HAR dosyası bulunamadı: {har_file}")
        return
    
    # Önce analiz yap
    analyze_har_file(har_file)
    
    # Collection bilgilerini al
    collection_name = input("\nCollection adı (boş bırakırsanız otomatik verilir): ").strip()
    output_file = input("Çıktı dosyası (boş bırakırsanız otomatik verilir): ").strip()
    
    print("\n🔄 HAR dosyası çevriliyor...")
    
    success = create_collection_from_har(
        har_file,
        output_file if output_file else None,
        collection_name if collection_name else None
    )
    
    if success:
        print("\n🎉 HAR başarıyla Postman collection'ına çevrildi!")
        print("📥 Artık bu dosyayı Postman'e import edebilirsiniz.")
        
        print("\n💡 Postman'e import etmek için:")
        print("   1. Postman'i açın")
        print("   2. 'Import' butonuna tıklayın")
        print("   3. Oluşturulan JSON dosyasını seçin")
        print("   4. 'Import' butonuna tıklayın")
    else:
        print("\n❌ Çevirme işlemi başarısız oldu!")

if __name__ == "__main__":
    # Hangi örneği çalıştırmak istediğinizi seçin
    print("🚀 HAR to Postman Converter")
    print("=" * 40)
    print("1. Örnek kullanımları göster")
    print("2. HAR dosyası analizi yap")
    print("3. İnteraktif converter")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == "1":
        example_usage()
    elif choice == "2":
        har_file = input("HAR dosyasının yolu: ").strip()
        if har_file:
            analyze_har_file(har_file)
        else:
            print("❌ HAR dosya yolu boş olamaz!")
    elif choice == "3":
        interactive_converter()
    else:
        print("❌ Geçersiz seçim!") 