from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, 
    input_materi, list_materi, 
    input_prestasi, list_prestasi, detail_prestasi, 
    input_karya, list_karya, detail_karya, 
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
    path('karya/<int:id>/', detail_karya, name='detail_karya'), # Detail

    # 4. PRESTASI MAHASISWA
    path('prestasi/', list_prestasi, name='list_prestasi'),
    path('prestasi/input/', input_prestasi, name='input_prestasi'),
    path('prestasi/<int:id>/', detail_prestasi, name='detail_prestasi'), # Detail

    # 5. KALENDER AKADEMIK
    path('kalender/', kalender, name='kalender'),

    # 6. INFO LOMBA
    path('info-lomba/', list_lomba, name='list_lomba'),
    path('info-lomba/<int:id>/', detail_lomba, name='detail_lomba'), # Detail
]

# --- PENTING: Konfigurasi agar foto bisa dibuka ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)