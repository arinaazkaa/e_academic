from django.urls import path
from .views import (
    home, 
    input_materi, list_materi, 
    input_prestasi, list_prestasi, 
    input_karya, list_karya, 
    kalender,
    detail_lomba,
    detail_prestasi   # <--- WAJIB DITAMBAHKAN (Agar halaman detail bisa dibuka)
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

    # 4. PRESTASI MAHASISWA
    path('prestasi/', list_prestasi, name='list_prestasi'),
    path('prestasi/input/', input_prestasi, name='input_prestasi'),
    
    # URL BARU: Halaman Detail Prestasi (Untuk melihat foto besar & info lengkap)
    path('prestasi/<int:id_prestasi>/', detail_prestasi, name='detail_prestasi'),

    # 5. KALENDER AKADEMIK
    path('kalender/', kalender, name='kalender'),

    # 6. DETAIL INFO LOMBA
    path('lomba/<int:id_lomba>/', detail_lomba, name='detail_lomba'),
]