#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Postman Collection GUI
Tkinter ile grafik arayüz
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from postman_collection_editor import PostmanCollectionEditor

class PostmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Postman Collection Düzenleyici")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Editor objesi
        self.editor = None
        self.collection_file = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Ana arayüzü oluştur"""
        
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dosya seçimi bölümü
        file_frame = ttk.LabelFrame(main_frame, text="📁 Collection Dosyası", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_var, width=60)
        file_entry.grid(row=0, column=0, padx=(0, 5))
        
        ttk.Button(file_frame, text="Dosya Seç", command=self.select_file).grid(row=0, column=1)
        ttk.Button(file_frame, text="Yükle", command=self.load_collection).grid(row=0, column=2, padx=(5, 0))
        
        # Collection bilgi bölümü
        info_frame = ttk.LabelFrame(main_frame, text="📊 Collection Bilgileri", padding="5")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=6, width=70)
        self.info_text.grid(row=0, column=0, columnspan=2)
        
        # İşlemler bölümü
        operations_frame = ttk.LabelFrame(main_frame, text="🛠️ İşlemler", padding="5")
        operations_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 5))
        
        # Header işlemleri
        header_frame = ttk.LabelFrame(operations_frame, text="Header İşlemleri", padding="5")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(header_frame, text="Header Adı:").grid(row=0, column=0, sticky=tk.W)
        self.header_name_var = tk.StringVar(value="Authorization")
        ttk.Entry(header_frame, textvariable=self.header_name_var, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(header_frame, text="Header Değeri:").grid(row=1, column=0, sticky=tk.W)
        self.header_value_var = tk.StringVar(value="Bearer TOKEN_HERE")
        ttk.Entry(header_frame, textvariable=self.header_value_var, width=20).grid(row=1, column=1, padx=5)
        
        ttk.Button(header_frame, text="Header Ekle", command=self.add_header).grid(row=0, column=2, padx=5)
        ttk.Button(header_frame, text="Header Kaldır", command=self.remove_header).grid(row=1, column=2, padx=5)
        
        # URL işlemleri
        url_frame = ttk.LabelFrame(operations_frame, text="URL İşlemleri", padding="5")
        url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(url_frame, text="Eski URL:").grid(row=0, column=0, sticky=tk.W)
        self.old_url_var = tk.StringVar(value="http://localhost:3000")
        ttk.Entry(url_frame, textvariable=self.old_url_var, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(url_frame, text="Yeni URL:").grid(row=1, column=0, sticky=tk.W)
        self.new_url_var = tk.StringVar(value="https://api.example.com")
        ttk.Entry(url_frame, textvariable=self.new_url_var, width=20).grid(row=1, column=1, padx=5)
        
        ttk.Button(url_frame, text="URL Güncelle", command=self.update_url).grid(row=0, column=2, rowspan=2, padx=5)
        
        # Metin değiştirme
        text_frame = ttk.LabelFrame(operations_frame, text="Metin Değiştirme", padding="5")
        text_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(text_frame, text="Eski Metin:").grid(row=0, column=0, sticky=tk.W)
        self.old_text_var = tk.StringVar()
        ttk.Entry(text_frame, textvariable=self.old_text_var, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(text_frame, text="Yeni Metin:").grid(row=1, column=0, sticky=tk.W)
        self.new_text_var = tk.StringVar()
        ttk.Entry(text_frame, textvariable=self.new_text_var, width=20).grid(row=1, column=1, padx=5)
        
        ttk.Button(text_frame, text="Metin Değiştir", command=self.replace_text).grid(row=0, column=2, rowspan=2, padx=5)
        
        # Environment Variable
        env_frame = ttk.LabelFrame(operations_frame, text="Environment Variable", padding="5")
        env_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(env_frame, text="Variable Adı:").grid(row=0, column=0, sticky=tk.W)
        self.env_name_var = tk.StringVar()
        ttk.Entry(env_frame, textvariable=self.env_name_var, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(env_frame, text="Variable Değeri:").grid(row=1, column=0, sticky=tk.W)
        self.env_value_var = tk.StringVar()
        ttk.Entry(env_frame, textvariable=self.env_value_var, width=20).grid(row=1, column=1, padx=5)
        
        ttk.Button(env_frame, text="Variable Ekle", command=self.add_variable).grid(row=0, column=2, rowspan=2, padx=5)
        
        # Endpoint listesi
        endpoint_frame = ttk.LabelFrame(main_frame, text="📋 Endpoint'ler", padding="5")
        endpoint_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Treeview for endpoints
        self.endpoint_tree = ttk.Treeview(endpoint_frame, columns=('method', 'name', 'url'), show='headings', height=15)
        self.endpoint_tree.heading('method', text='Method')
        self.endpoint_tree.heading('name', text='Name')
        self.endpoint_tree.heading('url', text='URL')
        
        self.endpoint_tree.column('method', width=70)
        self.endpoint_tree.column('name', width=200)
        self.endpoint_tree.column('url', width=300)
        
        scrollbar = ttk.Scrollbar(endpoint_frame, orient=tk.VERTICAL, command=self.endpoint_tree.yview)
        self.endpoint_tree.configure(yscrollcommand=scrollbar.set)
        
        self.endpoint_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Kontrol butonları
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(control_frame, text="🗑️ Scriptleri Kaldır", command=self.remove_scripts).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="🔄 Endpoint'leri Yenile", command=self.refresh_endpoints).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="💾 Yedek Oluştur", command=self.create_backup).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="💾 Kaydet", command=self.save_collection).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="💾 Farklı Kaydet", command=self.save_as).grid(row=0, column=4, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Hazır - Collection dosyası seçin")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        endpoint_frame.columnconfigure(0, weight=1)
        endpoint_frame.rowconfigure(0, weight=1)
        
    def select_file(self):
        """Dosya seçme dialog'u"""
        filename = filedialog.askopenfilename(
            title="Postman Collection Dosyası Seç",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
            
    def load_collection(self):
        """Collection'ı yükle"""
        file_path = self.file_var.get()
        if not file_path:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin!")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Hata", "Dosya bulunamadı!")
            return
            
        try:
            self.editor = PostmanCollectionEditor(file_path)
            if self.editor.load_collection():
                self.collection_file = file_path
                self.status_var.set(f"Collection yüklendi: {os.path.basename(file_path)}")
                self.update_info()
                self.refresh_endpoints()
                messagebox.showinfo("Başarılı", "Collection başarıyla yüklendi!")
            else:
                messagebox.showerror("Hata", "Collection yüklenemedi!\n\nMuhtemel sebepler:\n- Dosya geçerli JSON formatında değil\n- Encoding sorunu\n- Dosya bozuk")
        except Exception as e:
            messagebox.showerror("Hata", f"Collection yüklenirken hata: {e}\n\nDosyanın UTF-8 encoding'inde olduğundan emin olun.")
            
    def update_info(self):
        """Collection bilgilerini güncelle"""
        if not self.editor:
            return
            
        try:
            info = self.editor.collection.get('info', {})
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
            
            count_requests(self.editor.collection.get('item', []))
            
            file_size = os.path.getsize(self.collection_file) / 1024 / 1024
            
            info_text = f"""📊 Collection Bilgileri:
📝 Adı: {name}
📄 Açıklama: {description}
🔢 Toplam Request Sayısı: {request_count}
📏 Dosya Boyutu: {file_size:.2f} MB
📁 Dosya Yolu: {self.collection_file}
"""
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)
            
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, f"Bilgi güncellenirken hata: {e}")
            
    def refresh_endpoints(self):
        """Endpoint listesini yenile"""
        if not self.editor:
            return
            
        # Mevcut öğeleri temizle
        for item in self.endpoint_tree.get_children():
            self.endpoint_tree.delete(item)
            
        try:
            endpoints = self.editor.list_all_endpoints()
            for endpoint in endpoints:
                url = endpoint['url']
                if len(url) > 50:
                    url = url[:47] + "..."
                    
                self.endpoint_tree.insert('', 'end', values=(
                    endpoint['method'],
                    endpoint['name'],
                    url
                ))
                
            self.status_var.set(f"{len(endpoints)} endpoint listelendi")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Endpoint'ler listelenirken hata: {e}")
            
    def add_header(self):
        """Header ekle"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        header_name = self.header_name_var.get().strip()
        header_value = self.header_value_var.get().strip()
        
        if not header_name or not header_value:
            messagebox.showwarning("Uyarı", "Header adı ve değeri boş olamaz!")
            return
            
        try:
            count = self.editor.add_header_to_all_requests(header_name, header_value)
            self.status_var.set(f"{count} request'e '{header_name}' header'ı eklendi")
            messagebox.showinfo("Başarılı", f"{count} request'e header eklendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Header eklenirken hata: {e}")
            
    def remove_header(self):
        """Header kaldır"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        header_name = self.header_name_var.get().strip()
        
        if not header_name:
            messagebox.showwarning("Uyarı", "Header adı boş olamaz!")
            return
            
        try:
            count = self.editor.remove_header_from_all_requests(header_name)
            self.status_var.set(f"{count} request'ten '{header_name}' header'ı kaldırıldı")
            messagebox.showinfo("Başarılı", f"{count} request'ten header kaldırıldı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Header kaldırılırken hata: {e}")
            
    def update_url(self):
        """URL güncelle"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        old_url = self.old_url_var.get().strip()
        new_url = self.new_url_var.get().strip()
        
        if not old_url or not new_url:
            messagebox.showwarning("Uyarı", "URL'ler boş olamaz!")
            return
            
        try:
            count = self.editor.update_base_url(old_url, new_url)
            self.status_var.set(f"{count} request'te URL güncellendi")
            self.refresh_endpoints()
            messagebox.showinfo("Başarılı", f"{count} request'te URL güncellendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"URL güncellenirken hata: {e}")
            
    def replace_text(self):
        """Metin değiştir"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        old_text = self.old_text_var.get().strip()
        new_text = self.new_text_var.get().strip()
        
        if not old_text or not new_text:
            messagebox.showwarning("Uyarı", "Metinler boş olamaz!")
            return
            
        try:
            count = self.editor.replace_text_in_requests(old_text, new_text)
            self.status_var.set(f"{count} request'te metin değiştirildi")
            self.refresh_endpoints()
            messagebox.showinfo("Başarılı", f"{count} request'te metin değiştirildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Metin değiştirilirken hata: {e}")
            
    def add_variable(self):
        """Environment variable ekle"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        var_name = self.env_name_var.get().strip()
        var_value = self.env_value_var.get().strip()
        
        if not var_name or not var_value:
            messagebox.showwarning("Uyarı", "Variable adı ve değeri boş olamaz!")
            return
            
        try:
            self.editor.add_environment_variable(var_name, var_value)
            self.status_var.set(f"'{var_name}' variable'ı eklendi")
            messagebox.showinfo("Başarılı", "Environment variable eklendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Variable eklenirken hata: {e}")
            
    def remove_scripts(self):
        """Scriptleri kaldır"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        result = messagebox.askyesno("Onay", "Tüm pre-request ve test scriptlerini kaldırmak istediğinizden emin misiniz?")
        if not result:
            return
            
        try:
            count = self.editor.remove_all_scripts()
            self.status_var.set(f"{count} request'ten scriptler kaldırıldı")
            messagebox.showinfo("Başarılı", f"{count} request'ten scriptler kaldırıldı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Scriptler kaldırılırken hata: {e}")
            
    def create_backup(self):
        """Yedek oluştur"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        try:
            if self.editor.create_backup():
                self.status_var.set("Yedek başarıyla oluşturuldu")
                messagebox.showinfo("Başarılı", "Yedek başarıyla oluşturuldu!")
            else:
                messagebox.showerror("Hata", "Yedek oluşturulamadı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Yedek oluşturulurken hata: {e}")
            
    def save_collection(self):
        """Collection'ı kaydet"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        try:
            if self.editor.save_collection():
                self.status_var.set("Collection kaydedildi")
                messagebox.showinfo("Başarılı", "Collection başarıyla kaydedildi!")
            else:
                messagebox.showerror("Hata", "Collection kaydedilemedi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Collection kaydedilirken hata: {e}")
            
    def save_as(self):
        """Collection'ı farklı kaydet"""
        if not self.editor:
            messagebox.showwarning("Uyarı", "Önce collection yükleyin!")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Collection'ı Farklı Kaydet",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if self.editor.save_collection(filename):
                    self.status_var.set(f"Collection kaydedildi: {os.path.basename(filename)}")
                    messagebox.showinfo("Başarılı", f"Collection kaydedildi: {filename}")
                else:
                    messagebox.showerror("Hata", "Collection kaydedilemedi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Collection kaydedilirken hata: {e}")

def main():
    root = tk.Tk()
    app = PostmanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 