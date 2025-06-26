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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔧 Header İşlemleri", 
        "📝 Metin Değiştirme", 
        "🗑️ Script Temizleme",
        "⚙️ Environment Variables",
        "📋 Endpoint'ler"
    ])
    
    with tab1:
        header_operations()
    
    with tab2:
        text_operations()
        
    with tab3:
        script_operations()
        
    with tab4:
        environment_operations()
        
    with tab5:
        endpoint_list()

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
    """Endpoint listesi ve detay düzenleme sekmesi"""
    st.header("📋 Endpoint'ler")
    
    # Görünüm modu seçimi
    view_mode = st.radio(
        "Görünüm Modu:",
        ["📋 Liste Görünümü", "🔍 Detay Görünümü"],
        horizontal=True
    )
    
    if st.button("🔄 Listeyi Yenile"):
        if st.session_state.get('editor'):
            st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
            st.rerun()
    
        if not st.session_state.get('endpoints', []):
            st.info("Endpoint bulunamadı")
            return

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
    
    if view_mode == "📋 Liste Görünümü":
        # Basit tablo görünümü
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        # Detaylı görünüm
        endpoint_detail_view(filtered_df)

def endpoint_detail_view(filtered_df):
    """Endpoint detay görünümü ve düzenleme"""
    
    if filtered_df.empty:
        st.info("Filtreleme kriterlerine uygun endpoint bulunamadı")
        return
    
    # Endpoint seçimi
    endpoint_names = [f"{row['method']} - {row['name']}" for _, row in filtered_df.iterrows()]
    selected_endpoint_display = st.selectbox(
        "Düzenlemek İstediğiniz Endpoint'i Seçin:",
        options=["Seçin..."] + endpoint_names
    )
    
    if selected_endpoint_display == "Seçin...":
        st.info("👆 Yukarıdan bir endpoint seçin")
        return
    
    # Seçilen endpoint'in index'ini bul
    selected_index = endpoint_names.index(selected_endpoint_display)
    selected_endpoint = filtered_df.iloc[selected_index]
    
    # Collection'dan tam endpoint verisini al
    endpoint_data = find_endpoint_in_collection(selected_endpoint['name'])
    
    if not endpoint_data:
        st.error("❌ Endpoint verisi bulunamadı!")
        return
    
    # Endpoint düzenleme arayüzü
    edit_endpoint_interface(endpoint_data, selected_endpoint)

def find_endpoint_in_collection(endpoint_name):
    """Collection'da endpoint'i bul ve tam verisini döndür"""
    def search_in_items(items, target_name):
        for item in items:
            if 'request' in item and item.get('name', '') == target_name:
                return item
            elif 'item' in item:
                result = search_in_items(item['item'], target_name)
                if result:
                    return result
        return None
    
    if st.session_state.get('editor') and st.session_state.editor.collection:
        return search_in_items(st.session_state.editor.collection.get('item', []), endpoint_name)
    return None

def edit_endpoint_interface(endpoint_data, selected_endpoint):
    """Endpoint düzenleme arayüzü"""
    
    st.subheader(f"🔧 {selected_endpoint['name']} Düzenleme")
    
    # Tablar ile kategorize edilmiş düzenleme
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Genel Bilgiler",
        "🔗 Headers", 
        "📄 Body",
        "📜 Scripts",
        "⚙️ Variables"
    ])
    
    # Genel Bilgiler Tab'ı
    with tab1:
        edit_general_info(endpoint_data)
    
    # Headers Tab'ı
    with tab2:
        edit_headers(endpoint_data)
    
    # Body Tab'ı  
    with tab3:
        edit_body(endpoint_data)
    
    # Scripts Tab'ı
    with tab4:
        edit_scripts(endpoint_data)
    
    # Variables Tab'ı
    with tab5:
        edit_variables(endpoint_data)
    
    # Kaydet butonu
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Değişiklikleri Kaydet", type="primary", use_container_width=True):
            try:
                # Endpoint listesini yenile
                st.session_state.endpoints = st.session_state.editor.list_all_endpoints()
                st.success("✅ Değişiklikler kaydedildi!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Kaydetme hatası: {e}")

