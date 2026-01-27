from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Untuk notifikasi
from django.db.models import Q       # Untuk pencarian
from django.core.paginator import Paginator # Pagination
from datetime import date            # Untuk filter tanggal
from itertools import chain          # Untuk menggabungkan querysets (list_lomba)

# Import Models (Pastikan semua model ter-import)
from .models import Materi, Prestasi, Karya, InfoLomba, AgendaKalender, FileKalender
# Import Form
from .forms import MateriForm, KaryaForm, PrestasiForm

# --- 1. HOMEPAGE ("ELEKTRO BANGGA") ---
def home(request):
    # 1. Ambil 6 prestasi terbaru (approved)
    prestasi_list = Prestasi.objects.filter(status='approved').order_by('-created_at')[:6]
    
    today = date.today()

    # 2. Ambil 3 info lomba terbaru (Yang deadline-nya belum lewat)
    info_lomba_list = InfoLomba.objects.filter(
        Q(tanggal_deadline__gte=today) | Q(tanggal_deadline__isnull=True)
    ).order_by('tanggal_deadline')[:3]

    # 3. KARYA MAHASISWA - Ambil 4 karya terbaru
    karya_list = Karya.objects.filter(status='approved').order_by('-created_at')[:4]
    
    # 4. KALENDER (Agenda mendatang untuk Kartu Beranda)
    # Mengambil 4 agenda terdekat dari hari ini
    agenda_list = AgendaKalender.objects.filter(
        tanggal_mulai__gte=today
    ).order_by('tanggal_mulai')[:4]

    return render(request, 'materi/home.html', {
        'prestasi_list': prestasi_list,
        'info_lomba_list': info_lomba_list,
        'karya_list': karya_list, 
        'agenda_list': agenda_list, 
    })


# --- 2. LOGIC INPUT MATERI ---
def input_materi(request):
    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Terima kasih! Materi berhasil dikirim dan menunggu verifikasi Admin.')
            return redirect('list_materi')
        else:
            messages.error(request, 'Ada kesalahan input. Mohon periksa kembali.')
    else:
        form = MateriForm()

    return render(request, 'materi/input_materi.html', {'form': form})


# --- 3. LOGIC INPUT PRESTASI ---
def input_prestasi(request):
    if request.method == "POST":
        form = PrestasiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Prestasi berhasil dikirim! Menunggu verifikasi admin.')
            return redirect('list_prestasi')
        else:
            messages.error(request, 'Gagal mengirim. Periksa kembali isian form atau ukuran foto.')
    else:
        form = PrestasiForm()

    return render(request, 'materi/input_prestasi.html', {'form': form})


# --- 4. LOGIC INPUT KARYA ---
def input_karya(request):
    if request.method == 'POST':
        form = KaryaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Keren! Karya kamu sudah masuk antrian verifikasi.')
            return redirect('list_karya')
        else:
             messages.error(request, 'Gagal upload. Pastikan ukuran foto maksimal 2MB.')
    else:
        form = KaryaForm()

    return render(request, 'materi/input_karya.html', {'form': form})


# --- 5. PERPUSTAKAAN (LIST MATERI) ---
def list_materi(request):
    # 1. Ambil semua data approved
    materi_list = Materi.objects.filter(status='approved').order_by('-tanggal_upload')

    # 2. Filter & Search Logic
    cari_judul = request.GET.get('keyword')
    prodi = request.GET.get('prodi')
    semester = request.GET.get('semester')
    
    if cari_judul:
        materi_list = materi_list.filter(
            Q(judul__icontains=cari_judul) | 
            Q(mata_kuliah__icontains=cari_judul)
        )
    if prodi and prodi != '':
        materi_list = materi_list.filter(prodi=prodi)
    if semester and semester != '':
        materi_list = materi_list.filter(semester=semester)

    # 3. PAGINATION (16 item per halaman)
    paginator = Paginator(materi_list, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'materi': page_obj,
        'filter_prodi': prodi,
        'filter_semester': semester,
    }

    return render(request, 'materi/list_materi.html', context)


