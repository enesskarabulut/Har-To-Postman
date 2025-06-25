#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Deployment App
"""

from flask import Flask, render_template_string
import subprocess
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Postman Collection Düzenleyici</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .button {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px;
            font-size: 16px;
        }
        .button:hover { background: #45a049; }
        .features {
            text-align: left;
            margin: 30px 0;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
        }
        .code {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            text-align: left;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Postman Collection Düzenleyici</h1>
        <p><strong>Web tabanlı Postman collection düzenleme aracı</strong></p>
        
        <div class="features">
            <h2>✨ Özellikler</h2>
            <ul>
                <li>📥 <strong>HAR to Postman Converter</strong> - HAR dosyalarını collection'a çevir</li>
                <li>🔧 <strong>Header Yönetimi</strong> - Toplu header ekleme/çıkarma</li>
                <li>🌐 <strong>URL Güncelleme</strong> - Base URL değiştirme</li>
                <li>📝 <strong>Metin Değiştirme</strong> - Request içeriklerinde metin değiştirme</li>
                <li>🗑️ <strong>Script Temizleme</strong> - Pre-request ve test scriptlerini kaldırma</li>
                <li>⚙️ <strong>Environment Variables</strong> - Variable ekleme</li>
                <li>🗑️ <strong>Endpoint Silme</strong> - İstenmeyen endpoint'leri kaldırma</li>
            </ul>
        </div>

        <h2>🎯 Kullanım Seçenekleri</h2>
        
        <h3>1. Local Streamlit Uygulaması (Önerilen)</h3>
        <div class="code">
# Repository'yi klonlayın
git clone https://github.com/YOUR_USERNAME/postman-collection-editor.git
cd postman-collection-editor

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Web uygulamasını çalıştırın
streamlit run postman_web_app.py
        </div>
        
        <h3>2. Command Line Kullanımı</h3>
        <div class="code">
# İnteraktif menü
python postman_collection_editor.py

# HAR converter
python har_to_postman.py example.har

# CLI komutları
python postman_cli.py collection.json --add-header "Authorization" "Bearer TOKEN"
        </div>

        <h3>3. Python Script</h3>
        <div class="code">
from postman_collection_editor import PostmanCollectionEditor

editor = PostmanCollectionEditor("collection.json")
editor.load_collection()
editor.add_header_to_all_requests("Authorization", "Bearer TOKEN")
editor.save_collection()
        </div>

        <a href="https://github.com/YOUR_USERNAME/postman-collection-editor" class="button">
            📦 GitHub Repository
        </a>
        
        <a href="https://github.com/YOUR_USERNAME/postman-collection-editor/releases" class="button">
            📥 Download Latest
        </a>

        <div style="margin-top: 40px; font-size: 14px; opacity: 0.8;">
            <p>⚠️ <strong>Not:</strong> Streamlit uygulaması Vercel'de serverless function limitasyonları nedeniyle tam performansla çalışmayabilir. En iyi deneyim için local kullanım önerilir.</p>
            <p>Büyük HAR dosyaları (>10MB) için mutlaka local uygulamayı kullanın.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return {"status": "ok", "app": "Postman Collection Editor"}

# Vercel için handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True) 