def edit_general_info(endpoint_data):
    """Genel bilgiler düzenleme"""
    st.markdown("### 📝 Genel Bilgiler")
    
    request = endpoint_data.get('request', {})
    
    # Endpoint adı
    new_name = st.text_input(
        "Endpoint Adı:",
        value=endpoint_data.get('name', ''),
        key="edit_name"
    )
    if new_name != endpoint_data.get('name', ''):
        endpoint_data['name'] = new_name
    
    # HTTP Method
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    current_method = request.get('method', 'GET')
    new_method = st.selectbox(
        "HTTP Method:",
        options=methods,
        index=methods.index(current_method) if current_method in methods else 0,
        key="edit_method"
    )
    if new_method != current_method:
        request['method'] = new_method
    
    # URL
    current_url = request.get('url', '')
    if isinstance(current_url, dict):
        current_url = current_url.get('raw', '')
    
    new_url = st.text_area(
        "URL:",
        value=current_url,
        height=100,
        key="edit_url"
    )
    if new_url != current_url:
        if isinstance(request.get('url'), dict):
            request['url']['raw'] = new_url
        else:
            request['url'] = new_url
    
    # Açıklama
    current_description = endpoint_data.get('request', {}).get('description', '')
    new_description = st.text_area(
        "Açıklama:",
        value=current_description,
        key="edit_description"
    )
    if new_description != current_description:
        if 'request' not in endpoint_data:
            endpoint_data['request'] = {}
        endpoint_data['request']['description'] = new_description

def edit_headers(endpoint_data):
    """Headers düzenleme"""
    st.markdown("### 🔗 Headers")
    
    request = endpoint_data.get('request', {})
    headers = request.get('header', [])
    
    # Mevcut header'ları göster
    if headers:
        st.markdown("**Mevcut Headers:**")
        
        headers_to_remove = []
        for i, header in enumerate(headers):
            if isinstance(header, dict):
                col1, col2, col3, col4 = st.columns([3, 3, 1, 1])
                
                with col1:
                    new_key = st.text_input(
                        f"Key {i+1}:",
                        value=header.get('key', ''),
                        key=f"header_key_{i}"
                    )
                    header['key'] = new_key
                
                with col2:
                    new_value = st.text_input(
                        f"Value {i+1}:",
                        value=header.get('value', ''),
                        key=f"header_value_{i}"
                    )
                    header['value'] = new_value
                
                with col3:
                    enabled = st.checkbox(
                        "Aktif",
                        value=not header.get('disabled', False),
                        key=f"header_enabled_{i}"
                    )
                    header['disabled'] = not enabled
                
                with col4:
                    if st.button("🗑️", key=f"remove_header_{i}", help="Header'ı sil"):
                        headers_to_remove.append(i)
        
        # Silinecek header'ları kaldır
        for i in reversed(headers_to_remove):
            headers.pop(i)
    else:
        st.info("Header bulunamadı")
    
    # Yeni header ekleme
    st.markdown("**Yeni Header Ekle:**")
    col1, col2, col3 = st.columns([3, 3, 2])
    
    with col1:
        new_header_key = st.text_input("Yeni Header Key:", key="new_header_key")
    
    with col2:
        new_header_value = st.text_input("Yeni Header Value:", key="new_header_value")
    
    with col3:
        if st.button("➕ Header Ekle", key="add_header"):
            if new_header_key and new_header_value:
                if 'header' not in request:
                    request['header'] = []
                
                new_header = {
                    "key": new_header_key,
                    "value": new_header_value,
                    "type": "text"
                }
                request['header'].append(new_header)
                st.success(f"✅ Header eklendi: {new_header_key}")
                st.rerun()

