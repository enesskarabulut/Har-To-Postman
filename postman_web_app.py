#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection Web App
Streamlit ile web tabanlı arayüz
"""

import streamlit as st
import os
import json
import tempfile
from postman_collection_editor import PostmanCollectionEditor

# Session state'i initialize et
if 'editor' not in st.session_state:
    st.session_state.editor = None
if 'collection_loaded' not in st.session_state:
    st.session_state.collection_loaded = False
if 'endpoints' not in st.session_state:
    st.session_state.endpoints = []

def init_session_state():
    """Session state'i başlat (artık gerekmiyor ama uyumluluk için bırakıldı)"""
    pass

def main():
    st.set_page_config(
        page_title="Postman Collection Düzenleyici",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Postman Collection Düzenleyici")
    st.markdown("Web tabanlı Postman collection düzenleme aracı")
    
    # Sidebar - HAR Converter ve Collection Yükleme
    with st.sidebar:
        # HAR to Postman Converter
        st.header("📥 HAR to Postman")
        st.markdown("HAR dosyalarını collection'a çevirin")
        
        har_converter_sidebar()
        
        st.divider()
        
        # Collection Dosyası Yükleme
        st.header("📁 Collection Dosyası")
        
        uploaded_file = st.file_uploader(
            "Postman Collection JSON dosyası seçin",
            type=['json'],
            help="Postman'den export ettiğiniz collection JSON dosyasını yükleyin"
        )
        
        if uploaded_file is not None:
            if st.button("Collection'ı Yükle", type="primary"):
                load_collection(uploaded_file)
        
        st.divider()
        
        # Collection bilgileri
        if st.session_state.get('collection_loaded', False):
            st.header("📊 Collection Bilgileri")
            show_collection_info()
    
    # Ana içerik alanı
    if not st.session_state.get('collection_loaded', False):
        st.info("👆 Lütfen önce bir collection dosyası yükleyin")
        st.markdown("""
        ### Nasıl Kullanılır?
        1. **Dosya Yükle**: Sol taraftaki dosya yükleyici ile Postman collection JSON dosyanızı seçin
        2. **Collection Yükle**: Dosyayı seçtikten sonra "Collection'ı Yükle" butonuna tıklayın
        3. **İşlem Yapın**: Yüklendikten sonra aşağıdaki sekmelerden istediğiniz işlemi yapın
        4. **İndir**: İşlemlerinizi tamamladıktan sonra güncellenmiş dosyayı indirin
        """)
        return
    
    # Tab'lar (HAR Converter sidebar'a taşındı)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🔧 Header İşlemleri", 
        "🌐 URL İşlemleri", 
        "📝 Metin Değiştirme", 
        "🗑️ Script Temizleme",
        "⚙️ Environment Variables",
        "📋 Endpoint'ler",
        "🔍 Script Listesi",
        "🗑️ Endpoint Silme"
    ])
    
    with tab1:
        header_operations()
    
    with tab2:
        url_operations()
        
    with tab3:
        text_operations()
        
    with tab4:
        script_operations()
        
    with tab5:
        environment_operations()
        
    with tab6:
        endpoint_list()
        
    with tab7:
        script_list()
        
    with tab8:
        endpoint_removal()

