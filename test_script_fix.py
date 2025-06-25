#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Kaldırma Test
Düzeltilmiş script kaldırma fonksiyonunu test eder
"""

from postman_collection_editor import PostmanCollectionEditor

def test_script_detection():
    """Script tespit etme ve kaldırma işlemini test et"""
    
    collection_file = "collection (2).json"
    
    print("🧪 Script Kaldırma Test Başlıyor...")
    print("=" * 50)
    
    editor = PostmanCollectionEditor(collection_file)
    
    if not editor.load_collection():
        print("❌ Collection yüklenemedi!")
        return
    
    print("✅ Collection yüklendi!")
    
    # 1. Önce scriptleri listele
    print("\n🔍 1. ADIM: Mevcut scriptleri listele")
    print("-" * 30)
    scripts_before = editor.list_scripts_in_collection()
    
    if not scripts_before:
        print("❗ Hiç script bulunamadı. Test edilecek bir şey yok.")
        return
    
    # 2. Yedek oluştur
    print("\n💾 2. ADIM: Yedek oluştur")
    print("-" * 30)
    editor.create_backup()
    
    # 3. Scriptleri kaldır
    print("\n🗑️ 3. ADIM: Scriptleri kaldır")
    print("-" * 30)
    removed_count = editor.remove_all_scripts()
    
    # 4. Tekrar listele (boş olmalı)
    print("\n🔍 4. ADIM: Kaldırma sonrası kontrol")
    print("-" * 30)
    scripts_after = editor.list_scripts_in_collection()
    
    # 5. Sonuçları değerlendir
    print("\n📊 TEST SONUÇLARI:")
    print("=" * 50)
    print(f"🔢 Başlangıçta script bulunan request sayısı: {len(scripts_before)}")
    print(f"🗑️ Kaldırılan request sayısı: {removed_count}")
    print(f"🔢 Kaldırma sonrası script bulunan request sayısı: {len(scripts_after)}")
    
    if len(scripts_after) == 0 and removed_count > 0:
        print("✅ TEST BAŞARILI: Tüm scriptler kaldırıldı!")
    elif len(scripts_after) == 0 and removed_count == 0:
        print("⚠️ Hiç script bulunamadı veya kaldırılamadı")
    else:
        print("❌ TEST BAŞARISIZ: Bazı scriptler kaldırılamadı!")
        print("\n🔍 Kaldırılamayan scriptler:")
        for item in scripts_after:
            print(f"   • {item['name']}: {', '.join(item['scripts'])}")
    
    # 6. Güncellenmiş dosyayı kaydet
    if removed_count > 0:
        output_file = "collection_scripts_removed.json"
        editor.save_collection(output_file)
        print(f"\n💾 Güncellenmiş collection kaydedildi: {output_file}")
    
    print("\n🎉 Test tamamlandı!")

if __name__ == "__main__":
    test_script_detection() 