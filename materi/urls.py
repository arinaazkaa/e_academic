from django.urls import path
from .views import (
    home, 
    input_materi, list_materi, 
    input_prestasi, list_prestasi, detail_prestasi, 
    input_karya, list_karya, detail_karya, # <--- Tambahkan detail_karya di sini
    kalender,
    list_lomba, detail_lomba
)

urlpatterns = [
    # 1. HOMEPAGE
    path('', home, name='home'),

    # 2. E-LIBRARY (Materi)
    path('library/', list_materi, name='list_materi'),
    path('library/input/', input_materi, name='input_materi'),

    # 3. KARYA MAHASISWA
    path('karya/', list_karya, name='list_karya'),
    path('karya/input/', input_karya, name='input_karya'),
    
    # Detail Karya (URL Baru untuk Halaman Detail)
    path('karya/<int:id>/', detail_karya, name='detail_karya'),

    # 4. PRESTASI MAHASISWA
    path('prestasi/', list_prestasi, name='list_prestasi'),
    path('prestasi/input/', input_prestasi, name='input_prestasi'),
    
    # Detail Prestasi
    path('prestasi/<int:id>/', detail_prestasi, name='detail_prestasi'),

    # 5. KALENDER AKADEMIK
    path('kalender/', kalender, name='kalender'),

    # 6. INFO LOMBA
    # List Semua Lomba
    path('info-lomba/', list_lomba, name='list_lomba'),
    
    # Detail Lomba
    path('info-lomba/<int:id>/', detail_lomba, name='detail_lomba'),
]