def edit_body(endpoint_data):
    """Body düzenleme"""
    st.markdown("### 📄 Request Body")
    
    request = endpoint_data.get('request', {})
    body = request.get('body', {})
    
    # Body mode seçimi
    if body:
        current_mode = body.get('mode', 'raw')
    else:
        current_mode = 'raw'
    
    body_modes = ['raw', 'urlencoded', 'formdata', 'binary', 'graphql']
    new_mode = st.selectbox(
        "Body Tipi:",
        options=body_modes,
        index=body_modes.index(current_mode) if current_mode in body_modes else 0,
        key="body_mode"
    )
    
    if new_mode != current_mode:
        if 'body' not in request:
            request['body'] = {}
        request['body']['mode'] = new_mode
        body = request['body']
    
    # Body içeriği düzenleme
    if new_mode == 'raw':
        # Raw body
        current_raw = body.get('raw', '') if body else ''
        
        # Language seçimi
        if body and 'options' in body and 'raw' in body['options']:
            current_lang = body['options']['raw'].get('language', 'json')
        else:
            current_lang = 'json'
        
        languages = ['json', 'text', 'javascript', 'html', 'xml']
        new_lang = st.selectbox(
            "Dil:",
            options=languages,
            index=languages.index(current_lang) if current_lang in languages else 0,
            key="body_language"
        )
        
        # Minimal format butonları
        col1, col2, col3 = st.columns([8, 1, 1])
        
        with col2:
            if st.button("🎨", key="format_body", help="Akıllı formatla"):
                try:
                    # Otomatik format tespiti
                    content = current_raw.strip()
                    if content.startswith('{') or content.startswith('['):
                        # JSON formatla
                        import json
                        parsed_json = json.loads(content)
                        formatted = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                        st.session_state['beautified_body'] = formatted
                        st.success("✅ Formatlandı")
                    elif content.startswith('<'):
                        # XML formatla
                        import xml.dom.minidom
                        dom = xml.dom.minidom.parseString(content)
                        formatted_xml = dom.toprettyxml(indent="  ")
                        lines = formatted_xml.split('\n')[1:]
                        formatted = '\n'.join([line for line in lines if line.strip()])
                        st.session_state['beautified_body'] = formatted
                        st.success("✅ Formatlandı")
                    else:
                        st.info("Format algılanamadı")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
        
        with col3:
            if st.button("⚡", key="minify_body", help="Sıkıştır"):
                try:
                    content = current_raw.strip()
                    if content.startswith('{') or content.startswith('['):
                        # JSON minify
                        import json
                        parsed_json = json.loads(content)
                        minified = json.dumps(parsed_json, separators=(',', ':'), ensure_ascii=False)
                        st.session_state['beautified_body'] = minified
                        st.success("✅ Sıkıştırıldı")
                    else:
                        # Genel minify
                        import re
                        minified = re.sub(r'\s+', ' ', content)
                        st.session_state['beautified_body'] = minified
                        st.success("✅ Sıkıştırıldı")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
    
        # Beautify sonucunu kullan
        display_body = st.session_state.get('beautified_body', current_raw)
        if st.session_state.get('beautified_body'):
            # Beautify yapıldıysa, onu göster ve temizle
            current_raw = st.session_state['beautified_body']
            del st.session_state['beautified_body']
        
        new_raw = st.text_area(
            "Raw Body:",
            value=current_raw,
            height=200,
            key="body_raw",
            help="💡 Yukarıdaki butonları kullanarak kodu formatlandırabilirsiniz"
        )
        
        if new_raw != current_raw or new_lang != current_lang:
            if 'body' not in request:
                request['body'] = {}
            request['body']['mode'] = 'raw'
            request['body']['raw'] = new_raw
            request['body']['options'] = {
                'raw': {
                    'language': new_lang
                }
            }
    
    elif new_mode == 'urlencoded':
        # URL encoded form data
        st.markdown("**Form Data (URL Encoded):**")
        
        urlencoded_data = body.get('urlencoded', []) if body else []
        
        # Mevcut form data'yı göster
        data_to_remove = []
        for i, data in enumerate(urlencoded_data):
            col1, col2, col3, col4 = st.columns([3, 3, 1, 1])
            
            with col1:
                new_key = st.text_input(
                    f"Key {i+1}:",
                    value=data.get('key', ''),
                    key=f"form_key_{i}"
                )
                data['key'] = new_key
            
            with col2:
                new_value = st.text_input(
                    f"Value {i+1}:",
                    value=data.get('value', ''),
                    key=f"form_value_{i}"
                )
                data['value'] = new_value
            
            with col3:
                enabled = st.checkbox(
                    "Aktif",
                    value=not data.get('disabled', False),
                    key=f"form_enabled_{i}"
                )
                data['disabled'] = not enabled
            
            with col4:
                if st.button("🗑️", key=f"remove_form_{i}", help="Alanı sil"):
                    data_to_remove.append(i)
        
        # Silinecek alanları kaldır
        for i in reversed(data_to_remove):
            urlencoded_data.pop(i)
        
        # Yeni alan ekleme
        st.markdown("**Yeni Alan Ekle:**")
        col1, col2, col3 = st.columns([3, 3, 2])
        
        with col1:
            new_form_key = st.text_input("Yeni Key:", key="new_form_key")
        
        with col2:
            new_form_value = st.text_input("Yeni Value:", key="new_form_value")
        
        with col3:
            if st.button("➕ Alan Ekle", key="add_form_field"):
                if new_form_key:
                    if 'body' not in request:
                        request['body'] = {}
                    if 'urlencoded' not in request['body']:
                        request['body']['urlencoded'] = []
                    
                    new_field = {
                        "key": new_form_key,
                        "value": new_form_value,
                        "type": "text"
                    }
                    request['body']['urlencoded'].append(new_field)
                    st.success(f"✅ Alan eklendi: {new_form_key}")
                    st.rerun()

