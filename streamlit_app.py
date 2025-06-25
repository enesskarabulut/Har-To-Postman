#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App Entry Point for Vercel Deployment
"""

import sys
import os

# WSGI uyumluluğu için
def application(environ, start_response):
    """WSGI application entry point"""
    os.system("streamlit run postman_web_app.py --server.port 8000 --server.address 0.0.0.0")

# Vercel deployment için ana giriş noktası
if __name__ == "__main__":
    from postman_web_app import main
    main() 