"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include

# --- 1. IMPORT PENTING (Wajib ada) ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Halaman Admin Django
    path('admin/', admin.site.urls),
    
    # Menghubungkan ke aplikasi 'materi'
    path('', include('materi.urls')),
]

# --- 2. KONFIGURASI KHUSUS AGAR GAMBAR MUNCUL ---
# Bagian ini hanya berjalan saat mode pengembangan (DEBUG = True)
if settings.DEBUG:
    # Mengizinkan Django menampilkan file dari folder MEDIA (Foto user, Pamflet, dll)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)