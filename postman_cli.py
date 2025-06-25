#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection CLI Tool
Command line arayüzü ile collection düzenleme
"""

import argparse
import sys
from postman_collection_editor import PostmanCollectionEditor

def main():
    parser = argparse.ArgumentParser(
        description='Postman Collection düzenleyici - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Kullanım Örnekleri:
  # Collection bilgilerini göster
  python postman_cli.py "collection (2).json" --info
  
  # Endpoint'leri listele
  python postman_cli.py "collection (2).json" --list-endpoints
  
  # Authorization header ekle
  python postman_cli.py "collection (2).json" --add-header Authorization "Bearer TOKEN" --backup
  
  # Tüm scriptleri kaldır
  python postman_cli.py "collection (2).json" --remove-scripts --backup
  
  # Base URL güncelle
  python postman_cli.py "collection (2).json" --update-url "https://old-api.com" "https://new-api.com"
  
  # Metin değiştir
  python postman_cli.py "collection (2).json" --replace-text "old-text" "new-text"
  
  # Birden fazla işlemi birlikte yap
  python postman_cli.py "collection (2).json" --add-header "Content-Type" "application/json" --remove-scripts --backup --output "new_collection.json"
        '''
    )
    
    # Ana argümanlar
    parser.add_argument('collection', help='Collection JSON dosyası yolu')
    parser.add_argument('--backup', action='store_true', help='İşlem öncesi yedek oluştur')
    parser.add_argument('--output', '-o', help='Çıktı dosyası yolu (belirtilmezse orijinal dosya güncellenir)')
    
    # Bilgi alma işlemleri
    info_group = parser.add_argument_group('Bilgi Alma')
    info_group.add_argument('--info', action='store_true', help='Collection bilgilerini göster')
    info_group.add_argument('--list-endpoints', action='store_true', help='Tüm endpoint\'leri listele')
    
    # Header işlemleri
    header_group = parser.add_argument_group('Header İşlemleri')
    header_group.add_argument('--add-header', nargs=2, metavar=('NAME', 'VALUE'), 
                             help='Tüm requestlere header ekle')
    header_group.add_argument('--remove-header', metavar='NAME', 
                             help='Tüm requestlerden header kaldır')
    
    # Script işlemleri
    script_group = parser.add_argument_group('Script İşlemleri')
    script_group.add_argument('--remove-scripts', action='store_true', 
                             help='Tüm pre-request ve test scriptlerini kaldır')
    
    # URL işlemleri
    url_group = parser.add_argument_group('URL İşlemleri')
    url_group.add_argument('--update-url', nargs=2, metavar=('OLD_URL', 'NEW_URL'), 
                          help='Base URL güncelle')
    
    # Metin değiştirme
    text_group = parser.add_argument_group('Metin İşlemleri')
    text_group.add_argument('--replace-text', nargs=2, metavar=('OLD_TEXT', 'NEW_TEXT'), 
                           help='Tüm requestlerde metin değiştir')
    
    # Environment variable
    env_group = parser.add_argument_group('Environment Variable')
    env_group.add_argument('--add-variable', nargs=2, metavar=('NAME', 'VALUE'), 
                          help='Collection seviyesinde environment variable ekle')
    
    args = parser.parse_args()
    
    # Collection editor oluştur
    try:
        editor = PostmanCollectionEditor(args.collection)
    except Exception as e:
        print(f"❌ Hata: {e}")
        return 1
    
    # Collection'ı yükle
    if not editor.load_collection():
        return 1
    
    # Yedek oluştur
    if args.backup:
        if not editor.create_backup():
            print("⚠️  Yedek oluşturulamadı, devam ediliyor...")
    
    # Bilgi göster
    if args.info:
        editor.get_collection_info()
    
    # Endpoint'leri listele
    if args.list_endpoints:
        editor.list_all_endpoints()
    
    # İşlemleri gerçekleştir
    changes_made = False
    
    try:
        if args.add_header:
            count = editor.add_header_to_all_requests(args.add_header[0], args.add_header[1])
            changes_made = True
            print(f"✅ {count} request'e header eklendi")
        
        if args.remove_header:
            count = editor.remove_header_from_all_requests(args.remove_header)
            changes_made = True
            print(f"✅ {count} request'ten header kaldırıldı")
        
        if args.remove_scripts:
            count = editor.remove_all_scripts()
            changes_made = True
            print(f"✅ {count} request'ten scriptler kaldırıldı")
        
        if args.update_url:
            count = editor.update_base_url(args.update_url[0], args.update_url[1])
            changes_made = True
            print(f"✅ {count} request'te URL güncellendi")
        
        if args.replace_text:
            count = editor.replace_text_in_requests(args.replace_text[0], args.replace_text[1])
            changes_made = True
            print(f"✅ {count} request'te metin değiştirildi")
        
        if args.add_variable:
            editor.add_environment_variable(args.add_variable[0], args.add_variable[1])
            changes_made = True
        
        # Değişiklikler varsa kaydet
        if changes_made:
            if editor.save_collection(args.output):
                output_file = args.output or args.collection
                print(f"\n🎉 İşlemler tamamlandı! Dosya kaydedildi: {output_file}")
            else:
                print("❌ Dosya kaydedilemedi!")
                return 1
        elif not (args.info or args.list_endpoints):
            print("⚠️  Hiçbir işlem yapılmadı. --help parametresi ile kullanım bilgilerini görebilirsiniz.")
    
    except Exception as e:
        print(f"❌ İşlem sırasında hata: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 