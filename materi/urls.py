from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, 
    list_materi, 
    kalender,
    list_lomba, 
    detail_lomba
)

urlpatterns = [
    # --- 1. HOME ---
    path('', home, name='home'),

    # --- 2. E-LIBRARY (Daftar & Navigasi Bertingkat) ---
    # Jalur input_materi dihapus karena upload materi hanya dilakukan via Admin Panel.
    path('library/', list_materi, name='list_materi'),

    # --- 3. KALENDER AKADEMIK ---
    path('kalender/', kalender, name='kalender'),

    # --- 4. INFO LOMBA ---
    path('info-lomba/', list_lomba, name='list_lomba'),
    path('info-lomba/<int:id>/', detail_lomba, name='detail_lomba'),
]

# --- MEDIA & STATIC CONFIG ---
# Tetap aktifkan konfigurasi ini agar file statis (CSS/JS) terbaca saat pengembangan.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)