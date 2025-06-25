#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HAR to Postman Collection Converter
Bu script HAR (HTTP Archive) dosyalarını Postman collection formatına çevirir.
"""

import json
import os
import sys
import uuid
from urllib.parse import urlparse, parse_qs
from datetime import datetime

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
            postman_request = convert_har_request_to_postman(har_request, i + 1)
            
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

def convert_har_request_to_postman(har_request: dict, request_index: int):
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

def create_collection_from_har(har_file_path: str, output_path: str = None, collection_name: str = None):
    """HAR dosyasından Postman collection oluşturur ve kaydeder"""
    collection = har_to_postman_collection(har_file_path, collection_name)
    
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

def main():
    """Ana fonksiyon - komut satırından çalıştırma"""
    print("🚀 HAR to Postman Collection Converter")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Kullanım: python har_to_postman.py <har_dosyasi> [çıktı_dosyası] [collection_adı]")
        print("\nÖrnek:")
        print("  python har_to_postman.py example.har")
        print("  python har_to_postman.py example.har my_collection.json")
        print("  python har_to_postman.py example.har my_collection.json 'API Collection'")
        sys.exit(1)
    
    har_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    collection_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.exists(har_file):
        print(f"❌ HAR dosyası bulunamadı: {har_file}")
        sys.exit(1)
    
    print(f"📂 HAR dosyası: {har_file}")
    if output_file:
        print(f"📝 Çıktı dosyası: {output_file}")
    if collection_name:
        print(f"📋 Collection adı: {collection_name}")
    
    print("\n🔄 Çevirme işlemi başlatılıyor...")
    
    success = create_collection_from_har(har_file, output_file, collection_name)
    
    if success:
        print("\n🎉 HAR dosyası başarıyla Postman collection'ına çevrildi!")
        print("📥 Artık bu dosyayı Postman'e import edebilirsiniz.")
    else:
        print("\n❌ Çevirme işlemi başarısız oldu!")
        sys.exit(1)

if __name__ == "__main__":
    main() 