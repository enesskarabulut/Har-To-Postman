from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Postman Collection Düzenleyici</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh;
        }
        .container { 
            max-width: 900px; margin: 0 auto; padding: 40px 20px;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; text-align: center; }
        h2 { color: #ffd700; margin-top: 2rem; }
        .card { 
            background: rgba(255,255,255,0.15); padding: 2rem; 
            border-radius: 15px; margin: 1.5rem 0;
            backdrop-filter: blur(10px);
        }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
        .feature { background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; }
        .btn { 
            display: inline-block; background: #4CAF50; color: white; 
            padding: 12px 24px; text-decoration: none; border-radius: 8px; 
            margin: 10px 5px; font-weight: bold; transition: all 0.3s;
        }
        .btn:hover { background: #45a049; transform: translateY(-2px); }
        .code { 
            background: #2d3748; color: #e2e8f0; padding: 15px; 
            border-radius: 8px; margin: 10px 0; font-family: monospace;
            overflow-x: auto; white-space: pre;
        }
        .warning { 
            background: rgba(255,193,7,0.2); border-left: 4px solid #ffc107; 
            padding: 1rem; margin: 1rem 0; border-radius: 0 8px 8px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Postman Collection Düzenleyici</h1>
        <div style="text-align: center; font-size: 1.2rem; margin-bottom: 2rem;">
            HAR dosyalarını Postman collection'a çeviren ve collection'ları düzenleyen web aracı
        </div>
        
        <div class="card">
            <h2>✨ Ana Özellikler</h2>
            <div class="features">
                <div class="feature">
                    <strong>📥 HAR Converter</strong><br>
                    HAR dosyalarını Postman collection formatına çevir
                </div>
                <div class="feature">
                    <strong>🔧 Header Yönetimi</strong><br>
                    Toplu header ekleme ve çıkarma
                </div>
                <div class="feature">
                    <strong>🌐 URL Güncelleme</strong><br>
                    Base URL'leri toplu değiştirme
                </div>
                <div class="feature">
                    <strong>📝 Metin Değiştirme</strong><br>
                    Request içeriklerinde metin değiştirme
                </div>
                <div class="feature">
                    <strong>🗑️ Script Temizleme</strong><br>
                    Pre-request ve test scriptlerini kaldırma
                </div>
                <div class="feature">
                    <strong>🗑️ Endpoint Silme</strong><br>
                    İstenmeyen endpoint'leri kaldırma
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🚀 Hızlı Başlangıç</h2>
            <div class="code">git clone https://github.com/YOUR_USERNAME/postman-collection-editor.git
cd postman-collection-editor
pip install streamlit pandas
streamlit run postman_web_app.py</div>
            
            <h2>📱 Kullanım Seçenekleri</h2>
            <p><strong>Web Arayüzü:</strong> <code>streamlit run postman_web_app.py</code></p>
            <p><strong>Command Line:</strong> <code>python postman_collection_editor.py</code></p>
            <p><strong>HAR Converter:</strong> <code>python har_to_postman.py dosya.har</code></p>
        </div>

        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://github.com/YOUR_USERNAME/postman-collection-editor" class="btn">
                📦 GitHub Repository
            </a>
            <a href="https://github.com/YOUR_USERNAME/postman-collection-editor/archive/main.zip" class="btn">
                📥 Download ZIP
            </a>
        </div>

        <div class="warning">
            <strong>💡 Not:</strong> En iyi performans için local kullanım önerilir. 
            Büyük HAR dosyaları (>10MB) için mutlaka local uygulamayı kullanın.
        </div>
    </div>
</body>
</html>'''

@app.route('/health')
def health():
    return {"status": "ok"}

# Vercel compatibility
def handler(request):
    return app

if __name__ == '__main__':
    app.run() 