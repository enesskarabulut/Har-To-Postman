#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection Düzenleyici
Bu script Postman collection JSON dosyalarında toplu düzenlemeler yapmanızı sağlar.
"""

import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

class PostmanCollectionEditor:
    def __init__(self, collection_path: str):
        """
        Postman Collection düzenleyici sınıfı
        
        Args:
            collection_path (str): Collection JSON dosyasının yolu
        """
        self.collection_path = collection_path
        self.collection = None
        self.backup_created = False
        
    def load_collection(self):
        """Collection dosyasını yükler"""
        try:
            with open(self.collection_path, 'r', encoding='utf-8') as f:
                self.collection = json.load(f)
            print(f"✅ Collection başarıyla yüklendi: {self.collection_path}")
            return True
        except Exception as e:
            print(f"❌ Collection yüklenirken hata: {e}")
            return False
    
    def save_collection(self, output_path: Optional[str] = None):
        """Collection'ı dosyaya kaydeder"""
        save_path = output_path or self.collection_path
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.collection, f, indent=2, ensure_ascii=False)
            print(f"✅ Collection kaydedildi: {save_path}")
            return True
        except Exception as e:
            print(f"❌ Collection kaydedilirken hata: {e}")
            return False
    
    def create_backup(self):
        """Orijinal dosyanın yedeğini oluşturur"""
        if self.backup_created:
            return True
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.collection_path}.backup_{timestamp}"
        
        try:
            with open(self.collection_path, 'r', encoding='utf-8') as source:
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
            print(f"✅ Yedek oluşturuldu: {backup_path}")
            self.backup_created = True
            return True
        except Exception as e:
            print(f"❌ Yedek oluşturulurken hata: {e}")
            return False
    
    def _process_items_recursive(self, items: List[Dict], processor_func):
        """Collection itemlerini recursive olarak işler"""
        for item in items:
            if 'request' in item:
                # Bu bir request item'ı
                processor_func(item)
            elif 'item' in item:
                # Bu bir folder, alt itemleri işle
                self._process_items_recursive(item['item'], processor_func)
    
    def add_header_to_all_requests(self, header_name: str, header_value: str, overwrite: bool = False):
        """
        Tüm requestlere header ekler
        
        Args:
            header_name (str): Header adı
            header_value (str): Header değeri
            overwrite (bool): Mevcut header varsa üzerine yazılsın mı
        """
        def add_header(item):
            if 'request' not in item:
                return
                
            request = item['request']
            if 'header' not in request:
                request['header'] = []
            
            # Mevcut header'ı kontrol et
            existing_header = None
            for header in request['header']:
                if isinstance(header, dict) and header.get('key', '').lower() == header_name.lower():
                    existing_header = header
                    break
            
            if existing_header:
                if overwrite:
                    existing_header['value'] = header_value
                    print(f"🔄 Header güncellendi: {item.get('name', 'Unnamed')} - {header_name}")
                else:
                    print(f"⚠️  Header zaten mevcut: {item.get('name', 'Unnamed')} - {header_name}")
            else:
                new_header = {
                    "key": header_name,
                    "value": header_value,
                    "type": "text"
                }
                request['header'].append(new_header)
                print(f"✅ Header eklendi: {item.get('name', 'Unnamed')} - {header_name}")
        
        self._process_items_recursive(self.collection.get('item', []), add_header)
        print(f"🎉 Tüm requestlere '{header_name}' header'ı işlendi!")
    
    def remove_header_from_all_requests(self, header_name: str):
        """
        Tüm requestlerden belirtilen header'ı kaldırır
        
        Args:
            header_name (str): Kaldırılacak header adı
        """
        def remove_header(item):
            if 'request' not in item:
                return
                
            request = item['request']
            if 'header' not in request:
                return
            
            original_count = len(request['header'])
            request['header'] = [
                header for header in request['header']
                if not (isinstance(header, dict) and header.get('key', '').lower() == header_name.lower())
            ]
            
            if len(request['header']) < original_count:
                print(f"✅ Header kaldırıldı: {item.get('name', 'Unnamed')} - {header_name}")
        
        self._process_items_recursive(self.collection.get('item', []), remove_header)
        print(f"🎉 Tüm requestlerden '{header_name}' header'ı kaldırıldı!")
    
    def remove_all_scripts(self):
        """Tüm pre-request ve test scriptlerini kaldırır"""
        def remove_scripts(item):
            if 'request' not in item:
                return
                
            request = item['request']
            scripts_removed = []
            
            # Pre-request script kaldır
            if 'prerequest' in request and request['prerequest']:
                request['prerequest'] = {'exec': [], 'type': 'text/javascript'}
                scripts_removed.append('pre-request')
            
            # Test script kaldır (event içinde)
            if 'event' in request:
                test_events = [e for e in request['event'] if e.get('listen') == 'test']
                if test_events:
                    request['event'] = [e for e in request['event'] if e.get('listen') != 'test']
                    scripts_removed.append('test')
            
            if scripts_removed:
                print(f"✅ Scriptler kaldırıldı: {item.get('name', 'Unnamed')} - {', '.join(scripts_removed)}")
        
        self._process_items_recursive(self.collection.get('item', []), remove_scripts)
        print("🎉 Tüm scriptler kaldırıldı!")
    
    def update_base_url(self, old_url: str, new_url: str):
        """
        Tüm requestlerde base URL'i günceller
        
        Args:
            old_url (str): Eski base URL
            new_url (str): Yeni base URL
        """
        def update_url(item):
            if 'request' not in item:
                return
                
            request = item['request']
            if 'url' not in request:
                return
            
            url = request['url']
            if isinstance(url, str):
                if url.startswith(old_url):
                    request['url'] = url.replace(old_url, new_url, 1)
                    print(f"✅ URL güncellendi: {item.get('name', 'Unnamed')}")
            elif isinstance(url, dict) and 'raw' in url:
                if url['raw'].startswith(old_url):
                    url['raw'] = url['raw'].replace(old_url, new_url, 1)
                    # Host ve path bilgilerini de güncelle
                    if 'host' in url:
                        url['host'] = new_url.replace('https://', '').replace('http://', '').split('/')[0].split('.')
                    print(f"✅ URL güncellendi: {item.get('name', 'Unnamed')}")
        
        self._process_items_recursive(self.collection.get('item', []), update_url)
        print(f"🎉 Base URL güncellendi: {old_url} -> {new_url}")
    
    def list_all_endpoints(self):
        """Tüm endpoint'leri listeler"""
        endpoints = []
        
        def collect_endpoint(item):
            if 'request' not in item:
                return
                
            request = item['request']
            method = request.get('method', 'UNKNOWN')
            
            url = request.get('url', '')
            if isinstance(url, dict):
                url = url.get('raw', '')
            
            endpoints.append({
                'name': item.get('name', 'Unnamed'),
                'method': method,
                'url': url
            })
        
        self._process_items_recursive(self.collection.get('item', []), collect_endpoint)
        
        print("\n📋 Collection'daki tüm endpoint'ler:")
        print("-" * 80)
        for i, endpoint in enumerate(endpoints, 1):
            print(f"{i:3d}. [{endpoint['method']:6s}] {endpoint['name']}")
            print(f"      URL: {endpoint['url']}")
            print()
        
        return endpoints
    
    def add_environment_variable(self, var_name: str, var_value: str):
        """Collection seviyesinde environment variable ekler"""
        if 'variable' not in self.collection:
            self.collection['variable'] = []
        
        # Mevcut variable'ı kontrol et
        existing_var = None
        for var in self.collection['variable']:
            if var.get('key') == var_name:
                existing_var = var
                break
        
        if existing_var:
            existing_var['value'] = var_value
            print(f"🔄 Variable güncellendi: {var_name} = {var_value}")
        else:
            new_var = {
                "key": var_name,
                "value": var_value
            }
            self.collection['variable'].append(new_var)
            print(f"✅ Variable eklendi: {var_name} = {var_value}")
    
    def get_collection_info(self):
        """Collection hakkında genel bilgi verir"""
        if not self.collection:
            print("❌ Collection yüklenmemiş!")
            return
        
        info = self.collection.get('info', {})
        name = info.get('name', 'Bilinmeyen')
        description = info.get('description', 'Açıklama yok')
        
        # Request sayısını hesapla
        request_count = 0
        def count_requests(items):
            nonlocal request_count
            for item in items:
                if 'request' in item:
                    request_count += 1
                elif 'item' in item:
                    count_requests(item['item'])
        
        count_requests(self.collection.get('item', []))
        
        print(f"\n📊 Collection Bilgileri:")
        print(f"   Adı: {name}")
        print(f"   Açıklama: {description}")
        print(f"   Toplam Request Sayısı: {request_count}")
        print(f"   Dosya Boyutu: {os.path.getsize(self.collection_path) / 1024 / 1024:.2f} MB")