# --- 6. HALAMAN LIST KARYA (GALERI) ---
def list_karya(request):
    # 1. Ambil data approved
    karya_list = Karya.objects.filter(status='approved')

    # 2. Fitur Sorting (Terbaru / Terlama)
    sort_by = request.GET.get('sort', 'terbaru') # Default terbaru
    
    if sort_by == 'terlama':
        karya_list = karya_list.order_by('created_at') # Ascending (Lama ke Baru)
    else:
        karya_list = karya_list.order_by('-created_at') # Descending (Baru ke Lama)

    # 3. Pagination (16 karya per halaman -> Grid 4x4)
    paginator = Paginator(karya_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materi/list_karya.html', {'karya_list': page_obj})


# --- 7. DETAIL KARYA ---
def detail_karya(request, id):
    karya = get_object_or_404(Karya, id=id)
    return render(request, 'materi/detail_karya.html', {'karya': karya})


# --- 8. HALAMAN LIST PRESTASI (HALL OF FAME) ---
def list_prestasi(request):
    # 1. Ambil Data
    prestasi_list = Prestasi.objects.filter(status='approved').order_by('-created_at')

    # 2. Fitur Search
    keyword = request.GET.get('keyword')
    prodi = request.GET.get('prodi')

    if keyword:
        prestasi_list = prestasi_list.filter(
            Q(nama_mahasiswa__icontains=keyword) | 
            Q(nama_lomba__icontains=keyword)
        )
    
    if prodi and prodi != '':
        prestasi_list = prestasi_list.filter(prodi=prodi)

    # 3. PAGINATION (UPDATE UTAMA DI SINI)
    # Batasi 16 item per halaman (4 baris x 4 kolom)
    paginator = Paginator(prestasi_list, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materi/list_prestasi.html', {
        'prestasi_list': page_obj, # Kirim objek halaman, bukan list mentah
        'filter_prodi': prodi      # Kirim balik filter agar tidak hilang saat ganti halaman
    })


# --- 9. KALENDER AKADEMIK ---
def kalender(request):
    # 1. Ambil semua agenda urut tanggal
    agenda_list = AgendaKalender.objects.all().order_by('tanggal_mulai')
    
    # 2. Ambil file PDF terakhir yang diupload admin
    file_kalender = FileKalender.objects.last()

    return render(request, 'materi/kalender.html', {
        'agenda_list': agenda_list,
        'file_kalender': file_kalender
    })


# --- 10. LIST SEMUA LOMBA ---
def list_lomba(request):
    # Ambil semua lomba, urutkan berdasarkan deadline terdekat yang belum lewat
    today = date.today()
    
    # Pisahkan lomba aktif dan sudah lewat
    lomba_aktif = InfoLomba.objects.filter(
        Q(tanggal_deadline__gte=today) | Q(tanggal_deadline__isnull=True)
    ).order_by('tanggal_deadline')
    
    lomba_lewat = InfoLomba.objects.filter(
        tanggal_deadline__lt=today
    ).order_by('-tanggal_deadline')
    
    # Gabungkan (Aktif dulu, baru yang sudah lewat)
    semua_lomba = list(chain(lomba_aktif, lomba_lewat))

    return render(request, 'materi/list_lomba.html', {'lomba_list': semua_lomba})


# --- 11. DETAIL INFO LOMBA ---
def detail_lomba(request, id):
    lomba = get_object_or_404(InfoLomba, id=id)
    return render(request, 'materi/detail_lomba.html', {'lomba': lomba})


# --- 12. DETAIL PRESTASI ---
def detail_prestasi(request, id):
    # Mengambil satu objek prestasi berdasarkan ID
    item = get_object_or_404(Prestasi, id=id)
    
    # PENTING: Key dictionary HARUS 'prestasi' agar sesuai dengan template HTML
    return render(request, 'materi/detail_prestasi.html', {'prestasi': item})