def load_collection(uploaded_file):
    """Collection dosyasını yükle"""
    try:
        # Dosyayı okuyup encoding'i tespit et
        raw_bytes = uploaded_file.read()
        
        # Farklı encoding'leri dene
        encodings = ['utf-8', 'utf-8-sig', 'windows-1254', 'latin-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                content = raw_bytes.decode(encoding)
                st.info(f"📝 Dosya encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            st.error("❌ Dosya encoding'i tespit edilemedi!")
            return
        
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Editor oluştur ve yükle
        editor = PostmanCollectionEditor(tmp_file_path)
        if editor.load_collection():
            st.session_state.editor = editor
            st.session_state.collection_loaded = True
            st.session_state.uploaded_filename = uploaded_file.name
            
            # Endpoint'leri yükle
            st.session_state.endpoints = editor.list_all_endpoints()
            
            st.success(f"✅ Collection başarıyla yüklendi: {uploaded_file.name}")
            st.rerun()
        else:
            st.error("❌ Collection yüklenemedi!")
            
    except Exception as e:
        st.error(f"❌ Hata: {e}")

def show_collection_info():
    """Collection bilgilerini göster"""
    if not st.session_state.get('editor'):
        return
    
    try:
        collection = st.session_state.editor.collection
        info = collection.get('info', {})
        
        st.markdown(f"**📝 Adı:** {info.get('name', 'Bilinmeyen')}")
        st.markdown(f"**🔢 Request Sayısı:** {len(st.session_state.get('endpoints', []))}")
        
        # Yedek oluştur butonu
        if st.button("💾 Yedek Oluştur", help="Değişiklik yapmadan önce yedek oluşturun"):
            if st.session_state.editor.create_backup():
                st.success("✅ Yedek oluşturuldu!")
            else:
                st.error("❌ Yedek oluşturulamadı!")
                
    except Exception as e:
        st.error(f"Bilgi alınırken hata: {e}")

def header_operations():
    """Header işlemleri sekmesi"""
    st.header("🔧 Header İşlemleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("➕ Header Ekle")
        header_name = st.text_input(
            "Header Adı", 
            value="Authorization",
            key="add_header_name"
        )
        header_value = st.text_input(
            "Header Değeri", 
            value="Bearer TOKEN_HERE",
            key="add_header_value"
        )
        
        if st.button("Header Ekle", type="primary"):
            if header_name and header_value:
                try:
                    count = st.session_state.editor.add_header_to_all_requests(header_name, header_value)
                    st.success(f"✅ {count} request'e '{header_name}' header'ı eklendi!")
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
            else:
                st.warning("⚠️ Header adı ve değeri boş olamaz!")
    
    with col2:
        st.subheader("➖ Header Kaldır")
        remove_header_name = st.text_input(
            "Kaldırılacak Header Adı",
            key="remove_header_name"
        )
        
        if st.button("Header Kaldır", type="secondary"):
            if remove_header_name:
                try:
                    count = st.session_state.editor.remove_header_from_all_requests(remove_header_name)
                    st.success(f"✅ {count} request'ten '{remove_header_name}' header'ı kaldırıldı!")
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
            else:
                st.warning("⚠️ Header adı boş olamaz!")

def url_operations():
    """URL işlemleri sekmesi"""
    st.header("🌐 URL İşlemleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        old_url = st.text_input(
            "Eski Base URL",
            value="http://localhost:3000",
            help="Değiştirilecek URL"
        )
    
    with col2:
        new_url = st.text_input(
            "Yeni Base URL",
            value="https://api.example.com",
            help="Yeni URL"
        )
    
    if st.button("🔄 URL'leri Güncelle", type="primary"):
        if old_url and new_url:
            try:
                count = st.session_state.editor.update_base_url(old_url, new_url)
                st.success(f"✅ {count} request'te URL güncellendi!")
                # Endpoint'leri yenile
                st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
            except Exception as e:
                st.error(f"❌ Hata: {e}")
        else:
            st.warning("⚠️ URL'ler boş olamaz!")

def text_operations():
    """Metin değiştirme sekmesi"""
    st.header("📝 Metin Değiştirme")
    st.markdown("URL, header değerleri ve body içeriğindeki metinleri değiştirin")
    
    col1, col2 = st.columns(2)
    
    with col1:
        old_text = st.text_input(
            "Değiştirilecek Metin",
            help="Aranacak metin"
        )
    
    with col2:
        new_text = st.text_input(
            "Yeni Metin",
            help="Yerine konulacak metin"
        )
    
    if st.button("🔄 Metin Değiştir", type="primary"):
        if old_text and new_text:
            try:
                count = st.session_state.editor.replace_text_in_requests(old_text, new_text)
                st.success(f"✅ {count} request'te '{old_text}' -> '{new_text}' değiştirildi!")
                # Endpoint'leri yenile
                st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
            except Exception as e:
                st.error(f"❌ Hata: {e}")
        else:
            st.warning("⚠️ Metinler boş olamaz!")

def script_operations():
    """Script temizleme sekmesi"""
    st.header("🗑️ Script Temizleme")
    st.markdown("Pre-request ve test scriptlerini collection'dan kaldırın")
    
    st.warning("⚠️ Bu işlem geri alınamaz! Devam etmeden önce yedek oluşturun.")
    
    confirm = st.checkbox("Tüm scriptleri kaldırmak istediğimi onaylıyorum")
    
    if st.button("🗑️ Tüm Scriptleri Kaldır", type="primary", disabled=not confirm):
        try:
            count = st.session_state.editor.remove_all_scripts()
            st.success(f"✅ {count} request'ten scriptler kaldırıldı!")
        except Exception as e:
            st.error(f"❌ Hata: {e}")

def environment_operations():
    """Environment variable işlemleri"""
    st.header("⚙️ Environment Variables")
    st.markdown("Collection seviyesinde environment variable'lar ekleyin")
    
    col1, col2 = st.columns(2)
    
    with col1:
        var_name = st.text_input(
            "Variable Adı",
            help="Örn: API_BASE_URL"
        )
    
    with col2:
        var_value = st.text_input(
            "Variable Değeri",
            help="Örn: https://api.example.com"
        )
    
    if st.button("➕ Variable Ekle", type="primary"):
        if var_name and var_value:
            try:
                st.session_state.editor.add_environment_variable(var_name, var_value)
                st.success(f"✅ '{var_name}' variable'ı eklendi!")
            except Exception as e:
                st.error(f"❌ Hata: {e}")
        else:
            st.warning("⚠️ Variable adı ve değeri boş olamaz!")

def endpoint_list():
    """Endpoint listesi sekmesi"""
    st.header("📋 Endpoint'ler")
    
    if st.button("🔄 Listeyi Yenile"):
        if st.session_state.get('editor'):
            st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
            st.rerun()
    
    if st.session_state.get('endpoints', []):
        # DataFrame oluştur
        import pandas as pd
        df = pd.DataFrame(st.session_state.endpoints)
        
        # Filtreleme
        col1, col2 = st.columns(2)
        with col1:
            method_filter = st.selectbox(
                "Method Filtresi",
                options=["Tümü"] + sorted(df['method'].unique().tolist())
            )
        
        with col2:
            search_term = st.text_input("Endpoint Ara", placeholder="Endpoint adı veya URL'de ara")
        
        # Filtreleme uygula
        filtered_df = df.copy()
        
        if method_filter != "Tümü":
            filtered_df = filtered_df[filtered_df['method'] == method_filter]
        
        if search_term:
            mask = filtered_df['name'].str.contains(search_term, case=False, na=False) | \
                   filtered_df['url'].str.contains(search_term, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        st.markdown(f"**Toplam: {len(filtered_df)} endpoint**")
        
        # Tablo göster
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Endpoint bulunamadı")

def endpoint_removal():
    """Endpoint silme sekmesi"""
    st.header("🗑️ Endpoint Silme İşlemleri")
    st.markdown("Belirli endpoint'leri collection'dan kaldırın")
    
    st.warning("⚠️ Bu işlem geri alınamaz! Devam etmeden önce yedek oluşturun.")
    
    # Silme yöntemi seçimi
    method = st.selectbox(
        "Silme Yöntemi",
        ["İsme Göre Sil", "HTTP Method'una Göre Sil", "URL Pattern'ına Göre Sil", "Birden Fazla Endpoint Sil"]
    )
    
    if method == "İsme Göre Sil":
        st.subheader("📝 İsme Göre Endpoint Silme")
        
        # Mevcut endpoint'leri dropdown'da göster
        if st.session_state.get('endpoints', []):
            endpoint_names = [ep['name'] for ep in st.session_state.endpoints]
            selected_endpoint = st.selectbox(
                "Silinecek Endpoint'i Seçin",
                options=["Seçin..."] + endpoint_names
            )
            
            # Manual giriş de ekleyelim
            manual_name = st.text_input(
                "Veya Endpoint İsmini Manuel Girin",
                help="Yukarıdaki listede yoksa manuel girebilirsiniz"
            )
            
            endpoint_to_remove = manual_name if manual_name else (selected_endpoint if selected_endpoint != "Seçin..." else "")
            
            if endpoint_to_remove:
                st.info(f"Silinecek: {endpoint_to_remove}")
                
                confirm = st.checkbox(f"'{endpoint_to_remove}' endpoint'ini silmek istediğimi onaylıyorum")
                
                if st.button("🗑️ Endpoint'i Sil", type="primary", disabled=not confirm):
                    try:
                        count = st.session_state.editor.remove_endpoint_by_name(endpoint_to_remove)
                        if count > 0:
                            st.success(f"✅ {count} endpoint silindi!")
                            # Endpoint listesini yenile
                            st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
                            st.rerun()
                        else:
                            st.warning("⚠️ Belirtilen isimde endpoint bulunamadı!")
                    except Exception as e:
                        st.error(f"❌ Hata: {e}")
        else:
            st.info("Endpoint listesi yüklenmemiş. Lütfen önce collection yükleyin.")
    
    elif method == "HTTP Method'una Göre Sil":
        st.subheader("🌐 HTTP Method'una Göre Silme")
        
        # Mevcut method'ları göster
        if st.session_state.get('endpoints', []):
            methods = sorted(set(ep['method'] for ep in st.session_state.endpoints))
            selected_method = st.selectbox("HTTP Method Seçin", options=["Seçin..."] + methods)
            
            if selected_method != "Seçin...":
                # Bu method'a sahip endpoint sayısını göster
                method_count = sum(1 for ep in st.session_state.endpoints if ep['method'] == selected_method)
                st.info(f"Bu method'a sahip {method_count} endpoint bulundu")
                
                confirm = st.checkbox(f"Tüm {selected_method} endpoint'lerini silmek istediğimi onaylıyorum")
                
                if st.button(f"🗑️ Tüm {selected_method} Endpoint'lerini Sil", type="primary", disabled=not confirm):
                    try:
                        count = st.session_state.editor.remove_endpoints_by_method(selected_method)
                        st.success(f"✅ {count} adet {selected_method} endpoint'i silindi!")
                        # Endpoint listesini yenile
                        st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Hata: {e}")
    
    elif method == "URL Pattern'ına Göre Sil":
        st.subheader("🔗 URL Pattern'ına Göre Silme")
        
        url_pattern = st.text_input(
            "URL Pattern",
            help="Örn: 'localhost', 'api/v1', 'users' gibi URL'de aranacak metin"
        )
        
        if url_pattern:
            # Bu pattern'a uyan endpoint'leri göster
            if st.session_state.get('endpoints', []):
                matching_endpoints = [ep for ep in st.session_state.endpoints if url_pattern.lower() in ep['url'].lower()]
                
                if matching_endpoints:
                    st.info(f"'{url_pattern}' pattern'ına uyan {len(matching_endpoints)} endpoint bulundu:")
                    for ep in matching_endpoints[:5]:  # İlk 5'ini göster
                        st.markdown(f"• {ep['name']} - {ep['url']}")
                    if len(matching_endpoints) > 5:
                        st.markdown(f"... ve {len(matching_endpoints) - 5} endpoint daha")
                else:
                    st.warning("Bu pattern'a uyan endpoint bulunamadı")
                    return
            
            confirm = st.checkbox(f"URL'inde '{url_pattern}' içeren tüm endpoint'leri silmek istediğimi onaylıyorum")
            
            if st.button("🗑️ Pattern'a Uyan Endpoint'leri Sil", type="primary", disabled=not confirm):
                try:
                    count = st.session_state.editor.remove_endpoints_by_url_pattern(url_pattern)
                    st.success(f"✅ '{url_pattern}' pattern'ını içeren {count} endpoint silindi!")
                    # Endpoint listesini yenile
                    st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
    
    elif method == "Birden Fazla Endpoint Sil":
        st.subheader("📝 Birden Fazla Endpoint Silme")
        
        endpoint_names_text = st.text_area(
            "Silinecek Endpoint İsimleri",
            help="Her satıra bir endpoint ismi yazın veya virgülle ayırın",
            placeholder="Endpoint1\nEndpoint2\nEndpoint3"
        )
        
        if endpoint_names_text:
            # Satır veya virgülle ayrılmış isimleri parse et
            if '\n' in endpoint_names_text:
                endpoint_names = [name.strip() for name in endpoint_names_text.split('\n') if name.strip()]
            else:
                endpoint_names = [name.strip() for name in endpoint_names_text.split(',') if name.strip()]
            
            if endpoint_names:
                st.info(f"Silinecek {len(endpoint_names)} endpoint:")
                for name in endpoint_names[:10]:  # İlk 10'unu göster
                    st.markdown(f"• {name}")
                if len(endpoint_names) > 10:
                    st.markdown(f"... ve {len(endpoint_names) - 10} endpoint daha")
                
                confirm = st.checkbox(f"Bu {len(endpoint_names)} endpoint'i silmek istediğimi onaylıyorum")
                
                if st.button("🗑️ Seçili Endpoint'leri Sil", type="primary", disabled=not confirm):
                    try:
                        count = st.session_state.editor.remove_multiple_endpoints(endpoint_names)
                        st.success(f"✅ Toplam {count} endpoint silindi!")
                        # Endpoint listesini yenile
                        st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Hata: {e}")

def har_converter_sidebar():
    """Sidebar'daki HAR converter"""
    
    # HAR dosya nasıl elde edilir bilgisi
    with st.expander("💡 HAR dosyası nasıl elde edilir?"):
        st.markdown("""
        1. **Chrome/Firefox**'ta **F12**'ye basın
        2. **Network** sekmesine gidin
        3. Sayfayı yenileyin veya API istekleri yapın
        4. Network'te **sağ tık** → **'Save all as HAR'**
        """)
    
    # HAR dosya yükleme
    uploaded_har = st.file_uploader(
        "HAR Dosyası Seçin",
        type=['har', 'json'],
        help="Tarayıcıdan export ettiğiniz .har dosyası",
        key="sidebar_har_upload"
    )
    
    if uploaded_har:
        st.success(f"✅ {uploaded_har.name}")
        
        # Collection adı
        default_name = f"HAR-{uploaded_har.name.split('.')[0]}"
        collection_name = st.text_input(
            "Collection Adı",
            value=default_name,
            key="sidebar_collection_name"
        )
        
        # Çevirme butonu
        if st.button("🔄 HAR'ı Çevir", type="primary", use_container_width=True):
            try:
                with st.spinner("Çevriliyor..."):
                    # Geçici dosya oluştur
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='wb', suffix='.har', delete=False) as tmp_file:
                        uploaded_har.seek(0)  # Dosya başına git
                        tmp_file.write(uploaded_har.read())
                        tmp_har_path = tmp_file.name
                    
                    # HAR'ı çevir
                    collection = PostmanCollectionEditor.har_to_postman_collection(
                        tmp_har_path, 
                        collection_name
                    )
                    
                    if collection:
                        # Session state'e kaydet
                        st.session_state.converted_collection = collection
                        st.session_state.converted_filename = f"{collection_name.replace(' ', '_')}.postman_collection.json"
                        
                        # İstatistikleri hesapla
                        total_requests = 0
                        total_domains = len(collection.get('item', []))
                        
                        for folder in collection.get('item', []):
                            if 'item' in folder:
                                total_requests += len(folder['item'])
                        
                        st.success(f"✅ Çevrildi!\n📊 {total_requests} istek, {total_domains} domain")
                        
                    else:
                        st.error("❌ Çevirme hatası!")
                    
                    # Geçici dosyayı sil
                    try:
                        os.unlink(tmp_har_path)
                    except Exception:
                        pass
                        
            except Exception as e:
                st.error(f"❌ Hata: {e}")
        
        # İndirme butonu
        if st.session_state.get('converted_collection'):
            collection_json = json.dumps(
                st.session_state.converted_collection, 
                indent=2, 
                ensure_ascii=False
            )
            
            st.download_button(
                label="📥 Collection İndir",
                data=collection_json,
                file_name=st.session_state.get('converted_filename', 'collection.json'),
                mime="application/json",
                type="secondary",
                use_container_width=True
            )
            
            # Kısa önizleme
            collection = st.session_state.converted_collection
            st.info(f"**{collection['info']['name']}**\n{len(collection.get('item', []))} domain grubunda")

def har_converter():
    """Ana alandaki HAR converter (artık kullanılmıyor)"""
    st.info("📥 HAR Converter artık sol taraftaki sidebar'da bulunuyor!")

def script_list():
    """Script listesi sekmesi"""
    st.header("🔍 Script Listesi")
    st.markdown("Collection'daki tüm script'leri görüntüleyin")
    
    if st.button("🔄 Scriptleri Tara"):
        if st.session_state.get('editor'):
            with st.spinner("Scriptler taranıyor..."):
                scripts = st.session_state.editor.list_scripts_in_collection()
                st.session_state.scripts = scripts
                st.rerun()
    
    if st.session_state.get('scripts', []):
        st.success(f"📊 Toplam {len(st.session_state.scripts)} request'te script bulundu")
        
        # Script'leri göster
        for i, item in enumerate(st.session_state.scripts, 1):
            with st.expander(f"📝 {i}. {item['name']}", expanded=False):
                for script in item['scripts']:
                    st.markdown(f"• **{script}**")
    else:
        if st.session_state.get('scripts') is not None:
            st.success("✅ Hiçbir request'te script bulunamadı!")
        else:
            st.info("👆 Scriptleri taramak için yukarıdaki butona tıklayın")

# Ana sayfa alt kısmında indirme butonu
if st.session_state.get('collection_loaded', False):
    st.divider()
    st.header("💾 Collection'ı İndir")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Güncellenmiş Collection'ı İndir", type="primary", use_container_width=True):
            try:
                # Collection'ı JSON string'e çevir
                collection_json = json.dumps(st.session_state.editor.collection, indent=2, ensure_ascii=False)
                
                # İndirme
                filename = st.session_state.uploaded_filename.replace('.json', '_updated.json')
                st.download_button(
                    label="⬇️ Dosyayı İndir",
                    data=collection_json,
                    file_name=filename,
                    mime="application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ İndirilirken hata: {e}")

if __name__ == "__main__":
    main() 