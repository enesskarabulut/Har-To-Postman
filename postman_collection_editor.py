#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection Düzenleyici
Bu script Postman collection JSON dosyalarında toplu düzenlemeler yapmanızı sağlar.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid
from urllib.parse import urlparse, parse_qs

class PostmanCollectionEditor:
    def __init__(self, collection_path: str):
        """
        Postman Collection düzenleyici sınıfı
        """
        self.collection_path = collection_path
        self.collection = None
        self.backup_created = False
        
    def load_collection(self):
        """Collection dosyasını yükler"""
        try:
            # Önce encoding'i tespit et
            encodings = ['utf-8', 'utf-8-sig', 'windows-1254', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(self.collection_path, 'r', encoding=encoding) as f:
                        self.collection = json.load(f)
                    print(f"✅ Collection başarıyla yüklendi: {self.collection_path} (encoding: {encoding})")
                    return True
                except UnicodeDecodeError:
                    continue
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parse hatası: {e}")
                    return False
            
            print(f"❌ Dosya encoding'i tespit edilemedi: {self.collection_path}")
            return False
            
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
    
    def add_header_to_all_requests(self, header_name: str, header_value: str, overwrite: bool = True):
        """Tüm requestlere header ekler"""
        count = 0
        
        def add_header(item):
            nonlocal count
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
                    count += 1
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
                count += 1
        
        self._process_items_recursive(self.collection.get('item', []), add_header)
        print(f"🎉 Toplam {count} request'e '{header_name}' header'ı işlendi!")
        return count
    
    def remove_header_from_all_requests(self, header_name: str):
        """Tüm requestlerden belirtilen header'ı kaldırır"""
        count = 0
        
        def remove_header(item):
            nonlocal count
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
                count += 1
        
        self._process_items_recursive(self.collection.get('item', []), remove_header)
        print(f"🎉 Toplam {count} request'ten '{header_name}' header'ı kaldırıldı!")
        return count
    
    def remove_all_scripts(self):
        """Tüm pre-request ve test scriptlerini kaldırır"""
        count = 0
        
        def remove_scripts(item):
            nonlocal count
            scripts_removed = []
            item_name = item.get('name', 'Unnamed')
            
            # Request seviyesindeki scriptleri kontrol et
            if 'request' in item:
                request = item['request']
                
                # Pre-request script kaldır
                if 'prerequest' in request:
                    if isinstance(request['prerequest'], dict) and request['prerequest'].get('exec'):
                        request['prerequest'] = {'exec': [], 'type': 'text/javascript'}
                        scripts_removed.append('pre-request')
                    elif isinstance(request['prerequest'], str) and request['prerequest'].strip():
                        request['prerequest'] = ''
                        scripts_removed.append('pre-request')
                
                # Request seviyesindeki event'ları kontrol et
                if 'event' in request and request['event']:
                    original_events = len(request['event'])
                    request['event'] = [e for e in request['event'] 
                                      if not (e.get('listen') in ['test', 'prerequest'] and 
                                             e.get('script', {}).get('exec'))]
                    if len(request['event']) < original_events:
                        scripts_removed.append('test')
            
            # Item seviyesindeki event'ları da kontrol et (bazı durumlarda burada olabilir)
            if 'event' in item and item['event']:
                original_events = len(item['event'])
                item['event'] = [e for e in item['event'] 
                               if not (e.get('listen') in ['test', 'prerequest'] and 
                                      e.get('script', {}).get('exec'))]
                if len(item['event']) < original_events:
                    scripts_removed.append('item-level-test')
            
            if scripts_removed:
                print(f"✅ Scriptler kaldırıldı: {item_name} - {', '.join(scripts_removed)}")
                count += 1
        
        self._process_items_recursive(self.collection.get('item', []), remove_scripts)
        print(f"🎉 Toplam {count} request'ten scriptler kaldırıldı!")
        return count
    
    def list_scripts_in_collection(self):
        """Collection'daki tüm scriptleri listeler"""
        scripts_found = []
        
        def find_scripts(item):
            item_name = item.get('name', 'Unnamed')
            item_scripts = []
            
            # Request seviyesindeki scriptleri kontrol et
            if 'request' in item:
                request = item['request']
                
                # Pre-request script
                if 'prerequest' in request:
                    if isinstance(request['prerequest'], dict) and request['prerequest'].get('exec'):
                        exec_lines = request['prerequest']['exec']
                        if exec_lines and any(line.strip() for line in exec_lines):
                            item_scripts.append(f"Pre-request ({len(exec_lines)} satır)")
                    elif isinstance(request['prerequest'], str) and request['prerequest'].strip():
                        item_scripts.append("Pre-request (string)")
                
                # Request seviyesindeki event'lar
                if 'event' in request and request['event']:
                    for event in request['event']:
                        listen_type = event.get('listen', 'unknown')
                        if event.get('script', {}).get('exec'):
                            exec_lines = event['script']['exec']
                            if exec_lines and any(line.strip() for line in exec_lines):
                                item_scripts.append(f"{listen_type.title()} ({len(exec_lines)} satır)")
            
            # Item seviyesindeki event'lar
            if 'event' in item and item['event']:
                for event in item['event']:
                    listen_type = event.get('listen', 'unknown')
                    if event.get('script', {}).get('exec'):
                        exec_lines = event['script']['exec']
                        if exec_lines and any(line.strip() for line in exec_lines):
                            item_scripts.append(f"Item-level {listen_type.title()} ({len(exec_lines)} satır)")
            
            if item_scripts:
                scripts_found.append({
                    'name': item_name,
                    'scripts': item_scripts
                })
        
        self._process_items_recursive(self.collection.get('item', []), find_scripts)
        
        print(f"\n🔍 Collection'da Script Bulunan Request'ler:")
        print("-" * 60)
        
        if scripts_found:
            for i, item in enumerate(scripts_found, 1):
                print(f"{i:3d}. {item['name']}")
                for script in item['scripts']:
                    print(f"      • {script}")
                print()
            print(f"📊 Toplam: {len(scripts_found)} request'te script bulundu")
        else:
            print("✅ Hiçbir request'te script bulunamadı!")
        
        return scripts_found
    
    def remove_endpoint_by_name(self, endpoint_name: str):
        """Belirtilen isme sahip endpoint'i kaldırır"""
        removed_count = 0
        
        def remove_from_items(items):
            nonlocal removed_count
            items_to_remove = []
            
            for i, item in enumerate(items):
                if 'request' in item and item.get('name', '').lower() == endpoint_name.lower():
                    items_to_remove.append(i)
                    print(f"✅ Endpoint kaldırıldı: {item.get('name', 'Unnamed')}")
                    removed_count += 1
                elif 'item' in item:
                    # Folder içindeki itemleri kontrol et
                    remove_from_items(item['item'])
            
            # Geriye doğru sil (index'ler değişmesin)
            for i in reversed(items_to_remove):
                items.pop(i)
        
        remove_from_items(self.collection.get('item', []))
        print(f"🎉 Toplam {removed_count} endpoint kaldırıldı!")
        return removed_count
    
    def remove_endpoints_by_method(self, method: str):
        """Belirtilen HTTP method'una sahip tüm endpoint'leri kaldırır"""
        removed_count = 0
        
        def remove_from_items(items):
            nonlocal removed_count
            items_to_remove = []
            
            for i, item in enumerate(items):
                if 'request' in item:
                    request = item['request']
                    if request.get('method', '').upper() == method.upper():
                        items_to_remove.append(i)
                        print(f"✅ {method} endpoint kaldırıldı: {item.get('name', 'Unnamed')}")
                        removed_count += 1
                elif 'item' in item:
                    # Folder içindeki itemleri kontrol et
                    remove_from_items(item['item'])
            
            # Geriye doğru sil (index'ler değişmesin)
            for i in reversed(items_to_remove):
                items.pop(i)
        
        remove_from_items(self.collection.get('item', []))
        print(f"🎉 Toplam {removed_count} adet {method} endpoint'i kaldırıldı!")
        return removed_count
    
    def remove_endpoints_by_url_pattern(self, url_pattern: str):
        """URL'inde belirtilen pattern'i içeren endpoint'leri kaldırır"""
        removed_count = 0
        
        def remove_from_items(items):
            nonlocal removed_count
            items_to_remove = []
            
            for i, item in enumerate(items):
                if 'request' in item:
                    request = item['request']
                    url = request.get('url', '')
                    if isinstance(url, dict):
                        url = url.get('raw', '')
                    
                    if url_pattern.lower() in url.lower():
                        items_to_remove.append(i)
                        print(f"✅ URL pattern eşleşti, kaldırıldı: {item.get('name', 'Unnamed')} - {url}")
                        removed_count += 1
                elif 'item' in item:
                    # Folder içindeki itemleri kontrol et
                    remove_from_items(item['item'])
            
            # Geriye doğru sil (index'ler değişmesin)
            for i in reversed(items_to_remove):
                items.pop(i)
        
        remove_from_items(self.collection.get('item', []))
        print(f"🎉 '{url_pattern}' pattern'ını içeren {removed_count} endpoint kaldırıldı!")
        return removed_count
    
    def remove_multiple_endpoints(self, endpoint_names: list):
        """Birden fazla endpoint'i isimlerine göre kaldırır"""
        total_removed = 0
        
        for name in endpoint_names:
            removed = self.remove_endpoint_by_name(name)
            total_removed += removed
        
        print(f"🎉 Toplam {total_removed} endpoint kaldırıldı!")
        return total_removed
    
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
    
    def update_base_url(self, old_url: str, new_url: str):
        """
        Tüm requestlerde base URL'i günceller
        
        Args:
            old_url (str): Eski base URL
            new_url (str): Yeni base URL
        """
        count = 0
        
        def update_url(item):
            nonlocal count
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
                    count += 1
            elif isinstance(url, dict) and 'raw' in url:
                if url['raw'].startswith(old_url):
                    url['raw'] = url['raw'].replace(old_url, new_url, 1)
                    # Host bilgisini de güncelle
                    if 'host' in url:
                        new_host = new_url.replace('https://', '').replace('http://', '').split('/')[0]
                        url['host'] = new_host.split('.')
                    print(f"✅ URL güncellendi: {item.get('name', 'Unnamed')}")
                    count += 1
        
        self._process_items_recursive(self.collection.get('item', []), update_url)
        print(f"🎉 Toplam {count} request'te URL güncellendi: {old_url} -> {new_url}")
        return count
    
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
    
    def replace_text_in_requests(self, old_text: str, new_text: str):
        """Tüm requestlerde belirtilen metni değiştirir (URL, body, header değerlerinde)"""
        count = 0
        
        def replace_text(item):
            nonlocal count
            if 'request' not in item:
                return
                
            request = item['request']
            changed = False
            
            # URL'de değiştir
            if 'url' in request:
                url = request['url']
                if isinstance(url, str) and old_text in url:
                    request['url'] = url.replace(old_text, new_text)
                    changed = True
                elif isinstance(url, dict) and 'raw' in url and old_text in url['raw']:
                    url['raw'] = url['raw'].replace(old_text, new_text)
                    changed = True
            
            # Header değerlerinde değiştir
            if 'header' in request:
                for header in request['header']:
                    if isinstance(header, dict):
                        if 'value' in header and old_text in str(header['value']):
                            header['value'] = str(header['value']).replace(old_text, new_text)
                            changed = True
            
            # Body'de değiştir
            if 'body' in request and request['body']:
                body = request['body']
                if isinstance(body, dict):
                    if 'raw' in body and old_text in str(body['raw']):
                        body['raw'] = str(body['raw']).replace(old_text, new_text)
                        changed = True
            
            if changed:
                print(f"✅ Metin değiştirildi: {item.get('name', 'Unnamed')}")
                count += 1
        
        self._process_items_recursive(self.collection.get('item', []), replace_text)
        print(f"🎉 Toplam {count} request'te '{old_text}' -> '{new_text}' değiştirildi!")
        return count

    @staticmethod
    def har_to_postman_collection(har_file_path: str, collection_name: str = None):
        """HAR dosyasını Postman collection'ına çevirir"""
        try:
            # HAR dosyasını yükle
            with open(har_file_path, 'r', encoding='utf-8') as f:
                har_data = json.load(f)
            
            if 'log' not in har_data or 'entries' not in har_data['log']:
                raise ValueError("Geçersiz HAR dosyası formatı")
            
            entries = har_data['log']['entries']
            
            # Collection adını belirle
            if not collection_name:
                collection_name = f"HAR Import - {os.path.basename(har_file_path)}"
            
            # Postman collection template
            collection = {
                "info": {
                    "name": collection_name,
                    "description": f"HAR dosyasından çevrildi: {har_file_path}",
                    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                    "_postman_id": str(uuid.uuid4())
                },
                "item": []
            }
            
            # Domain'lere göre grupla
            domain_items = {}
            
            print(f"🔄 {len(entries)} HTTP isteği işleniyor...")
            
            for i, entry in enumerate(entries):
                if 'request' not in entry:
                    continue
                
                har_request = entry['request']
                
                # URL'yi parse et
                url = har_request.get('url', '')
                if not url:
                    continue
                
                parsed_url = urlparse(url)
                domain = parsed_url.netloc or 'unknown'
                
                # Postman request formatına çevir
                postman_request = PostmanCollectionEditor._convert_har_request_to_postman(har_request, i + 1)
                
                # Domain grubuna ekle
                if domain not in domain_items:
                    domain_items[domain] = {
                        "name": domain,
                        "item": []
                    }
                
                domain_items[domain]["item"].append(postman_request)
            
            # Domain'leri collection'a ekle
            for domain_item in domain_items.values():
                collection["item"].append(domain_item)
            
            total_requests = sum(len(domain["item"]) for domain in domain_items.values())
            print(f"✅ {total_requests} istek {len(domain_items)} domain'de gruplandı")
            
            return collection
            
        except Exception as e:
            print(f"❌ HAR çevirilirken hata: {e}")
            return None
    
    @staticmethod
    def _convert_har_request_to_postman(har_request: Dict, request_index: int):
        """Tek bir HAR request'ini Postman formatına çevirir"""
        url = har_request.get('url', '')
        method = har_request.get('method', 'GET').upper()
        
        # URL'yi parse et
        parsed_url = urlparse(url)
        
        # Query parameters
        query_params = []
        if parsed_url.query:
            for key, values in parse_qs(parsed_url.query, keep_blank_values=True).items():
                for value in values:
                    query_params.append({
                        "key": key,
                        "value": value
                    })
        
        # HAR'dan gelen query params da ekle (fazladan kontrol)
        if 'queryString' in har_request:
            for param in har_request['queryString']:
                query_params.append({
                    "key": param.get('name', ''),
                    "value": param.get('value', '')
                })
        
        # Headers
        headers = []
        if 'headers' in har_request:
            for header in har_request['headers']:
                header_name = header.get('name', '')
                header_value = header.get('value', '')
                
                # Bazı headerları skip et (browser otomatik ekliyor)
                skip_headers = ['host', 'content-length', 'connection', 'accept-encoding']
                if header_name.lower() not in skip_headers:
                    headers.append({
                        "key": header_name,
                        "value": header_value,
                        "type": "text"
                    })
        
        # Request body
        body = {}
        if 'postData' in har_request and har_request['postData']:
            post_data = har_request['postData']
            mime_type = post_data.get('mimeType', '')
            
            if 'text' in post_data:
                if 'application/json' in mime_type:
                    body = {
                        "mode": "raw",
                        "raw": post_data['text'],
                        "options": {
                            "raw": {
                                "language": "json"
                            }
                        }
                    }
                elif 'application/x-www-form-urlencoded' in mime_type:
                    # Form data'yı parse et
                    form_data = []
                    if 'params' in post_data:
                        for param in post_data['params']:
                            form_data.append({
                                "key": param.get('name', ''),
                                "value": param.get('value', ''),
                                "type": "text"
                            })
                    body = {
                        "mode": "urlencoded",
                        "urlencoded": form_data
                    }
                else:
                    body = {
                        "mode": "raw",
                        "raw": post_data['text']
                    }
        
        # URL objesi oluştur
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        
        url_obj = {
            "raw": url,
            "protocol": parsed_url.scheme,
            "host": parsed_url.netloc.split('.') if parsed_url.netloc else [],
            "path": [p for p in parsed_url.path.split('/') if p]
        }
        
        if query_params:
            url_obj["query"] = query_params
        
        # Request name
        request_name = f"{method} {parsed_url.path.split('/')[-1] or parsed_url.netloc}"
        if len(request_name) > 50:
            request_name = request_name[:47] + "..."
        
        # Postman request object
        postman_request = {
            "name": f"{request_index:03d}. {request_name}",
            "request": {
                "method": method,
                "header": headers,
                "url": url_obj
            }
        }
        
        # Body varsa ekle
        if body:
            postman_request["request"]["body"] = body
        
        return postman_request

    @staticmethod
    def create_collection_from_har(har_file_path: str, output_path: str = None, collection_name: str = None):
        """HAR dosyasından Postman collection oluşturur ve kaydeder"""
        collection = PostmanCollectionEditor.har_to_postman_collection(har_file_path, collection_name)
        
        if not collection:
            return False
        
        # Output dosya adını belirle
        if not output_path:
            base_name = os.path.splitext(os.path.basename(har_file_path))[0]
            output_path = f"{base_name}_postman_collection.json"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(collection, f, indent=2, ensure_ascii=False)
            print(f"✅ Postman collection oluşturuldu: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Collection kaydedilirken hata: {e}")
            return False

def interactive_menu():
    """Interaktif menü"""
    print("\n🚀 Postman Collection Düzenleyici")
    print("=" * 50)
    
    # Collection dosyası seç
    collection_file = input("Collection JSON dosyasının adını girin (varsayılan: 'collection (2).json'): ").strip()
    if not collection_file:
        collection_file = "collection (2).json"
    
    if not os.path.exists(collection_file):
        print(f"❌ Dosya bulunamadı: {collection_file}")
        return
    
    # Editor oluştur ve yükle
    editor = PostmanCollectionEditor(collection_file)
    if not editor.load_collection():
        return
    
    # Ana menü
    while True:
        print("\n" + "="*50)
        print("İşlem seçiniz:")
        print("1. Collection bilgilerini göster")
        print("2. Tüm endpoint'leri listele")
        print("3. Scriptleri listele")
        print("4. Tüm requestlere header ekle")
        print("5. Tüm requestlerden header kaldır")
        print("6. Tüm scriptleri kaldır")
        print("7. Base URL güncelle")
        print("8. Environment variable ekle")
        print("9. Metin değiştir (URL/Body/Header)")
        print("10. Endpoint silme işlemleri")
        print("11. HAR dosyasından collection oluştur")
        print("12. Yedek oluştur")
        print("13. Collection'ı kaydet")
        print("0. Çıkış")
        
        choice = input("\nSeçiminiz (0-13): ").strip()
        
        if choice == "0":
            print("👋 Görüşürüz!")
            break
        elif choice == "1":
            editor.get_collection_info()
        elif choice == "2":
            editor.list_all_endpoints()
        elif choice == "3":
            editor.list_scripts_in_collection()
        elif choice == "4":
            header_name = input("Header adı: ").strip()
            header_value = input("Header değeri: ").strip()
            if header_name and header_value:
                editor.add_header_to_all_requests(header_name, header_value)
            else:
                print("❌ Header adı ve değeri boş olamaz!")
        elif choice == "5":
            header_name = input("Kaldırılacak header adı: ").strip()
            if header_name:
                editor.remove_header_from_all_requests(header_name)
            else:
                print("❌ Header adı boş olamaz!")
        elif choice == "6":
            confirm = input("Tüm scriptleri kaldırmak istediğinizden emin misiniz? (e/h): ").strip().lower()
            if confirm == 'e':
                editor.remove_all_scripts()
        elif choice == "7":
            old_url = input("Eski base URL: ").strip()
            new_url = input("Yeni base URL: ").strip()
            if old_url and new_url:
                editor.update_base_url(old_url, new_url)
            else:
                print("❌ URL'ler boş olamaz!")
        elif choice == "8":
            var_name = input("Variable adı: ").strip()
            var_value = input("Variable değeri: ").strip()
            if var_name and var_value:
                editor.add_environment_variable(var_name, var_value)
            else:
                print("❌ Variable adı ve değeri boş olamaz!")
        elif choice == "9":
            old_text = input("Değiştirilecek metin: ").strip()
            new_text = input("Yeni metin: ").strip()
            if old_text and new_text:
                editor.replace_text_in_requests(old_text, new_text)
            else:
                print("❌ Metinler boş olamaz!")
        elif choice == "10":
            # Endpoint silme alt menüsü
            while True:
                print("\n" + "-"*30)
                print("Endpoint Silme İşlemleri:")
                print("1. İsme göre endpoint sil")
                print("2. HTTP method'una göre endpoint sil")
                print("3. URL pattern'ına göre endpoint sil")
                print("4. Birden fazla endpoint sil")
                print("5. Endpoint listesini görüntüle")
                print("0. Ana menüye dön")
                
                sub_choice = input("\nSeçiminiz (0-5): ").strip()
                
                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    endpoint_name = input("Silinecek endpoint ismi: ").strip()
                    if endpoint_name:
                        confirm = input(f"'{endpoint_name}' endpoint'ini silmek istediğinizden emin misiniz? (e/h): ").strip().lower()
                        if confirm == 'e':
                            editor.remove_endpoint_by_name(endpoint_name)
                    else:
                        print("❌ Endpoint ismi boş olamaz!")
                elif sub_choice == "2":
                    method = input("Silinecek HTTP method (GET, POST, PUT, DELETE, vb.): ").strip()
                    if method:
                        confirm = input(f"Tüm {method.upper()} endpoint'lerini silmek istediğinizden emin misiniz? (e/h): ").strip().lower()
                        if confirm == 'e':
                            editor.remove_endpoints_by_method(method)
                    else:
                        print("❌ HTTP method boş olamaz!")
                elif sub_choice == "3":
                    url_pattern = input("URL'de aranacak pattern: ").strip()
                    if url_pattern:
                        confirm = input(f"URL'inde '{url_pattern}' içeren tüm endpoint'leri silmek istediğinizden emin misiniz? (e/h): ").strip().lower()
                        if confirm == 'e':
                            editor.remove_endpoints_by_url_pattern(url_pattern)
                    else:
                        print("❌ URL pattern boş olamaz!")
                elif sub_choice == "4":
                    print("Silinecek endpoint isimlerini virgülle ayırarak girin:")
                    endpoints_str = input("Örnek: Endpoint1, Endpoint2, Endpoint3: ").strip()
                    if endpoints_str:
                        endpoint_names = [name.strip() for name in endpoints_str.split(',')]
                        if endpoint_names:
                            print(f"\nSilinecek endpoint'ler: {endpoint_names}")
                            confirm = input("Bu endpoint'leri silmek istediğinizden emin misiniz? (e/h): ").strip().lower()
                            if confirm == 'e':
                                editor.remove_multiple_endpoints(endpoint_names)
                    else:
                        print("❌ Endpoint isimleri boş olamaz!")
                elif sub_choice == "5":
                    editor.list_all_endpoints()
                else:
                    print("❌ Geçersiz seçim!")
        elif choice == "11":
            # HAR converter
            har_file = input("HAR dosyasının yolu: ").strip()
            if not har_file:
                print("❌ HAR dosya yolu boş olamaz!")
                continue
            
            if not os.path.exists(har_file):
                print(f"❌ HAR dosyası bulunamadı: {har_file}")
                continue
            
            collection_name = input("Collection adı (boş bırakırsanız otomatik verilir): ").strip()
            output_file = input("Çıktı dosyası adı (boş bırakırsanız otomatik verilir): ").strip()
            
            print("🔄 HAR dosyası çevriliyor...")
            success = PostmanCollectionEditor.create_collection_from_har(
                har_file, 
                output_file if output_file else None,
                collection_name if collection_name else None
            )
            
            if success:
                print("✅ HAR dosyası başarıyla Postman collection'ına çevrildi!")
            else:
                print("❌ HAR dosyası çevrilirken hata oluştu!")
        elif choice == "12":
            editor.create_backup()
        elif choice == "13":
            output_file = input("Çıktı dosyası adı (boş bırakırsanız orijinal dosya güncellenir): ").strip()
            editor.save_collection(output_file if output_file else None)
        else:
            print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    interactive_menu() 