def main():
    print("🚀 Postman Collection Düzenleyici")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description='Postman Collection düzenleyici')
    parser.add_argument('collection', help='Collection JSON dosyası yolu')
    parser.add_argument('--backup', action='store_true', help='İşlem öncesi yedek oluştur')
    parser.add_argument('--output', help='Çıktı dosyası yolu (belirtilmezse orijinal dosya güncellenir)')
    
    # İşlem türleri
    parser.add_argument('--add-header', nargs=2, metavar=('NAME', 'VALUE'), help='Tüm requestlere header ekle')
    parser.add_argument('--remove-header', metavar='NAME', help='Tüm requestlerden header kaldır')
    parser.add_argument('--remove-scripts', action='store_true', help='Tüm scriptleri kaldır')
    parser.add_argument('--update-url', nargs=2, metavar=('OLD', 'NEW'), help='Base URL güncelle')
    parser.add_argument('--list-endpoints', action='store_true', help='Tüm endpoint\'leri listele')
    parser.add_argument('--info', action='store_true', help='Collection bilgilerini göster')
    parser.add_argument('--add-variable', nargs=2, metavar=('NAME', 'VALUE'), help='Environment variable ekle')
    
    args = parser.parse_args()
    
    # Collection editor oluştur
    editor = PostmanCollectionEditor(args.collection)
    
    # Collection'ı yükle
    if not editor.load_collection():
        return 1
    
    # Yedek oluştur
    if args.backup:
        editor.create_backup()
    
    # Bilgi göster
    if args.info:
        editor.get_collection_info()
    
    # Endpoint'leri listele
    if args.list_endpoints:
        editor.list_all_endpoints()
    
    # İşlemleri gerçekleştir
    changes_made = False
    
    if args.add_header:
        editor.add_header_to_all_requests(args.add_header[0], args.add_header[1], overwrite=True)
        changes_made = True
    
    if args.remove_header:
        editor.remove_header_from_all_requests(args.remove_header)
        changes_made = True
    
    if args.remove_scripts:
        editor.remove_all_scripts()
        changes_made = True
    
    if args.update_url:
        editor.update_base_url(args.update_url[0], args.update_url[1])
        changes_made = True
    
    if args.add_variable:
        editor.add_environment_variable(args.add_variable[0], args.add_variable[1])
        changes_made = True
    
    # Değişiklikler varsa kaydet
    if changes_made:
        editor.save_collection(args.output)
        print("\n🎉 Tüm işlemler tamamlandı!")
    
    return 0

if __name__ == "__main__":
    exit(main()) 