def edit_scripts(endpoint_data):
    """Scripts düzenleme"""
    st.markdown("### 📜 Scripts")
    
    request = endpoint_data.get('request', {})
    
    # Pre-request Script
    st.markdown("**Pre-request Script:**")
    prerequest = request.get('prerequest', {})
    
    if isinstance(prerequest, dict):
        current_prereq = '\n'.join(prerequest.get('exec', [])) if prerequest.get('exec') else ''
    else:
        current_prereq = str(prerequest) if prerequest else ''
    
    new_prereq = st.text_area(
        "Pre-request Script:",
        value=current_prereq,
        height=150,
        key="prerequest_script",
        help="JavaScript kodu yazın"
    )
    
    if new_prereq != current_prereq:
        if new_prereq.strip():
            request['prerequest'] = {
                'exec': new_prereq.split('\n'),
                'type': 'text/javascript'
            }
        else:
            request['prerequest'] = {'exec': [], 'type': 'text/javascript'}
    
    # Test Script
    st.markdown("**Test Script:**")
    
    # Event'larda test script'i ara
    events = request.get('event', [])
    test_event = None
    for event in events:
        if event.get('listen') == 'test':
            test_event = event
            break
    
    if test_event and test_event.get('script', {}).get('exec'):
        current_test = '\n'.join(test_event['script']['exec'])
    else:
        current_test = ''
    
    new_test = st.text_area(
        "Test Script:",
        value=current_test,
        height=150,
        key="test_script",
        help="Test JavaScript kodu yazın"
    )
    
    if new_test != current_test:
        if 'event' not in request:
            request['event'] = []
        
        # Mevcut test event'ini kaldır
        request['event'] = [e for e in request['event'] if e.get('listen') != 'test']
        
        # Yeni test event'i ekle
        if new_test.strip():
            test_event = {
                'listen': 'test',
                'script': {
                    'exec': new_test.split('\n'),
                    'type': 'text/javascript'
                }
            }
            request['event'].append(test_event)

def edit_variables(endpoint_data):
    """Variables düzenleme"""
    st.markdown("### ⚙️ Variables")
    
    # Endpoint seviyesinde variable yok, collection seviyesinde var
    st.info("💡 Variables collection seviyesinde tanımlanır. Endpoint'e özel variable yoktur.")
    
    # Collection variables'ı göster
    if st.session_state.get('editor') and st.session_state.editor.collection:
        collection_vars = st.session_state.editor.collection.get('variable', [])
        
        if collection_vars:
            st.markdown("**Collection Variables:**")
            for var in collection_vars:
                st.code(f"{var.get('key', 'unknown')} = {var.get('value', '')}")
        else:
            st.info("Collection'da tanımlı variable bulunamadı")
    
    # URL'de kullanılan variable'ları tespit et
    request = endpoint_data.get('request', {})
    url = request.get('url', '')
    if isinstance(url, dict):
        url = url.get('raw', '')
    
    import re
    variables_in_url = re.findall(r'\{\{([^}]+)\}\}', str(url))
    
    if variables_in_url:
        st.markdown("**Bu Endpoint'te Kullanılan Variables:**")
        for var in set(variables_in_url):
            st.markdown(f"• `{{{{{var}}}}}`")
    else:
        st.info("Bu endpoint'te variable kullanımı bulunamadı")

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