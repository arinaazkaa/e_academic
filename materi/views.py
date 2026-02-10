from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date

# Mengimpor model terbaru
from .models import Materi, InfoLomba, AgendaAkademik, KalenderPDF

# --- KONSTANTA DESAIN: PALET WARNA KONSISTEN ---
PRODI_DATA = [
    ('PTIK', 'PTIK', '#eff6ff'),   # Soft Blue
    ('PTE', 'PTE', '#fef2f2'),     # Soft Red
    ('TE', 'TE', '#f5f3ff'),       # Soft Purple
    ('TEKKOM', 'TEKKOM', '#f0fdf4'),   # Soft Green
    ('MKU', 'MKU', '#fffbeb'),     # Soft Amber
]

# --- 1. BERANDA (HOMEPAGE) ---
def home(request):
    """Menampilkan ringkasan informasi terbaru dan tombol download kalender."""
    today = date.today()

    # Mengambil info lomba aktif terdekat
    info_lomba_list = InfoLomba.objects.filter(
        tanggal_pelaksanaan__gte=today,
        is_active=True
    ).order_by('tanggal_pelaksanaan')[:3]

    materi_terbaru = Materi.objects.all().order_by('-tanggal_upload')[:3]
    
    agenda_list = AgendaAkademik.objects.filter(
        tanggal_mulai__gte=today
    ).order_by('tanggal_mulai')[:4]

    kalender_data = KalenderPDF.objects.last()

    return render(request, 'materi/home.html', {
        'info_lomba_list': info_lomba_list,
        'agenda_list': agenda_list, 
        'materi_terbaru': materi_terbaru,
        'prodi_data': PRODI_DATA,
        'kalender_data': kalender_data,
    })

# --- 2. E-LIBRARY (DAFTAR MATERI BERTINGKAT) ---
def list_materi(request):
    """Menangani navigasi folder Prodi -> Semester -> List Materi."""
    materi_list = Materi.objects.all().order_by('mata_kuliah')
    
    keyword = request.GET.get('keyword')
    prodi = request.GET.get('prodi')
    semester = request.GET.get('semester')
    
    if keyword:
        materi_list = materi_list.filter(
            Q(judul__icontains=keyword) | Q(mata_kuliah__icontains=keyword)
        )
    
    if prodi:
        materi_list = materi_list.filter(prodi=prodi)
        if prodi != 'MKU' and semester:
            materi_list = materi_list.filter(semester=semester)
    
    paginator = Paginator(materi_list, 12) 
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'materi/list_materi.html', {
        'materi': page_obj,
        'filter_prodi': prodi,
        'filter_semester': semester,
        'prodi_data': PRODI_DATA,
    })

# --- 3. KALENDER AKADEMIK ---
def kalender(request):
    agenda_list = AgendaAkademik.objects.all().order_by('tanggal_mulai')
    kalender_data = KalenderPDF.objects.last()

    return render(request, 'materi/kalender.html', {
        'agenda_list': agenda_list,
        'kalender_data': kalender_data,
    })

# --- 4. INFO LOMBA (FIXED & LOGIKA SORTING) ---
def list_lomba(request):
    """Menampilkan daftar lomba dengan fitur pencarian dan pengurutan."""
    # Default: Ambil semua lomba
    lombas = InfoLomba.objects.all()
    
    # Fitur Pencarian
    query = request.GET.get('q')
    if query:
        lombas = lombas.filter(
            Q(judul__icontains=query) | Q(penyelenggara__icontains=query)
        )

    # Fitur Pengurutan (Sorting)
    sort_by = request.GET.get('sort', 'deadline') # Default ke deadline
    if sort_by == 'terbaru':
        lombas = lombas.order_by('-id') # Berdasarkan urutan upload terbaru
    else:
        lombas = lombas.order_by('tanggal_deadline') # Berdasarkan deadline terdekat

    return render(request, 'materi/list_lomba.html', {
        'info_lomba_list': lombas, # Nama variabel disamakan dengan template
    })

# --- 5. DETAIL LOMBA ---
def detail_lomba(request, id):
    lomba = get_object_or_404(InfoLomba, id=id)
    return render(request, 'materi/detail_lomba.html', {'info_lomba': lomba})